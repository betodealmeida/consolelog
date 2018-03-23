import json
import logging
import os.path
from queue import Queue

from werkzeug.wrappers import Response
from wsgigzip import gzip


# map between Python levels and the console method in Javascript
levels = {
    logging.CRITICAL: 'error',
    logging.ERROR: 'error',
    logging.WARNING: 'warn',
    logging.INFO: 'info',
    logging.DEBUG: 'debug',
    logging.NOTSET: 'log',
}


class DictHandler(logging.Handler):
    def __init__(self, queue):
        super().__init__()
        self.queue = queue

    def emit(self, record):
        record.pathname = os.path.abspath(record.pathname)
        message = {
            'level': levels[record.levelno],
            'content': record.msg,
        }
        try:
            payload = json.dumps(message)
        except TypeError:
            message['content'] = repr(record.msg)
            payload = json.dumps(message)

        self.queue.put(payload)


JAVASCRIPT = """
console.log('Starting...');

const ws = new WebSocket("ws://{base}/__ws__");
ws.onmessage = function (event) {{
    const msg = JSON.parse(event.data);
    console[msg.level](msg.content);
}};
"""


class ConsoleLog:
    def __init__(self, app, logger, js_path='/__console__.js'):
        self.app = app
        self.queue = Queue()
        self.logger = logger
        self.js_path = js_path

        handler = DictHandler(self.queue)
        formatter = logging.Formatter(
            '[file://%(pathname)s:%(lineno)d] %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def __call__(self, environ, start_response):
        if environ.get('wsgi.websocket'):
            ws = environ["wsgi.websocket"]
            while not ws.closed:
                message = self.queue.get()
                ws.send(message)
                self.queue.task_done()
            return
        elif environ["PATH_INFO"] == self.js_path:
            if environ.get('HTTP_HOST'):
                base = environ['HTTP_HOST']
            else:
                host = environ['SERVER_NAME']
                port = environ['SERVER_PORT']
                base = ':'.join((host, port))
            response = Response(JAVASCRIPT.format(base=base))
            return response(environ, start_response)

        # request non-compressed response
        environ.pop('HTTP_ACCEPT_ENCODING', '')
        response = Response.from_app(self.app, environ)

        # inject JS
        if response.mimetype == 'text/html':
            response = self.inject(response)

        # compress response, if necessary
        response = gzip()(response)

        return response(environ, start_response)

    def inject(self, response):
        code = '<script src="{}" async="async"></script>'.format(self.js_path)
        data = response.get_data()
        payload = data.decode(response.charset)
        response.data = '{code}\n{payload}'.format(code=code, payload=payload)

        return response

from collections import defaultdict
import json
import logging
import os.path

from werkzeug.wrappers import Response


# TODO:
# - use BeautifulSoup for injecting JS
# - work with streaming response


levels = {
    logging.CRITICAL: 'console.error',
    logging.ERROR: 'console.error',
    logging.WARNING: 'console.warn',
    logging.INFO: 'console.info',
    logging.DEBUG: 'console.debug',
    logging.NOTSET: 'console.log',
}


class DictHandler(logging.Handler):
    def __init__(self):
        super().__init__()
        self.messages = defaultdict(list)

    def emit(self, record):
        record.pathname = os.path.abspath(record.pathname)
        self.messages[record.levelno].append(self.format(record))


class ConsoleLog:
    def __init__(self, app, root):
        self.app = app

        self.handler = DictHandler()
        formatter = logging.Formatter(
            '[%(asctime)s] file://%(pathname)s:%(lineno)d: %(message)s')
        self.handler.setFormatter(formatter)
        root.addHandler(self.handler)

    def __call__(self, environ, start_response):
        response = Response.from_app(self.app, environ)
        if response.mimetype == 'text/html':
            response = self.inject(response)
        return response(environ, start_response)

    def inject(self, response):
        html = b''.join(response.response).decode(response.charset)

        messages = self.handler.messages.copy()
        self.handler.messages.clear()
        code = []
        for level, method in levels.items():
            if messages[level]:
                message = json.dumps('\n'.join(messages[level]))
                code.append(f'{method}({message});')

        if code:
            code = '\n'.join(code)
            html += f'<script>{code}</script>'

        response.data = html

        return response

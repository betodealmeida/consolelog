from collections import defaultdict
import gzip
from io import BytesIO
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


def gzip_response(response):
    gzip_buffer = BytesIO()
    gzip_file = gzip.GzipFile(mode='wb', fileobj=gzip_buffer)
    gzip_file.write(response.data)
    gzip_file.close()

    response.data = gzip_buffer.getvalue()
    response.headers['Content-Encoding'] = 'gzip'
    response.headers['Vary'] = 'Accept-Encoding'
    response.headers['Content-Length'] = len(response.data)

    return response


class ConsoleLog:
    def __init__(self, app, root):
        self.app = app

        self.handler = DictHandler()
        formatter = logging.Formatter(
            '[%(asctime)s] file://%(pathname)s:%(lineno)d: %(message)s')
        self.handler.setFormatter(formatter)
        root.addHandler(self.handler)

    def __call__(self, environ, start_response):
        # request non-compressed response
        http_accept_encoding = environ.pop('HTTP_ACCEPT_ENCODING', '')

        response = Response.from_app(self.app, environ)
        if response.mimetype == 'text/html':
            response = self.inject(response, script=True)
        elif response.mimetype == 'application/javascript':
            response = self.inject(response, script=False)

        # compress response?
        if 'gzip' in http_accept_encoding:
            response = gzip_response(response)

        return response(environ, start_response)

    def inject(self, response, script=True):
        data = response.get_data()
        payload = data.decode(response.charset)

        messages = self.handler.messages.copy()
        self.handler.messages.clear()
        code = []
        for level, method in levels.items():
            if messages[level]:
                message = json.dumps('\n'.join(messages[level]))
                code.append(f'{method}({message});')

        if code:
            code = '\n'.join(code)
            if script:
                response.data = f'{payload}\n<script>{code}</script>'
            else:
                response.data = f'{payload}\n{code}'

        return response

import html
import logging

from flask import Flask
from gevent import pywsgi
from geventwebsocket.handler import WebSocketHandler
import werkzeug.serving

from console_log import ConsoleLog

app = Flask(__name__)

logger = logging.getLogger('console')
logger.setLevel(logging.DEBUG)

with open(__file__) as f:
    source = '<pre>{}</pre>'.format(html.escape(f.read()))


@app.route("/")
def hello():
    logger.error('Error logged from Python')
    logger.warning('Warning logged from Python')
    logger.info('Info logged from Python')
    logger.debug('Debug logged from Python')
    logger.debug({'foo': ['bar', 'baz']})
    return source


app = ConsoleLog(app, logger)


@werkzeug.serving.run_with_reloader
def main():
    server = pywsgi.WSGIServer(("", 5000), app, handler_class=WebSocketHandler)
    server.serve_forever()


if __name__ == '__main__':
    main()

import html
import logging

from flask import Flask
import gevent
from gevent import pywsgi
from geventwebsocket.handler import WebSocketHandler
import werkzeug.serving

from console_log import ConsoleLog


app = Flask(__name__)

logger = logging.getLogger('console')
logger.setLevel(logging.DEBUG)


with open(__file__) as f:
    source = '<pre>{}</pre>'.format(html.escape(f.read()))


def ping():
    i = 0
    while True:
        logger.info(i)
        i += 1
        gevent.sleep(2)


@app.route("/")
def hello():
    logger.debug(app)
    logger.error('Error logged from Python')
    logger.warning('Warning logged from Python')
    logger.info('Info logged from Python')
    logger.debug('Debug logged from Python')
    logger.debug({'foo': ['bar', 'baz']})
    return source


app = ConsoleLog(app, logger)


def main():
    server = pywsgi.WSGIServer(("", 5000), app, handler_class=WebSocketHandler)
    gevent.joinall([
        gevent.spawn(server.start),
        gevent.spawn(ping),
    ])


if __name__ == '__main__':
    main()

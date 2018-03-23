import logging
import threading
import time

from flask import Flask
from gevent import pywsgi
from gevent import monkey
from geventwebsocket.handler import WebSocketHandler
import werkzeug.serving

from console_log import ConsoleLog

monkey.patch_all()

app = Flask(__name__)

logger = logging.getLogger('console')
logger.setLevel(logging.DEBUG)


def ping():
    i = 0
    while True:
        logger.info(i)
        i += 1
        time.sleep(2)


t = threading.Thread(target=ping)
t.setDaemon(True)
t.start()


@app.route("/")
def hello():
    logger.error('Error logged from Python')
    logger.warning('Warning logged from Python')
    logger.info('Info logged from Python')
    logger.debug('Debug logged from Python')
    return "Hello World!"


app = ConsoleLog(app, logger)


@werkzeug.serving.run_with_reloader
def main():
    server = pywsgi.WSGIServer(("", 5000), app, handler_class=WebSocketHandler)
    server.serve_forever()


if __name__ == '__main__':
    main()

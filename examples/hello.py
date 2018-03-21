import logging

from flask import Flask
from werkzeug.serving import run_simple

from console_log import ConsoleLog


app = Flask(__name__)

logger = logging.getLogger('console')
logger.setLevel(logging.DEBUG)


@app.route("/")
def hello():
    logger.error('Error logged from Python')
    logger.warning('Warning logged from Python')
    logger.info('Info logged from Python')
    logger.debug('Debug logged from Python')
    return "Hello World!"


app = ConsoleLog(app, logger)


if __name__ == '__main__':
    run_simple(
        'localhost',
        5000,
        app,
        use_reloader=True,
        use_debugger=True,
        use_evalex=True,
    )

console_log
===========

This module provides a WSGI middleware that allows you to log to the
browser console from Python:

.. code:: python

    import logging

    from flask import Flask

    from console_log import ConsoleLog

    console = logging.getLogger('console')
    console.setLevel(logging.DEBUG)

    app = Flask(__name__)

    @app.route('/')
    def hello():
        logger.error('Error logged from Python')
        logger.warning('Warning logged from Python')
        logger.info('Info logged from Python')
        logger.debug('Debug logged from Python')
        logger.debug({'foo': ['bar', 'baz']})
        return "Hello World!"

    app.wsgi_app = ConsoleLog(app.wsgi_app, console)

The logged messages will them show up in the browser console:

.. figure:: https://github.com/betodealmeida/consolelog/blob/master/docs/console_log.png
   :alt: Example showing messages in console

   Example showing messages in console

How it works
============

The new WSGI app does two things:

1. Creates a websocket backchannel.
2. Injects Javascript code into HTML responses, fetching data from the
   websocket channel and logging them to console.

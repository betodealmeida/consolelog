# console_log #

This module provides a WSGI middleware that allows you to log to the browser console from Python:

```python
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
    return "Hello World!"

app = ConsoleLog(app, console)
```

The logged messages will them show up in the browser console:

![Example showing messages in console](https://github.com/betodealmeida/consolelog/blob/master/docs/console_log.png)

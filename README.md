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
    console.error('Error logged from Python')
    console.debug('Debug logged from Python')

app = ConsoleLog(app, console)
```

The logged messages will them show up in the browser console.

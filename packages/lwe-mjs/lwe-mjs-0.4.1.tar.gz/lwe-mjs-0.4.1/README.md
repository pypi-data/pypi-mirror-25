mjs - Mapper JSON Server
========================
[![pypi](https://img.shields.io/pypi/v/lwe-mjs.svg)](https://pypi.python.org/pypi/lwe-mjs)

**mjs** is a simple server component which uses the [mapper project](https://github.com/linuxwhatelse/mapper) to run functions mapped to url patterns.

## Requirements
1. python 3.4 and up
2. [mapper.py](https://github.com/linuxwhatelse/mapper)

## Installation
Just run:
```bash
pip install lwe-mjs
```

## Usage
It's pretty straight forward...
```python
import mjs
import mapper

mpr = mapper.Mapper()

def validator(path, headers):
    # Would verify if the request is allowed or not
    return True

# Map "/index" to the index function.
#
# To see how the mapper works and what it can do, head over to
# https://github.com/linuxwhatelse/mapper
@mpr.url('^/index/$', 'GET')
def index():
    # When using mjs, your functions response HAS to look like this!
    return {
        # (Required) Status-Code to be sent to the client
        'status_code' : 200,

        # (Optional) Alternative message to be sent to the client
        'message' : 'Success',

        # (Optional) A cookie to be sent to the client.
        # e.g. http.cookies.SimpleCookie()
        'cookie' : None,

        # (Optional) Payload/Body to be sent to the client
        # Has to be of type dict or list
        'payload' : None
    }

if __name__ == '__main__':
    # Create a default configuration
    conf = mjs.Config()

    # Who is allowed to access the server
    conf.address = '0.0.0.0'

    # The port to be used with the server
    conf.port = 8088

    # A callback to be called for EVERY request (GET, POST, PUT, DELETE)
    # BEFORE the resolved function will be run.
    #
    # This callback HAS to return either True (if the request is allowed), or
    # False (if the request should be denied)
    #
    # Usefully to implement e.g. authentication
    conf.validate_callback = validator

    # A list of url-paths (without host:port) to be excluded from validation.
    conf.validate_exclude_paths = ['/login', '/register']

    # Create a new server instance
    server = mjs.Server(conf)
    # or
    server = mjs.ThreadedServer(conf)

    # Start the server
    print('Server running: %s:%s' % (conf.address, conf.port))
    print('use ctrl+c to exit')
    try:
        server.serve_forever()

    except KeyboardInterrupt:
        print('Server closed...')
```

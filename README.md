django-simple-response
======================

Return HTTP responses in a easier way


## Basic Usage

_settings.py_

```python
MIDDLEWARE_CLASSES = (
    ...
    # last on the list
    django_simple_response.middleware.SimpleResponseMiddleware,
)
```

Want more settings? go [here](docs/settings.md).

_views.py_

```python
def view(request):
    # return HTTP response with status code 200 (default)
    return

def another_view(request):
    # return HTTP response with content and status code 401 
    return 401, 'Not authorized'

def yet_another_view(request):
    # return JSON/JSONP response with content and default status code
    return {'foo': 'bar'}
```

In a nutshell, you can either return: 

- an object, which will be serialized into the response's content.
- a tuple, which first element defines the status code and the second the content of the response.

Want to know more? go [here](docs/serialization.md).

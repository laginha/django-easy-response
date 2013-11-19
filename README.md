django-simple-response
======================

Return HTTP responses in a easier way


## Usage

_settings.py_

```python
MIDDLEWARE_CLASSES = (
    ...
    # last on the list
    django_simple_response.middleware.SimpleResponseMiddleware,
)
```

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

The following table records in order the serialized result for all the supported objects:

<table border="1">
    <tr>
        <th>Object Type</th>
        <th>Description</th>
    </tr>
    <tr>
        <td>HttpResponse</td>
        <td>Returns HttpResponse as it is</td>
    </tr>
    <tr>
        <td>None</td>
        <td>Returns HTTP-response (status code defaults to 200)</td>
    </tr>
    <tr>
        <td>int</td>
        <td>Returns HTTP-response with the int value as the status code</td>
    </tr>
    <tr>
        <td>bool</td>
        <td>Returns JSON-response with the bool value as content</td>
    </tr>
    <tr>
        <td>str</td>
        <td>Returns HTTP-response with the str value as content</td>
    </tr>
    <tr>
        <td>float</td>
        <td>Returns HTTP-response with the float value as content</td>
    </tr>
    <tr>
        <td>dict</td>
        <td>Returns JSON-response with the dict value as content</td>
    </tr>
    <tr>
        <td>list</td>
        <td>Returns JSON-response with the list value as content</td>
    </tr>
    <tr>
        <td>Geometry</td>
        <td>Returns GeoJSON-response with the geometry value as content</td>
    </tr>
    <tr>
        <td>ValuesQuerySet</td>
        <td>Returns JSON-response with the ValuesQuerySet items as content</td>
    </tr>
    <tr>
        <td>QuerySet</td>
        <td>Returns JSON-response with the QuerySet unicoded items as content</td>
    </tr>
    <tr>
        <td>Model Instance</td>
        <td>Returns JSON-response with the model instance's attribute dict as content</td>
    </tr>
    <tr>
        <td>file</td>
        <td>Returns a HTTP-response as file like object</td>
    </tr>
    <tr>
        <td>generator</td>
        <td>Returns JSON-response with the generator items as content</td>
    </tr>
    <tr>
        <td>iterator</td>
        <td>Returns JSON-response with the iterator items as content</td>
    </tr>
    <tr>
        <td>Any other object</td>
        <td>Returns HTTP-response with unicoded value of the object as content</td>
    </tr>
</table>

# Serialization

<table border="0">
    <tr>
        <th>Object</th>
        <th>Response</th>
        <th>Attribute</th>
    </tr>
    <tr>
        <td>HttpResponse</td>
        <td>HTTP-Response</td>
        <td> - </td>
    </tr>
    <tr>
        <td>None</td>
        <td>HTTP-response</td>
        <td> - </td>
    </tr>
    <tr>
        <td>int</td>
        <td>HTTP-response</td>
        <td>status code</td>
    </tr>
    <tr>
        <td>bool</td>
        <td>JSON-response</td>
        <td>content</td>
    </tr>
    <tr>
        <td>str</td>
        <td>HTTP-response</td>
        <td>content</td>
    </tr>
    <tr>
        <td>str ending with '.html'</td>
        <td>HTTP-response</td>
        <td>template name</td>
    </tr>
    <tr>
        <td>float</td>
        <td>HTTP-response</td>
        <td>content</td>
    </tr>
    <tr>
        <td>dict</td>
        <td>JSON-response</td>
        <td>content</td>
    </tr>
    <tr>
        <td>list</td>
        <td>JSON-response</td>
        <td>content</td>
    </tr>
    <tr>
        <td>Geometry</td>
        <td>GeoJSON-response</td>
        <td>content</td>
    </tr>
    <tr>
        <td>ValuesQuerySet</td>
        <td>JSON-response</td>
        <td>content</td>
    </tr>
    <tr>
        <td>QuerySet</td>
        <td>JSON-response</td>
        <td>content</td>
    </tr>
    <tr>
        <td>RelatedManager</td>
        <td>JSON-response</td>
        <td>content</td>
    </tr>
    <tr>
        <td>Model Instance</td>
        <td>JSON-response</td>
        <td>content</td>
    </tr>
    <tr>
        <td>file</td>
        <td>File-response</td>
        <td>content</td>
    </tr>
    <tr>
        <td>generator</td>
        <td>JSON-response</td>
        <td>content</td>
    </tr>
    <tr>
        <td>iterator</td>
        <td>JSON-response</td>
        <td>content</td>
    </tr>
    <tr>
        <td>Any other object</td>
        <td>HTTP-response</td>
        <td>content</td>
    </tr>
</table>


## Examples

### Basic

```python
def view(request):
    return 401
```

```python
def view(request):
    return 401, 'Not authorized'
```

```python
def view(request):
    return {'foo': 'bar'}
```

### Return model related resources

```python
def view(request):
    return SomeModel.objects.all()
```

```python
def view(request):
    return SomeModel.objects.get(pk=1)
```

```python
def view(request):
    return SomeModel.objects.values()
```

### Return a template

```python
def view(request):
    return "template_name.html"
```

```python
def view(request):
    return "template_name.html", {'foo': 'bar'}
```

```python
def view(request):
    return 401, "template_name.html", {'foo': 'bar'}
```

The example above is the only case that view can return a tuple with 3 elements.

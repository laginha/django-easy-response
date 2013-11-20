# Settings

## DEFAULT_STATUS\_CODE

Default status code for the response, when not given explicitly. Defaults to `200`.

```python
DEFAULT_STATUS_CODE = 400
```

## CAREFUL_SERIALIZATION

Check and serialize each item of the iterable returned object (e.g. list and dict). Defaults to `True`.

```python
def view(request):
    return ['foo', date.today()]
```

If `CAREFUL_SERIALIZATION` is not set to true, the view above will raise an error, because the item Date object is not serializable.

However, if your views return simple serializable objects 

```python
def view(request):
    return ['foo', 'bar']
```

`CAREFUL_SERIALIZATION` is not needed. Set it to `False` which might improve your response time.

```python
CAREFUL_SERIALIZATION = False
```

## IN_DEPTH\_SERIALIZATION

Check and serialize in depth each item of the iterable returned object (e.g. list and dict). Defaults to `True`.

```python
def view(request):
    return [{
        'foo': date.today()
    }]

def view(request):
    return [{
        'foo': ['bar', date.today()]
    }]
```

If `IN_DEPTH_SERIALIZATION` is not set to true, the view above will raise an error, because the Date object within the item is not serializable. 

However, if your views return simple serializable objects 

```python
def view(request):
    return [{'foo': 'bar'}]
```

`IN_DEPTH_SERIALIZATION` is not needed. Set it to `False` which might improve your response time.

```python
IN_DEPTH_SERIALIZATION = False
```

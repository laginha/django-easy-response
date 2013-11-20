# Settings

## DEFAULT_STATUS\_CODE

Default status code for the response, when not given explicitly. Defaults to `200`.

```python
DEFAULT_STATUS_CODE = 400
```

## CAREFUL_SERIALIZATION

Check and serialize each item of the iterable returned object (e.g. list and dict). Defaults to `False`.

```python
def view(request):
    # if CAREFUL_SERIALIZATION not set to true, this will raise an error
    # because the item Date object is not serializable
    return [date.today()]
```

```python
CAREFUL_SERIALIZATION = True
```

## SMART_SERIALIZATION

Check and serialize in depth each item of the iterable returned object (e.g. list and dict). Defaults to `False`.

```python
def view(request):
    # if SMART_SERIALIZATION not set to true, this will raise an error
    # because, altough dict is serializable, the object Date within the item is not
    return [{'today': date.today()}]
```

```python
SMART_SERIALIZATION = True
```

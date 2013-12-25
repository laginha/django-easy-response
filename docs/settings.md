# Settings

## DEFAULT_STATUS\_CODE

Default status code for the response, when not given explicitly. 

Defaults to `200`.

```python
DEFAULT_STATUS_CODE = 400
```


## BASIC\_SERIALIZATION

Unicodes unserializable objects if set to `True` (e.g. `ValuesSet`, `QuerySet`). Otherwise inspects objects for deeper serialization. 

Defaults to `False`.

```python
BASIC_SERIALIZATION = True
```

#### Example

```python
def view(request):
    return User.objects.filter(username='bar')
```

If `BASIC_SERIALIZATION` set to `True`:

```python
'bar'
```

If `BASIC_SERIALIZATION` set to `False`:

```python
{
    'id': 1,
    'username': 'bar',
    ...
}
```

from .utils.process import to_http
from .consts import BASIC_SERIALIZATION

def serialization(basic=BASIC_SERIALIZATION):
    def decorator(view):
        def wrapper(request, *args, **kwargs):
            response = view(request, *args, **kwargs)
            return to_http(request, response, basic_serialization=basic)
        return wrapper
    return decorator


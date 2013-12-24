from .utils.process import to_http
from .consts import CAREFUL_SERIALIZATION, IN_DEPTH_SERIALIZATION

def serialization(careful=CAREFUL_SERIALIZATION, in_depth=IN_DEPTH_SERIALIZATION):
    def decorator(view):
        def wrapper(request, *args, **kwargs):
            response = view(request, *args, **kwargs)
            return to_http(request, response, 
                careful_serialization=careful,
                in_depth_serialization=in_depth)
        return wrapper
    return decorator

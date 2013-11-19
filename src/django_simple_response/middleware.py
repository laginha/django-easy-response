from .http import to_http
from .utils import is_tuple
from .consts import DEFAULT_STATUS_CODE


class SimpleResponseMiddleware(object):
    def process_view(self, request, view, args, kwargs):
        response = view(request, *args, **kwargs)
        if is_tuple(response):
            status, response = response
        else:
            status = DEFAULT_STATUS_CODE
        return to_http(request, response, status)

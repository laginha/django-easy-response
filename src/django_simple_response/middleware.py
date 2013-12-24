from .utils.process import to_http

class SimpleResponseMiddleware(object):
    def process_view(self, request, view, args, kwargs):
        response = view(request, *args, **kwargs)
        return to_http( request, response )

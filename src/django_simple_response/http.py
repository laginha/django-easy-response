import simplejson, mimetypes
from django.conf import settings
from django.http import HttpResponse
from .consts import IN_DEBUG_MODE
from .utils.functions import *
from .utils.serialize import *


class FileResponse(HttpResponse):
    """
    Http Response with file content
    """
    def __init__(self, content='', status=None, filename=None):
        content_type = mimetypes.guess_type(content.name)[0]
        filename = filename or content.name
        HttpResponse.__init__(self, content      = content, 
                                    status       = status, 
                                    content_type = content_type,)
        self['Content-Disposition'] = 'attachment; filename=' + filename


class JSONResponse(HttpResponse):
    """
    Http Response with Json content type
    """
    def __init__(self, content='', status=None):
        content_type = 'application/json; charset=utf-8'
        content = simplejson.dumps( content, ensure_ascii=False )
        HttpResponse.__init__(self, content      = content, 
                                    status       = status, 
                                    content_type = content_type,)


class JSONPResponse(HttpResponse):
    """
    Http Response with Jsonp content type
    """
    def __init__(self, content='', status=None, callback='callback'):
        content_type = 'application/javascript; charset=utf-8'
        json_content = simplejson.dumps( content, ensure_ascii=False )
        content = "%s(%s)" %(callback, json_content)
        HttpResponse.__init__(self, content      = content,
                                    status       = status, 
                                    content_type = content_type,)


class _DebugResponse(HttpResponse):
    """
    Json Response for debug purposes (django-debug-toolbar)
    """
    def __call__(self, content='', status=None, context=None):
        content = simplejson.dumps( content, ensure_ascii=False )
        return HttpResponse(content = self.__to_html(content),
                            status  = status, )

    def __to_html(self, content):
        TAG = settings.DEBUG_TOOLBAR_CONFIG.get('TAG', 'body') 
        return "<%s>%s</%s>" %(TAG, content, TAG)


class _JsonResponse(type):
    """
    HTTP Response context-dependent for Json or Jsonp content type
    """
    def __call__(self, content='', status=None, context=None):
        callback = context.GET.get('callback', None) if context else None
        if callback:
            return JSONPResponse(content, status, callback)
        return JSONResponse(content, status)


class JsonResponse(HttpResponse):
    __metaclass__ = _DebugResponse if IN_DEBUG_MODE else _JsonResponse


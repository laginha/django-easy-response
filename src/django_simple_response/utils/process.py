from django_simple_response.consts import DEFAULT_STATUS_CODE, BASIC_SERIALIZATION
from django_simple_response.http import HttpResponse, JsonResponse, FileResponse
from django_simple_response.utils import *


def to_http(request, response, status=DEFAULT_STATUS_CODE, basic_serialization=BASIC_SERIALIZATION):

    def http_response(content, ststus):
        return HttpResponse(content, status=status)

    def json_response(content, ststus):
        return JsonResponse(content, status=status, basic=basic_serialization, context=request)
        
    def file_response(content, status):
        return FileResponse(content, status=status) 

    if is_int(response) and not is_bool(response):
        return HttpResponse(status=response)
    if is_tuple(response):
        status, content = response
    else:
        content = response
    
    if is_httpresponse(content):
        return content
    elif is_file(content):
        return file_response( content, status )
    elif is_bool(content) or is_dict(content) or is_list(content) or \
         is_geo_value(content) or is_valuesset(content) or is_queryset(content) or \
         is_modelinstance(content) or is_related_manager(content) or \
         is_generator(content) or is_iter(content):
        return json_response( content, status )
    elif is_none(content) or is_str(content) or is_int(content) or is_float(content):
        return http_response( content, status )
    else:
        return http_response( unicode(content), status )

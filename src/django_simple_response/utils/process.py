from django_simple_response.utils import *
from django_simple_response.consts import *
from django_simple_response.http import *


def to_http(request, response, status=DEFAULT_STATUS_CODE,
careful_serialization=CAREFUL_SERIALIZATION,
in_depth_serialization=IN_DEPTH_SERIALIZATION):

    def http_response(content, ststus):
        return HttpResponse(content, status=status)

    def json_response(content, ststus):
        return JsonResponse(content, status=status, context=request)
        
    def file_response(content, status):
        return FileResponse(content, status=status) 
    
    def handle_geo(content, status):
        return json_response( content.geojson, status )
    
    def handle_valuesset(content, status):
        if in_depth_serialization:
            content = serialize_valuesset_in_depth( content )
        else:
            content = serialize_valuesset( content )
        return json_response( content, status )
        
    def handle_queryset(content, status):
        if in_depth_serialization:
            content = serialize_queryset_in_depth( content )
        else:
            content = serialize_queryset( content )
        return json_response( content, status )
    
    def handle_model_instance(content, status):
        if in_depth_serialization:
            content = serialize_model_instance_in_depth( content )
        else:
            content = serialize_model_instance( content )
        return json_response( content, status )
    
    def handle_related_manager(content, status):
        return handle_queryset( content.all(), status )
    
    def handle_generator(content, status):
        if careful_serialization:
            if in_depth_serialization:
                content = serialize_list_in_depth(content)
            else:
                content = serialize_list(content)
        else:
            content = [i for i in content]
        return json_response( content, status )
    
    def handle_dict(content, status):
        if careful_serialization:
            if in_depth_serialization:
                content = serialize_dict_in_depth(content)
            else:
                content = serialize_dict(content)
        return json_response( content, status )
        
    def handle_list(content, status):
        if careful_serialization:
            if in_depth_serialization:
                content = serialize_list_in_depth(content)
            else:
                content = serialize_list(content)
        return json_response( content, status )

    if is_int(response) and not is_bool(response):
        return HttpResponse(status=response)
    if is_tuple(response):
        status, content = response
    else:
        content = response
    
    if is_httpresponse(content):
        return content
    elif is_bool(content):
        return json_response( content, status )
    elif is_none(content) or is_str(content) or is_int(content) or is_float(content):
        return http_response( content, status )
    elif is_dict(content):
        return handle_dict( content, status )
    elif is_list(content):
        return handle_list( content, status )
    elif is_geo_value(content):
        return handle_geo( content, status )
    elif is_valuesset(content):
        return handle_valuesset( content, status )
    elif is_queryset(content):
        return handle_queryset( content, status )
    elif is_modelinstance(content):
        return handle_model_instance( content, status )
    elif is_related_manager(content):
        return handle_related_manager( content, status )
    elif is_file(content):
        return file_response( content, status )
    elif is_generator(content) or is_iter(content):
        return handle_generator( content, status )
    else:
        return http_response( unicode(content), status )

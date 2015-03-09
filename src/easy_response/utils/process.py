from django.shortcuts import render
from easy_response.consts import DEFAULT_STATUS_CODE, BASIC_SERIALIZATION
from easy_response.http import HttpResponse, JsonResponse, FileResponse
from easy_response.utils import is_int, is_tuple, is_float, is_file,\
    is_http_response, is_none, is_int, is_str


class MalformedResponse(Exception):
    pass


def to_http(request, response, status=DEFAULT_STATUS_CODE, basic_serialization=BASIC_SERIALIZATION):
    if is_int(response):
        return HttpResponse(status=response)
    if is_tuple(response):
        if len(response) == 3:
            status, template, dictionary = response
            return render(request, template, dictionary=dictionary, status=status)
        elif len(response) == 2:
            if is_str(response[0]) and response[0].endswith('.html'):
                status, template = response
                return render(request, template, status=status)
            status, content = response
        else:
            raise MalformedResponse("View can only return a `tuple` with 2 or 3 elements.")
    else:
        content = response
    
    if is_http_response(content):
        return content
    elif is_file(content):
        return FileResponse(content, status=status) 
    elif is_str(content):
        if content.endswith('.html'):
            return render(request, content, status=status)
        return HttpResponse(content, status=status)
    elif is_none(content):
        return HttpResponse(status=status)
    elif is_int(content) or is_float(content):
        return HttpResponse(content, status=status)
    return JsonResponse(content, status=status, basic=basic_serialization, context=request)

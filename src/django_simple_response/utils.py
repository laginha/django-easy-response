from django.db.models.query import QuerySet, ValuesQuerySet
from django.db import models
from django.http import HttpResponse
from types import NoneType
from inspect import isgenerator, isgeneratorfunction
from .consts import SMART_SERIALIZATION

try:
    from django.contrib.gis.geos import GEOSGeometry
    is_geodj_project = True
except ImportError:
    import sys
    sys.stdout.write("Warning: Could not find the GEOS library.\n")
    is_geodj_project = False


is_serializable  = lambda x: isinstance(x, (int,str,bool,unicode,float,list,dict,NoneType))
is_basic         = lambda x: isinstance(x, (int,str,bool,unicode,float,NoneType))
is_float         = lambda x: isinstance(x, float)
is_int           = lambda x: isinstance(x, int)
is_str           = lambda x: isinstance(x, str)
is_unicode       = lambda x: isinstance(x, unicode)
is_tuple         = lambda x: isinstance(x, tuple)
is_dict          = lambda x: isinstance(x, dict)
is_list          = lambda x: isinstance(x, list)
is_file          = lambda x: isinstance(x, file)
is_iter          = lambda x: hasattr(x, '__iter__')
is_generator     = lambda x: isgenerator(x) or isgeneratorfunction(x)
is_geo_value     = lambda x: is_geodj_project and isinstance(x, GEOSGeometry)

is_queryset      = lambda x: isinstance(x, QuerySet)
is_valuesset     = lambda x: isinstance(x, ValuesQuerySet)
is_modelinstance = lambda x: isinstance(x, models.Model)
is_httpresponse  = lambda x: isinstance(x, HttpResponse)
is_related_manager = lambda x: all(i in str(type(x)) for i in ["django.", "Related"])


def basic_serialize(x):
    if is_serializable(x):
        return x
    return unicode(x)

def smart_serialize(x): 
    if is_basic(x):
        return x
    if is_dict(x):
        return serialize_dict( x )
    if is_list(x) or is_tuple(x) or is_generator(x):
        return serialize_list( x )
    if is_geo_value(x):
        return x.geojson  
    if is_modelinstance(x):
        return serialize_model_instance(x)
    if is_queryset(x):
        return serialize_queryset( x )
    if is_valuesset(x):
        return serialize_valuesset( x )
    if is_related_manager(x):
        return serialize_related_manager( x )
    if is_iter(x):
        return serialize_list( x )
    return unicode(x)

serialize = smart_serialize if SMART_SERIALIZATION else basic_serialize
    
serialize_dict            = lambda x: {k:serialize(v) for k,v in x.iteritems()}
serialize_list            = lambda x: [serialize(x) for i in x]
serialize_queryset        = lambda x: [unicode(i) for i in x]
serialize_valuesset       = lambda x: [serialize_dict(i) for i in x]
serialize_related_manager = lambda x: [serialize(i) for i in x.all()]
serialize_model_instance  = lambda x: {f.name: serialize(getattr(x, f.name)) for f in x._meta.fields}

from django_simple_response.consts import IN_DEPTH_SERIALIZATION
from django_simple_response.utils import *

def serialize(value):
    if is_serializable(value):
        return value
    return unicode(value)

def serialize_in_depth(value): 
    if is_basic(value):
        return value
    if is_dict(value):
        return serialize_dict_in_depth(value)
    if is_list(value) or is_tuple(value) or is_generator(value):
        return serialize_list_in_depth(value)
    if is_geo_value(value):
        return x.geojson  
    if is_modelinstance(value):
        return serialize_model_instance_in_depth(value)
    if is_queryset(value):
        return serialize_queryset_in_depth(value)
    if is_valuesset(value):
        return serialize_valuesset_in_depth(value)
    if is_related_manager(value):
        return serialize_related_manager_in_depth(value)
    if is_iter(value):
        return serialize_list_in_depth(value)
    return unicode(value)


serialize_dict = lambda x: {k:serialize(v) for k,v in x.iteritems()}
serialize_dict_in_depth = lambda x: {k:serialize_in_depth(v) for k,v in x.iteritems()}

serialize_list = lambda x: [serialize(i) for i in x]
serialize_list_in_depth = lambda x: [serialize_in_depth(i) for i in x]

# import simplejson
# serialize_queryset = lambda x: simplejson.dumps(x, default=lambda y: unicode(y))
serialize_queryset = lambda x: [unicode(i) for i in x]
serialize_queryset_in_depth = serialize_queryset

serialize_valuesset = lambda x: [serialize_dict(i) for i in x]
serialize_valuesset_in_depth = lambda x: [serialize_dict_in_depth(i) for i in x]

serialize_related_manager = lambda x: [serialize(i) for i in x.all()]
serialize_related_manager_in_depth = lambda x: [serialize_in_depth(i) for i in x.all()]

serialize_model_instance = lambda x: {f.name: serialize(getattr(x, f.name)) for f in x._meta.fields}
serialize_model_instance_in_depth = lambda x: {f.name: serialize(getattr(x, f.name)) for f in x._meta.fields}

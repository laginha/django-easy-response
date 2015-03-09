from easy_response.utils import is_geo_value, is_model_instance, is_valuesset
from easy_response.utils import is_related_manager, is_queryset, is_iter, is_generator

def basic_serialization(value):
    try:
        return unicode(value)
    except StopIteration:
        return repr(value)
    
def careful_serialization(value):
    if is_geo_value(value):
        return value.geojson  
    if is_model_instance(value):
        return {f.name: getattr(value, f.name) for f in value._meta.fields}
    if is_valuesset(value):
        return [dict(i) for i in value]
    if is_related_manager(value):
        return [i for i in value.all()]
    if is_iter(value): # or is_queryset or is_generator
        return [i for i in value]
    return unicode(value)

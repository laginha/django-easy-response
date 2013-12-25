from django_simple_response.utils import is_geo_value, is_modelinstance, is_valuesset
from django_simple_response.utils import is_related_manager, is_queryset, is_iter, is_generator

def basic_serialization(value):
    return unicode(value)
    
def careful_serialization(value):
    if is_geo_value(value):
        return value.geojson  
    if is_modelinstance(value):
        return {f.name: getattr(value, f.name) for f in value._meta.fields}
    if is_valuesset(value):
        return [dict(i) for i in value]
    if is_related_manager(value):
        return [i for i in value.all()]
    if is_queryset(value) or is_iter(value) or is_generator(value):
        return [i for i in value]
    return unicode(value)

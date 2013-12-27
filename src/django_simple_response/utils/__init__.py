from django.db.models.query import QuerySet, ValuesQuerySet
from django.db import models
from django.http import HttpResponse
from types import NoneType
from inspect import isgenerator, isgeneratorfunction

try:
    from django.contrib.gis.geos import GEOSGeometry
    is_geodj_project = True
except ImportError:
    import sys
    sys.stdout.write("Warning: Could not find the GEOS library.\n")
    is_geodj_project = False

is_float        = lambda x: isinstance(x, float)
is_int          = lambda x: isinstance(x, int) and not isinstance(x, bool)
is_str          = lambda x: isinstance(x, str)
is_unicode      = lambda x: isinstance(x, unicode)
is_tuple        = lambda x: isinstance(x, tuple)
is_dict         = lambda x: isinstance(x, dict)
is_list         = lambda x: isinstance(x, list)
is_bool         = lambda x: isinstance(x, bool)
is_file         = lambda x: isinstance(x, file)
is_none         = lambda x: isinstance(x, NoneType)
is_iter         = lambda x: hasattr(x, '__iter__')
is_generator    = lambda x: isgenerator(x) or isgeneratorfunction(x)
is_geo_value    = lambda x: is_geodj_project and isinstance(x, GEOSGeometry)

is_queryset        = lambda x: isinstance(x, QuerySet)
is_valuesset       = lambda x: isinstance(x, ValuesQuerySet)
is_model_instance  = lambda x: isinstance(x, models.Model)
is_http_response   = lambda x: isinstance(x, HttpResponse)
is_related_manager = lambda x: all(i in str(type(x)) for i in ["django.", "Related"])

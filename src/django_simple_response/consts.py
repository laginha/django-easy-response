from django.conf import settings

DEFAULT_STATUS_CODE    = getattr(settings, 'DEFAULT_STATUS_CODE', 200)
IN_DEPTH_SERIALIZATION = getattr(settings, 'IN_DEPTH_SERIALIZATION', True)
CAREFUL_SERIALIZATION  = getattr(settings, 'CAREFUL_SERIALIZATION', True) 
CAREFUL_SERIALIZATION  = CAREFUL_SERIALIZATION or IN_DEPTH_SERIALIZATION

IN_DEBUG_MODE = getattr(settings, 'DEBUG', False) and\
                'debug_toolbar' in settings.INSTALLED_APPS and\
                hasattr(settings, 'DEBUG_TOOLBAR_CONFIG')

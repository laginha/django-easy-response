from django.conf import settings

DEFAULT_STATUS_CODE   = getattr(settings, 'DEFAULT_STATUS_CODE', 200)
CAREFUL_SERIALIZATION = getattr(settings, 'DEEP_SERIALIZATION', False)
SMART_SERIALIZATION   = getattr(settings, 'SMART_SERIALIZATION', False)

IN_DEBUG_MODE = getattr(settings, 'DEBUG', False) and\
                getattr(settings, 'YARD_DEBUG_MODE', False) and\
                'debug_toolbar' in settings.INSTALLED_APPS and\
                hasattr(settings, 'DEBUG_TOOLBAR_CONFIG')

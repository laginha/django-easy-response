from django.conf import settings

DEFAULT_STATUS_CODE = getattr(settings, 'DEFAULT_STATUS_CODE', 200)
BASIC_SERIALIZATION = getattr(settings, 'BASIC_SERIALIZATION', False)

IN_DEBUG_MODE = getattr(settings, 'DEBUG', False) and\
                'debug_toolbar' in settings.INSTALLED_APPS and\
                hasattr(settings, 'DEBUG_TOOLBAR_CONFIG')

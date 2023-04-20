from .base import *

DEBUG = True

ALLOWED_HOSTS = []
CORS_ORIGIN_ALLOW_ALL = True

DATABASES = {
    'default': {
        'NAME': 'eroshiku_db',
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'USER': 'postgres',
        'PASSWORD': 'postgres'
    },
}

SITE_ID = 1

DEBUG_TOOLBAR_PANELS = [
    'debug_toolbar.panels.versions.VersionsPanel',
    'debug_toolbar.panels.timer.TimerPanel',
    'debug_toolbar.panels.settings.SettingsPanel',
    'debug_toolbar.panels.headers.HeadersPanel',
    'debug_toolbar.panels.request.RequestPanel',
    'debug_toolbar.panels.sql.SQLPanel',
    'debug_toolbar.panels.staticfiles.StaticFilesPanel',
    'debug_toolbar.panels.templates.TemplatesPanel',
    'debug_toolbar.panels.cache.CachePanel',
    'debug_toolbar.panels.signals.SignalsPanel',
    'debug_toolbar.panels.logging.LoggingPanel',
    'debug_toolbar.panels.redirects.RedirectsPanel',
]

DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False,
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
        'json': {
            'format': '{ "loggerName":"%(name)s", "timestamp":"%(asctime)s", "fileName":"%(filename)s", "logRecordCreationTime":"%(created)f", '
                      '"functionName":"%(funcName)s", "levelNo":"%(levelno)s", "lineNo":"%(lineno)d", "time":"%(msecs)d", "levelName":"%(levelname)s", "message":"%(message)s"}',
        },
    },
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        }
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'sql.file': {
            'level': 'DEBUG',
            'class': 'common.logging.Utf8FileHandler',
            'filename': ROOT_DIR / 'log/sql.log',
        },
        'error.file': {
            'level': 'ERROR',
            'class': 'common.logging.Utf8FileHandler',
            'filename': ROOT_DIR / 'log/error.log',
        },
    },
    'loggers': {
        'django.db.backends': {
            'level': 'DEBUG',
            # 'handlers': ['console'],
            'handlers': ['sql.file', ],
        },
        'default': {
            'level': 'DEBUG',
            # 'handlers': ['console', 'loggly', ]
            'handlers': ['console', 'error.file']
        },
    }
}

STATICFILES_DIRS = (
    ROOT_DIR / 'staticfiles',
)

MEDIAFILES_DIRS = (
    ROOT_DIR / 'media',
)

EMAIL_HOST = "smtp.yandex.com"
EMAIL_PORT = 465
EMAIL_HOST_USER = "test-st0re@yandex.ru"
EMAIL_HOST_PASSWORD = "netfprmcgalvfkuh"
EMAIL_USE_SSL = True


# REDIS related settings
REDIS_HOST = 'localhost'
REDIS_PORT = '6379'
BROKER_URL = 'redis://' + REDIS_HOST + ':' + REDIS_PORT + '/0'
BROKER_TRANSPORT_OPTIONS = {'visibility_timeout': 3600}
CELERY_RESULT_BACKEND = 'redis://' + REDIS_HOST + ':' + REDIS_PORT + '/0'

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': ROOT_DIR.parent / 'cache' / 'default',
        'TIMEOUT': 60 * 60 * 24 * 6,
    },
}

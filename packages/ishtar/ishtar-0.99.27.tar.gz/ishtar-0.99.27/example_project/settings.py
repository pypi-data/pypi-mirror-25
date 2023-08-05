#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Django settings for ishtar project.

import os
import sys

DEBUG = False
DEBUG_TOOLBAR = False
TEMPLATE_DEBUG = DEBUG
SQL_DEBUG = False
DJANGO_EXTENSIONS = False
USE_SPATIALITE_FOR_TESTS = True

if "test" in sys.argv:
    sys.path.insert(0, '..')

IMAGE_MAX_SIZE = (1024, 768)
THUMB_MAX_SIZE = (300, 300)

CACHE_SMALLTIMEOUT = 60
CACHE_TIMEOUT = 3600
CACHE_BACKEND = 'memcached://127.0.0.1:11211/'

SEP = os.path.sep
ROOT_PATH = SEP.join(
    os.path.abspath(__file__).split(SEP)[:-1]) + SEP
STATIC_URL = '/static/'
STATIC_ROOT = ROOT_PATH + 'static/'
BASE_URL = "/"
URL_PATH = ""
EXTRA_VERSION = 'git'

ODT_TEMPLATE = ROOT_PATH + "../ishtar_common/static/template.odt"

LOGIN_REDIRECT_URL = "/" + URL_PATH

AUTH_PROFILE_MODULE = 'ishtar_common.IshtarUser'
ACCOUNT_ACTIVATION_DAYS = 7

# change this in local_settings
DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'ishtar',
        'USER': 'ishtar',
        'PASSWORD': 'ishtar',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/Paris'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'fr-fr'

COUNTRY = "fr"

OOOK_DATE_FORMAT = u"%-d %B %Y"
OOO_DATE_FORMAT = u"%-d %B %Y"
DATE_FORMAT = u"%-d %B %Y"

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True
LANGUAGES = (
    ('fr', u'Français'),
    ('en', u'English'),
)
DEFAULT_LANGUAGE = 1

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = ROOT_PATH + 'media/'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/media/'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    # 'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = [
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.locale.LocaleMiddleware',
]

TEMPLATE_CONTEXT_PROCESSORS = (
    'ishtar_common.context_processors.get_base_context',
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.request",
)

ROOT_URLCONF = 'example_project.urls'

TEMPLATE_DIRS = (
    ROOT_PATH + 'templates',
)

AUTHENTICATION_BACKENDS = (
    'ishtar_common.backend.ObjectPermBackend',
)

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.admin',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.gis',
    'django.contrib.staticfiles',
    'django.contrib.formtools',
    'django.contrib.messages',
    'django.contrib.humanize',
    'south',
    'registration',
    # 'geodjangofla',
    'ishtar_pdl',
    'ishtar_common',
    'archaeological_files_pdl',
    'archaeological_files',
    'archaeological_operations',
    'archaeological_context_records',
    'archaeological_warehouse',
    'archaeological_finds',
    # 'debug_toolbar',
]

LOGFILE = ''

default_handler = {
    'handlers': ['logfile'],
    'level': 'INFO',
    'propogate': False
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        # Include the default Django email handler for errors
        # This is what you'd get without configuring logging at all.
        'mail_admins': {
            'class': 'django.utils.log.AdminEmailHandler',
            'level': 'ERROR',
            # But the emails are plain text by default - HTML is nicer
            'include_html': True,
        },
        # Log to a text file that can be rotated by logrotate
        'logfile': {
            'class': 'logging.handlers.WatchedFileHandler',
            'filename': '/var/log/django/ishtar.log'
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins', 'logfile'],
            'level': 'ERROR',
            'propagate': True,
        },
        'django': {
            'handlers': ['logfile'],
            'level': 'ERROR',
            'propagate': False,
        },
        'ishtar_pdl': default_handler,
        'ishtar_common': default_handler,
        'archaeological_files_pdl': default_handler,
        'archaeological_files': default_handler,
        'archaeological_operations': default_handler,
        'archaeological_context_records': default_handler,
        'archaeological_warehouse': default_handler,
        'archaeological_finds': default_handler,
    },
}

# Ishtar custom
SRID = 27572
ENCODING = 'windows-1252'
ALT_ENCODING = 'ISO-8859-15'
APP_NAME = "SRA - Pays de la Loire"
SURFACE_UNIT = 'square-metre'
SURFACE_UNIT_LABEL = u'm²'
JOINT = u" | "
# dir for ishtar maintenance script - as it can be a serious security issue if
# not managed cautiously the dir contening theses scripts is not set by default
ISHTAR_SCRIPT_DIR = ""

ISHTAR_FILE_PREFIX = u""
ISHTAR_OPE_PREFIX = u"OA"
ISHTAR_DEF_OPE_PREFIX = u"OP"
# string len of find indexes - i.e: find with index 42 will be 00042
ISHTAR_FINDS_INDEX_ZERO_LEN = 5
ISHTAR_OPE_COL_FORMAT = None
# DB key: (txt_idx, label)
ISHTAR_OPE_TYPES = {}
# DB key: txt_idx
ISHTAR_PERIODS = {}
ISHTAR_PERMIT_TYPES = {}
ISHTAR_DOC_TYPES = {u"undefined": u"Undefined"}


ISHTAR_DPTS = []

PRE_APPS = []
EXTRA_APPS = []

TEST_RUNNER = 'ishtar_common.tests.ManagedModelTestRunner'

try:
    from local_settings import *
except ImportError, e:
    print('Unable to load local_settings.py:', e)

TESTING = sys.argv[1:2] == ['test']

if TESTING:
    SOUTH_TESTS_MIGRATE = False

    if USE_SPATIALITE_FOR_TESTS:
        DATABASES['default']['ENGINE'] = \
            'django.contrib.gis.db.backends.spatialite'

PROJECT_SLUG = locals().get('PROJECT_SLUG', 'default')

if LOGFILE:
    LOGGING['handlers']['logfile']['filename'] = LOGFILE
else:
    LOGGING['handlers']['logfile']['filename'] = \
        '/var/log/django/ishtar-' + PROJECT_SLUG + '.log'

INTERNAL_IPS = ('127.0.0.1',)

JQUERY_URL = STATIC_URL + "js/jquery.min.js"
JQUERY_UI_URL = STATIC_URL + "js/jquery-ui/"

if DEBUG:
    # make all loggers use the console
    for logger in LOGGING['loggers']:
        LOGGING['loggers'][logger]['handlers'] += ['console']

if DJANGO_EXTENSIONS:
    INSTALLED_APPS.append('django_extensions')

if DEBUG_TOOLBAR:
    if '..' not in sys.path:
        sys.path.insert(0, '..')
    global DEBUG_TOOLBAR_PANELS
    global DEBUG_TOOLBAR_CONFIG
    MIDDLEWARE_CLASSES += ['debug_toolbar.middleware.DebugToolbarMiddleware']
    INSTALLED_APPS += ['debug_toolbar']
    DEBUG_TOOLBAR_PANELS = (
        'debug_toolbar.panels.version.VersionDebugPanel',
        'debug_toolbar.panels.timer.TimerDebugPanel',
        'debug_toolbar.panels.settings_vars.SettingsVarsDebugPanel',
        'debug_toolbar.panels.headers.HeaderDebugPanel',
        'debug_toolbar.panels.request_vars.RequestVarsDebugPanel',
        'debug_toolbar.panels.template.TemplateDebugPanel',
        'debug_toolbar.panels.sql.SQLDebugPanel',
        'debug_toolbar.panels.signals.SignalDebugPanel',
        'debug_toolbar.panels.logger.LoggingPanel',
    )
    DEBUG_TOOLBAR_CONFIG = {'INTERCEPT_REDIRECTS': False}


if SQL_DEBUG:
    LOGGING['loggers']['django.db.backends'] = {
        'level': 'DEBUG',
        'handlers': ['console'],
    }

if 'test' in sys.argv:
    PROJECT_SLUG += "-test"

#!/usr/bin/env python
# -*- coding: utf-8 -*-

# rename this file to local_settings.py and overload settings in this file

ISHTAR_SCRIPT_DIR = "/home/etienne/Work/ishtar-project/ishtar/admin_scripts"

DEBUG = True
DEBUG_TOOLBAR = True
DEBUG_TOOLBAR = False
TEMPLATE_DEBUG = DEBUG
SQL_DEBUG = True
SQL_DEBUG = False
DJANGO_EXTENSIONS = True
USE_SPATIALITE_FOR_TESTS = False

# SITE_ID = 3

POSTGIS_VERSION = (2, 1, 4)

# Make this string unique, and don't share it with anybody.
SECRET_KEY = ''

ADMINS = (
    ('Nim', 'etienne.loks@peacefrogs.net'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'ishtar',
        'USER': 'postgres',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}

ISHTAR_DPTS = [
    ('44', u"Loire-Atlantique"),
    ('49', u"Maine-et-Loire"),
    ('53', u"Mayenne"),
    ('72', u"Sarthe"),
    ('85', u"Vendée")
]

ROOT_URLCONF = 'example_project.urls'
# MEDIA_URL = 'http://localhost/ishtar/static/'

BASE_URL = 'http://localhost/'

# choose the extensions to install
EXTRA_APPS = [
    'django_extensions',
    'archaeological_files',
    'archaeological_context_records',
    'archaeological_warehouse',
    'archaeological_finds',
    'django_extensions'
]

PRE_APPS = ['ishtar_pdl']

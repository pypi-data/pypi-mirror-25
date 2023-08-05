# -*- encoding:utf-8 -*-
import os
import logging
import copy
from django.utils.log import DEFAULT_LOGGING

APP_NAME = "MY APP"

AUTHOR = "ADMIN"

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = 'YOUR SECRET KEY'

DEBUG = True

ALLOW_HOSTS = ("127.0.0.1",)

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

MEDIA_ROOT = os.path.join(BASE_DIR, "upload")
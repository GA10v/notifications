"""Django settings for admin_panel project."""

import os
from pathlib import Path

from split_settings.tools import include

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = os.getenv('SECRET_KEY')
DEBUG = os.environ.get('DEBUG', False) == 'True'
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '127.0.0.1').split(',')
include('components/_apps_middleware.py')
ROOT_URLCONF = 'admin_panel.urls'
WSGI_APPLICATION = 'admin_panel.wsgi.application'
include('components/_templates.py')
include('components/_database.py')
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]
include('components/_localization.py')
STATIC_URL = 'static/'
STATIC_ROOT = '/code/static/'
MEDIA_URL = 'media/'
MEDIA_ROOT = '/code/media/'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
AUTH_USER_MODEL = 'users.User'
CELERY_BROKER_URL = os.getenv('RABBITMQ_URL')
CELERY_RESULT_BACKEND = 'rpc://'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_IMPORTS = ('notifications.tasks',)

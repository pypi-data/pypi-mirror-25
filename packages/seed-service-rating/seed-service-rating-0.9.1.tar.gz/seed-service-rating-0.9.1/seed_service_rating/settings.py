"""
Django settings for seed_service_rating project.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os

import dj_database_url
import djcelery
from kombu import Exchange, Queue

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', 'REPLACEME')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG', False)

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = (
    # admin
    'django.contrib.admin',
    # core
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # documentation
    'rest_framework_docs',
    # 3rd party
    'djcelery',
    'raven.contrib.django.raven_compat',
    'rest_framework',
    'rest_framework.authtoken',
    'django_filters',
    'rest_hooks',
    # us
    'ratings',

)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'seed_service_rating.urls'

WSGI_APPLICATION = 'seed_service_rating.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': dj_database_url.config(
        default=os.environ.get(
            'SERVICE_RATING_DATABASE',
            'postgres://postgres:@localhost/seed_service_rating')),
}


# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-gb'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django.contrib.staticfiles.finders.FileSystemFinder',
)

STATIC_ROOT = 'static'
STATIC_URL = '/static/'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates')
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# Sentry configuration
RAVEN_CONFIG = {
    # DevOps will supply you with this.
    'dsn': os.environ.get('SERVICE_RATING_SENTRY_DSN', None),
}

# REST Framework conf defaults
REST_FRAMEWORK = {
    'PAGE_SIZE': 1000,
    'DEFAULT_PAGINATION_CLASS':
        'rest_framework.pagination.LimitOffsetPagination',
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_FILTER_BACKENDS': ('rest_framework.filters.DjangoFilterBackend',)
}

# Webhook event definition
HOOK_EVENTS = {
    # 'any.event.name': 'App.Model.Action' (created/updated/deleted)
    'rating.added': 'ratings.Rating.created+',
    'invite.added': 'ratings.Invite.created+'
}

HOOK_DELIVERER = 'ratings.tasks.deliver_hook_wrapper'

HOOK_AUTH_TOKEN = os.environ.get('HOOK_AUTH_TOKEN', 'REPLACEME')

# Celery configuration options
CELERY_RESULT_BACKEND = 'djcelery.backends.database:DatabaseBackend'
CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler'

BROKER_URL = os.environ.get('BROKER_URL', 'redis://localhost:6379/0')

CELERY_DEFAULT_QUEUE = 'seed_service_rating'
CELERY_QUEUES = (
    Queue('seed_service_rating',
          Exchange('seed_service_rating'),
          routing_key='seed_service_rating'),
)

CELERY_ALWAYS_EAGER = False

# Tell Celery where to find the tasks
CELERY_IMPORTS = (
    'ratings.tasks',
)

CELERY_CREATE_MISSING_QUEUES = True
CELERY_ROUTES = {
    'celery.backend_cleanup': {
        'queue': 'mediumpriority',
    },
    'ratings.tasks.send_invite_messages': {
        'queue': 'priority',
    },
    'ratings.tasks.send_invite_message': {
        'queue': 'priority',
    },
    'ratings.tasks.post_send_update_invite': {
        'queue': 'priority',
    },
    'ratings.tasks.deliver_hook_wrapper': {
        'queue': 'priority',
    },
}

CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT = ['json']

djcelery.setup_loader()

TOTAL_INVITES_TO_SEND = int(os.environ.get('TOTAL_INVITES_TO_SEND', '2'))
DAYS_BETWEEN_INVITES = int(os.environ.get('DAYS_BETWEEN_INVITES', '7'))
INVITE_TEXT = os.environ.get(
    'INVITE_TEXT',
    'Thank you for registering. We can only improve if we get your feedback. '
    'Please dial *134*550*4# to rate the service you received at the clinic '
    'you registered at')
MESSAGE_SENDER_URL = os.environ.get('MESSAGE_SENDER_URL',
                                    'http://ms/api/v1')
MESSAGE_SENDER_TOKEN = os.environ.get('MESSAGE_SENDER_TOKEN',
                                      'REPLACEME')
IDENTITY_STORE_URL = os.environ.get('IDENTITY_STORE_URL',
                                    'http://is/api/v1')
IDENTITY_STORE_TOKEN = os.environ.get('IDENTITY_STORE_TOKEN',
                                      'REPLACEME')

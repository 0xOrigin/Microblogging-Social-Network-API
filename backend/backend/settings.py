"""
Django settings for backend project.

Generated by 'django-admin startproject' using Django 4.2.11.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""
import os
import sys
import psycopg2.extensions
import environ
import logging
from pathlib import Path
from datetime import timedelta
from corsheaders.defaults import default_headers, default_methods
from django.utils.translation import gettext_lazy as _
from django.conf import settings

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Read .env file
environ.Env.read_env(BASE_DIR.parent / '.env.backend.dev', overwrite=True)
environ.Env.read_env(BASE_DIR.parent / '.env', overwrite=True)
env = environ.Env()


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env.str('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool('DEBUG', default=False)


# Allowed hosts & IP addresses

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=['*'])

INTERNAL_IPS = env.list('INTERNAL_IPS', default=['127.0.0.1',])

DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': lambda request: settings.DEBUG,
}

ALLOW_DJANGO_DEBUG_TOOLBAR = env.bool('ALLOW_DJANGO_DEBUG_TOOLBAR', default=False)


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'corsheaders',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',
    'rest_framework.authtoken',
    'django_filters',
    'django_cleanup.apps.CleanupConfig',
    'drf_spectacular',
    'core.apps.CoreConfig',
    # new applications.
    'iam.apps.IamConfig',
]

if DEBUG and ALLOW_DJANGO_DEBUG_TOOLBAR:
    INSTALLED_APPS.append('debug_toolbar') # Django Debug Toolbar


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware', # CORS
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'backend.middlewares.JWTCookieAuthenticationMiddleware', # JWT Middleware
    'backend.middlewares.ExceptionMiddleware', # Exception Middleware
    'django.middleware.gzip.GZipMiddleware', # GZip Compression
]

if DEBUG and ALLOW_DJANGO_DEBUG_TOOLBAR:
    MIDDLEWARE.append('debug_toolbar.middleware.DebugToolbarMiddleware') # Django Debug Toolbar


ROOT_URLCONF = 'backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [ BASE_DIR / 'emails_template'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.template.context_processors.i18n', # Django Internationalization
                'django.template.context_processors.media', # Media
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


ASGI_APPLICATION = 'backend.asgi.application'

WSGI_APPLICATION = 'backend.wsgi.application'

APPEND_SLASH = env.bool('APPEND_SLASH', default=False)


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': env.str('POSTGRES_ENGINE', default='django.db.backends.sqlite3'),
        'HOST': env.str('POSTGRES_HOST', default='localhost'),
        'PORT': env.str('POSTGRES_PORT', default='5432'),
        'USER': env.str('POSTGRES_USER', default='user'),
        'PASSWORD': env.str('POSTGRES_PASSWORD', default='password'),
        'NAME': env.str('POSTGRES_DB', default='db.sqlite3'),
        'CHARSET': env.str('POSTGRES_CHARSET', default='utf8'),
        'TIME_ZONE': env.str('POSTGRES_TIME_ZONE', default='UTC'),
        'CONN_HEALTH_CHECKS': env.bool('CONN_HEALTH_CHECKS', default=True),
        # 'CONN_MAX_AGE': env.int('CONN_MAX_AGE', default=0), # Comment this line if you want to use dj_db_conn_pool engine
        'POOL_OPTIONS': {
            'POOL_SIZE': env.int('POSTGRES_POOL_SIZE', default=10),
            'MAX_OVERFLOW': env.int('POSTGRES_POOL_MAX_OVERFLOW', default=20),
            'RECYCLE': env.int('POSTGRES_POOL_RECYCLE', default=3600),
            'TIMEOUT': env.int('POSTGRES_POOL_TIMEOUT', default=30),
        },
        'OPTIONS': {
            'isolation_level': psycopg2.extensions.ISOLATION_LEVEL_READ_COMMITTED if env.str(
                'POSTGRES_ENGINE', default='django.db.backends.sqlite3') != 'django.db.backends.sqlite3' else None,
            'sslmode': env.str('POSTGRES_SSLMODE', default='disable'),
        }
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 8,
        },
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
    {
        'NAME': 'iam.validators.StrongPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

LANGUAGES = [
    ('en', _('English')),
]

LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale/'),
]

TIME_ZONE = env.str('TIME_ZONE', default='UTC')

USE_I18N = True

USE_TZ = env.bool('USE_TZ', default=True)


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = env.str('STATIC_URL', default='/static/')

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles/')

MEDIA_URL = env.str('MEDIA_URL', default='/media/')

MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')


# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Logging Configurations

logging.basicConfig(stream=sys.stdout, level=logging.INFO)


# REST Framework Configurations

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'iam.authentication.JWTCookieAuthentication',
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'core.renderers.BaseJSONRenderer',
        'core.renderers.BaseBrowsableAPIRenderer',
        'rest_framework.renderers.JSONRenderer',
    ),
    'NON_FIELD_ERRORS_KEY': 'non-field-errors',
    'DEFAULT_PAGINATION_CLASS': 'core.paginations.BasePagination',
    'PAGE_SIZE': env.int('PAGE_SIZE', default=10),
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

if DEBUG:
    REST_FRAMEWORK['DEFAULT_AUTHENTICATION_CLASSES'] += ('rest_framework.authentication.SessionAuthentication',) # For DRF Browsable API only


# Pagination Configurations

PAGINATION_PAGE_SIZE = 10
PAGINATION_MAX_PAGE_SIZE = 100
PAGINATION_ADMIN_PAGE_SIZE = 50


# Security Configurations

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_HSTS_SECONDS = env.int('SECURE_HSTS_SECONDS', default=0)
SECURE_HSTS_INCLUDE_SUBDOMAINS = env.bool('SECURE_HSTS_INCLUDE_SUBDOMAINS', default=False)

SECURE_SSL_REDIRECT = env.bool('SECURE_SSL_REDIRECT', default=False)
SESSION_COOKIE_SECURE = env.bool('SESSION_COOKIE_SECURE', default=False)

CSRF_COOKIE_SECURE = env.bool('CSRF_COOKIE_SECURE', default=False)
CSRF_TRUSTED_ORIGINS = env.list('CSRF_TRUSTED_ORIGINS', default=[])


# CORS Configurations

CORS_ALLOWED_ORIGINS = env.list('CORS_ALLOWED_ORIGINS', default=[])
CORS_ORIGIN_WHITELIST = env.list('CORS_ORIGIN_WHITELIST', default=[])
CORS_ALLOW_CREDENTIALS = env.bool('CORS_ALLOW_CREDENTIALS', default=True)
CORS_ALLOW_HEADERS = list(default_headers) + env.list('CORS_ALLOW_HEADERS', default=[])
CORS_ALLOW_METHODS = list(default_methods) + env.list('CORS_ALLOW_METHODS', default=[])


# JWT Authentication Configurations

SIMPLE_JWT = {
    'AUTH_HEADER_TYPES': ('Bearer',),
    'ACCESS_TOKEN_LIFETIME': timedelta(days=1), # Just for testing purposes, should be 5 minutes in production
    'REFRESH_TOKEN_LIFETIME': timedelta(days=15), # Just for testing purposes
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': True,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'JWT_CLAIM': 'jti',
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_OBTAIN_SERIALIZER': 'iam.serializers.BaseTokenObtainPairSerializer',
    'TOKEN_REFRESH_SERIALIZER': 'iam.serializers.CookieTokenRefreshSerializer',
}


JWT_AUTH_ACCESS_COOKIE_NAME = env.str('JWT_AUTH_ACCESS_COOKIE_NAME', default='access_token')
JWT_AUTH_ACCESS_COOKIE_PATH = env.str('JWT_AUTH_ACCESS_COOKIE_PATH', default='/')

JWT_AUTH_REFRESH_COOKIE_NAME = env.str('JWT_AUTH_REFRESH_COOKIE_NAME', default='refresh_token')
JWT_AUTH_REFRESH_COOKIE_PATH = env.str('JWT_AUTH_REFRESH_COOKIE_PATH', default='/')

JWT_AUTH_COOKIE_HTTPONLY = env.bool('JWT_AUTH_ACCESS_COOKIE_HTTPONLY', default=True)
JWT_AUTH_COOKIE_SECURE = env.bool('JWT_AUTH_ACCESS_COOKIE_SECURE', default=False)
JWT_AUTH_COOKIE_SAMESITE = env.str('JWT_AUTH_ACCESS_COOKIE_SAMESITE', default='Lax')


# Email Configurations

IS_SEND_EMAIL_ENABLED = env.bool('IS_SEND_EMAIL_ENABLED', default=True)
EMAIL_BACKEND = env.str('EMAIL_BACKEND', default='django.core.mail.backends.smtp.EmailBackend')
EMAIL_HOST = env.str('EMAIL_HOST', default='smtp.gmail.com')
EMAIL_PORT = env.int('EMAIL_PORT', default=587)
EMAIL_USE_TLS = env.bool('EMAIL_USE_TLS', default=True)
EMAIL_TIMEOUT = env.int('EMAIL_TIMEOUT', default=10) # In seconds
EMAIL_HOST_NAME = env.str('EMAIL_HOST_NAME', default='Propyz')
EMAIL_HOST_USER = env.str('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = env.str('EMAIL_HOST_PASSWORD', default='')
EMAIL_SUBJECT_PREFIX = env.str('EMAIL_SUBJECT_PREFIX', default='Propyz')
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# Miscellaneous Configurations

AUTH_USER_MODEL = 'iam.User'
ALLOW_POST_MIGRATE_SEEDERS = env.bool('ALLOW_POST_MIGRATE_SEEDERS', default=True)


# Swagger Configurations

SPECTACULAR_SETTINGS = {
    'TITLE': 'Microblogging App API',
    'DESCRIPTION': 'Microblogging application',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    'COMPONENT_SPLIT_REQUEST': True,
}


# Redis Configurations

REDIS_HOST = env.str('REDIS_HOST', default='localhost')
REDIS_PORT = env.int('REDIS_PORT', default=6379)
REDIS_DB = env.int('REDIS_DB', default=0)
REDIS_PASSWORD = env.str('REDIS_PASSWORD', default=None)


# Celery Configuration

CELERY_ENABLE_UTC = env.bool('CELERY_ENABLE_UTC', default=False)
CELERY_TIMEZONE = env.str('CELERY_TIMEZONE', default='Asia/Dubai')
CELERY_BROKER_URL = env.str('CELERY_BROKER_URL', default='redis://localhost:6379/0')
CELERY_RESULT_BACKEND = env.str('CELERY_RESULT_BACKEND', default='redis://localhost:6379/0')
BROKER_CONNECTION_RETRY = env.bool('BROKER_CONNECTION_RETRY', default=True)
BROKER_CONNECTION_MAX_RETRIES = env.int('BROKER_CONNECTION_MAX_RETRIES', default=5)
BROKER_CONNECTION_TIMEOUT = env.int('BROKER_CONNECTION_TIMEOUT', default=30)
CELERY_ACCEPT_CONTENT = {'application/json', 'application/x-python-serialize'}
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_SERIALIZER = 'json'


# Redis Cache Configurations

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}",
    }
}

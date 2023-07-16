from os import getenv
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()
BASE_DIR = Path(__file__).resolve().parent.parent

ENV = getenv('ENV', 'PROD')
IS_DEV = ENV == 'DEV'
IS_PROD = ENV == 'PROD'
DEBUG = IS_DEV
APPEND_SLASH = False

APP_DOMAINS = getenv('APP_DOMAINS', '127.0.0.1,localhost').split(',')
APP_URLS = getenv('APP_URLS', 'http://127.0.0.1,http://localhost').split(',')
AUTH_USER_MODEL = 'authentication.User'

# Application definition

DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

INTERNAL_APPS = [
    'apps.authentication',
    'apps.news',
]

THIRD_PARTY_APPS = [
    'django_extensions',
]

INSTALLED_APPS = [
    'jazzmin',  # This app must be before django.contrib.admin
    *DJANGO_APPS,
    *INTERNAL_APPS,
    *THIRD_PARTY_APPS
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'configuration.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'configuration.wsgi.application'

# Database

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Cache
ENABLE_CACHE = bool(int(getenv('ENABLE_CACHE', '0')))
MEMCACHED_LOCATION = getenv('MEMCACHED_LOCATION', None)

if not ENABLE_CACHE:
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
        }
    }
elif MEMCACHED_LOCATION:
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.memcached.PyMemcacheCache',
            'LOCATION': MEMCACHED_LOCATION,
        }
    }
else:
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
            'LOCATION': 'unique-snowflake',
        }
    }

# Security

ALLOWED_HOSTS = APP_DOMAINS
SECRET_KEY = getenv('SECRET_KEY', 'django-insecure-je5fqjrctl0_*z1fvxk_^7h0ol7kki*o9tsgo%-zb&b+a)%jdp')

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

# Logging

LOG_LEVEL = getenv('LOG_LEVEL', 'INFO')
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,

    'root': {
        'handlers': ['error_file', 'info_file', 'console'],
        'level': LOG_LEVEL,
        'propagate': True
    },

    'handlers': {
        'error_file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'error.log',
            'level': 'ERROR',
            'formatter': 'verbose',
            'maxBytes': 100 * 1024 * 1024  # 100MB
        },
        'info_file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'info.log',
            'level': 'INFO',
            'formatter': 'verbose',
            'maxBytes': 100 * 1024 * 1024  # 100MB
        },
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'DEBUG' if DEBUG else 'INFO',
            'formatter': 'simple'
        }
    },

    'formatters': {
        'verbose': {
            'format': '{levelname} - {asctime} - {name}:{lineno} - {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} - {asctime} - {message}',
            'style': '{',
        },
    },
    'filters': {
        'exclude_disallowed_host': {
            '()': 'django.utils.log.CallbackFilter',
            'callback': lambda record: not record.getMessage().startswith("Invalid HTTP_HOST header:"),
        },
    },
    'loggers': {
        'django.security.DisallowedHost': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
            'filters': ['exclude_disallowed_host'],
        },
    },
}

# Internationalization

LANGUAGE_CODE = 'ru'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'static'
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

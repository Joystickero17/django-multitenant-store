"""
Django settings for multistore project.

Generated by 'django-admin startproject' using Django 3.2.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

import os
from pathlib import Path
from django.utils.timezone import timedelta
from google.oauth2 import service_account

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

CORS_ORIGIN_ALLOW_ALL = True
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ["SECRET_KEY"]

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv("DEBUG", True)
ALLOWED_HOSTS = ["*"]


# Application definition

INSTALLED_APPS = [
    'daphne',
    'django.contrib.admin',
     'django.contrib.admindocs',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'storages',
    'cities_light',
    'drf_yasg',
    "rest_framework",
    'rest_framework_simplejwt',
    "jwtauth",
    "core",
    "corsheaders",
    'django_extensions',
    'store',
    "store_admin",
    'staticinline.apps.StaticInlineAppConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    "corsheaders.middleware.CorsMiddleware",
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'multistore.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'core.views.admin_view'
            ],
        },
    },
]

REDIS_HOST = os.getenv("REDIS_HOST","127.0.0.1")
REDIS_PORT = os.getenv("REDIS_PORT", 6380)
BROKER_URL = f"redis://{REDIS_HOST}:{REDIS_PORT}/"

# mysite/settings.py
# Daphne
ASGI_APPLICATION = "multistore.asgi.application"
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [(REDIS_HOST, 6380)],
        },
    },
}

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases
DATABASES = {}
if os.getenv("USE_POSTGRES"):
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': os.getenv("NAME_DB"),
            'USER': os.getenv("USER_DB"),
            'PASSWORD': os.getenv("PASSWORD_DB"),
            'HOST': os.getenv("HOST_DB"),
            'PORT': os.getenv("PORT_DB"),
            }
        }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = 'multistore'
AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}
AWS_LOCATION = 'static'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]
DEFAULT_FILE_STORAGE = 'multistore.storage_backends.MediaStorage'
if not DEBUG:
    STATICFILES_STORAGE = 'storages.backends.s3boto3.S3StaticStorage'
    STATIC_URL = 'https://%s/%s/' % (AWS_S3_CUSTOM_DOMAIN, AWS_LOCATION)
    STATIC_ROOT = os.path.join(BASE_DIR, 'static')
else:
    STATIC_URL = "/static/"

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = "core.user"



CORS_ORIGIN_WHITELIST = [
    "http://127.0.0.1"
]

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES":[
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    "DEFAULT_PAGINATION_CLASS": 'rest_framework.pagination.LimitOffsetPagination',
    "PAGE_SIZE": 30
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=7),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=14)
}

GRAPH_MODELS = {
  'all_applications': True,
  'group_models': True,
}
LANGUAGE_CODE = 'es'
LOGIN_URL = "/login/"

BASE_URL = os.getenv("BASE_URL", "http://127.0.0.1:8000")

# Integracion con paypal
PAYPAL_API = os.getenv("PAYPAL_SANDBOX_API") if DEBUG else os.getenv("PAYPAL_PRODUCTION_API")
PAYPAL_SECRET = os.getenv("PAYPAL_SECRET")
PAYPAL_CLIENT_ID = os.getenv("PAYPAL_CLIENT_ID")

# para solucionar el about blank blocked bug
SECURE_CROSS_ORIGIN_OPENER_POLICY='same-origin-allow-popups'

# Nombre de cada url de caso de pago en coinbase
# Se deben tomar a la hora de hacer las urls de redirecciones
# path(..., name=settings.COINBASE_SUCCESS_URL_NAME)
# path(..., name=settings.COINBASE_CANCELED_URL_NAME)
COINBASE_API_KEY = os.environ["COINBASE_API_KEY"]
COINBASE_SUCCESS_URL_NAME = os.getenv("COINBASE_SUCCESS_URL_NAME", "payment_success")
COINBASE_CANCELLED_URL_NAME = os.getenv("COINBASE_CANCELLED_URL_NAME", "payment_canceled")

# Django Cities Ligth
CITIES_LIGHT_INCLUDE_COUNTRIES = ['VE']

CSRF_TRUSTED_ORIGINS = [
    "http://127.0.0.1:8000/",
    "https://*.ngrok.io"
]

BASE_URL = os.getenv("BASE_URL", "http://127.0.0.1:8000/")

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True  
EMAIL_HOST = 'mail.privateemail.com'
EMAIL_PORT = 587  
EMAIL_HOST_USER = 'contacto@mlsparts.shop'  
EMAIL_HOST_PASSWORD = os.environ["EMAIL_HOST_PASSWORD"]

# link del admin en vue
ADMIN_VUE_URL = os.getenv("ADMIN_VUE_URL", "http://localhost:8080/")
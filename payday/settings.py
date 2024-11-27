"""
Django settings for payday project.

Generated by 'django-admin startproject' using Django 5.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from dotenv import load_dotenv
from pathlib import Path
import dj_database_url
import os

# Setting environment variables
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-06ypcma#qfpku2z89w08jpa0o%5uy9vwsq2@7i)ierd=!jf@+g"
SECRET_KEY = os.getenv('SECRET_KEY', SECRET_KEY)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = bool(int(os.getenv('DEBUG', 1)))

ALLOWED_HOSTS = list(os.getenv('ALLOWED_HOSTS', '*').split(','))

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.humanize",

    "storages",

    "dal",
    "dal_select2",
    "widget_tweaks",

    "tinymce",
    "mathfilters",
    "crispy_forms",
    "django_filters",
    "rest_framework",
    "crispy_bootstrap5",
    "django_json_widget",

    "djmoney",
    "qr_code",
    "django_ace",
    "phonenumber_field",
    "slick_reporting",
    "corsheaders",
    'django_extensions',

    "core",
    "api",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django_currentuser.middleware.ThreadLocalUserMiddleware",
    "core.middleware.organization.OrganizationMiddleware"
]

if DEBUG:
    INSTALLED_APPS += ["debug_toolbar"]
    MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]

ROOT_URLCONF = "payday.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": ['templates'],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "core.context.base"
            ],
        },
    },
]

WSGI_APPLICATION = "payday.wsgi.application"
ASGI_APPLICATION = "payday.asgi.application"

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASE_URL = 'sqlite:///db.sqlite3'
DATABASES = {'default': None}
TEST = {'NAME': DATABASE_URL}

# Default database
DEFAULT_DATABASE_URL = os.getenv('DATABASE_URL', default=DATABASE_URL)
DATABASES['default'] = dj_database_url.parse(DEFAULT_DATABASE_URL)

DATABASES['default']['TEST'] = TEST
CONN_MAX_AGE = int(os.getenv('CONN_MAX_AGE', 0))
DATABASES['default']['CONN_MAX_AGE'] = CONN_MAX_AGE

# Replica database
REPLICATED_DATABASE_URL = os.getenv('REPLICATED_DATABASE_URL', default=None)
if REPLICATED_DATABASE_URL:
    DATABASES['replica'] = dj_database_url.parse(REPLICATED_DATABASE_URL)
    DATABASES['replica']['CONN_MAX_AGE'] = CONN_MAX_AGE

    # Database router
    DATABASE_ROUTERS = ['payday.db_routers.PrimaryReplicaRouter']

print(DEFAULT_DATABASE_URL)

# Redis settings
REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379')
REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
REDIS_PORT = os.getenv('REDIS_PORT', 6379)


# Cache settings default memory and redis cache
CACHE_BACKEND = os.getenv('CACHE_BACKEND', 'django.core.cache.backends.dummy.DummyCache')
CACHE_LOCATION = os.getenv('CACHE_LOCATION',  '')

CACHES = {
    "default": {
        "LOCATION": CACHE_LOCATION,
        "BACKEND": CACHE_BACKEND,
    }
}

# Channels settings
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer"
    }
}

# Default user model and authentication
LOGIN_URL = os.getenv("LOGIN_URL", 'login')
AUTH_USER_MODEL = os.getenv("AUTH_USER_MODEL", 'core.user')
LOGOUT_REDIRECT_URL = os.getenv("LOGOUT_REDIRECT_URL", 'login')
LOGIN_REDIRECT_URL = os.getenv("LOGIN_REDIRECT_URL", 'core:home')


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = "fr"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

from storages.backends.s3boto3 import S3Boto3Storage

STATIC_URL = 'static/'
STATIC_URL = os.getenv("STATIC_URL", STATIC_URL)
# STATICFILES_DIRS =[os.path.join(BASE_DIR, 'static')]
STATIC_ROOT = os.getenv("STATIC_ROOT", STATIC_URL.replace('/', ''))

AWS_LOCATION = os.getenv('AWS_LOCATION', default='')
AWS_DEFAULT_ACL = os.getenv('AWS_DEFAULT_ACL', default='public-read')
AWS_QUERYSTRING_AUTH= os.getenv('AWS_QUERYSTRING_AUTH', default=False)

AWS_S3_REGION = os.getenv('AWS_S3_REGION')
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_S3_ENDPOINT_URL = os.getenv('AWS_S3_ENDPOINT_URL')
AWS_S3_CUSTOM_DOMAIN = os.getenv('AWS_S3_CUSTOM_DOMAIN')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_S3_OBJECT_PARAMETERS = {'CacheControl': 'max-age=86400'}
AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_STORAGE_BUCKET_NAME')
AWS_S3_SECURE_URLS = int(os.getenv('AWS_S3_SECURE', default=0))
AWS_S3_URL_PROTOCOL = os.getenv('AWS_S3_URL_PROTOCOL', default='http:')

DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'
DEFAULT_FILE_STORAGE = os.getenv('DEFAULT_FILE_STORAGE', default=DEFAULT_FILE_STORAGE)

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
STATICFILES_STORAGE = os.getenv("STATICFILES_STORAGE", STATICFILES_STORAGE)

MEDIA_ROOT = BASE_DIR / 'media'
MEDIA_URL = os.getenv("MEDIA_URL", 'media/')
PUBLIC_MEDIA_LOCATION = os.getenv('PUBLIC_MEDIA_LOCATION', default='media')

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Email settings
EMAIL_BACKEND = os.getenv('EMAIL_BACKEND', 'django.core.mail.backends.console.EmailBackend')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD', '')
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER', '')
EMAIL_USE_TLS = bool(int(os.getenv('EMAIL_USE_TLS', 0)))
EMAIL_USE_SSL = bool(int(os.getenv('EMAIL_USE_SSL', 0)))
EMAIL_HOST = os.getenv('EMAIL_HOST', 'localhost')
EMAIL_PORT = os.getenv('EMAIL_PORT', 1025)

# Django Rest Framework settings
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
}

# Django Crispy Forms settings
CRISPY_TEMPLATE_PACK = 'bootstrap5'
CRISPY_ALLOWED_TEMPLATE_PACKS = ['bootstrap', 'bootstrap5', 'uni_form']

# Django JSON Widget settings
JSON_WIDGET_CSS = 'https://cdnjs.cloudflare.com/ajax/libs/jsoneditor/9.0.0/jsoneditor.min.css'
JSON_WIDGET_JS = 'https://cdnjs.cloudflare.com/ajax/libs/jsoneditor/9.0.0/jsoneditor.min.js'

# Django Money settings
DEFAULT_CURRENCY = 'CDF'
CURRENCIES = ('USD', 'CDF')
CURRENCY_CHOICES = [(currency, currency) for currency in CURRENCIES]

# Django QR Code settings
QR_CODE_FOREGROUND = 'black'
QR_CODE_BACKGROUND = 'white'
QR_CODE_MODULE_SIZE = 5
QR_CODE_VERSION = 1
QR_CODE_ERROR_CORRECTION = 'L'
QR_CODE_IMAGE_FORMAT = 'PNG'
QR_CODE_CACHE_TIMEOUT = 3600
QR_CODE_CACHE_PREFIX = 'qr_code'

# Django Ace settings
ACE_DEFAULT_THEME = 'chrome'
ACE_DEFAULT_MODE = 'python'
ACE_DEFAULT_WIDTH = '100%'
ACE_DEFAULT_HEIGHT = '300px'

# Django Phonenumber Field settings
PHONENUMBER_DB_FORMAT = 'E164'
PHONENUMBER_DEFAULT_REGION = 'CD'

# Django TinyMCE settings
TINYMCE_DEFAULT_CONFIG = {
    'cleanup_on_startup': True,
    'custom_undo_redo_levels': 20,
    'theme': 'silver',
    'height': '600',
    'plugins': '''
            textcolor save link image media preview codesample contextmenu
            table code lists fullscreen  insertdatetime  nonbreaking
            contextmenu directionality searchreplace wordcount visualblocks
            visualchars code fullscreen autolink lists  charmap print  hr
            anchor pagebreak
            ''',
    'toolbar1': '''
            fullscreen preview bold italic underline | fontselect,
            fontsizeselect  | forecolor backcolor | alignleft alignright |
            aligncenter alignjustify | indent outdent | bullist numlist table |
            | link image media | codesample |
            ''',
    'toolbar2': '''
            visualblocks visualchars |
            charmap hr pagebreak nonbreaking anchor |  code |
            ''',
    'contextmenu': 'formats | link image',
    'menubar': True,
    'statusbar': True
}

# Django Select2 settings
SELECT2_JS = 'https://cdnjs.cloudflare.com/ajax/libs/select2/4.0.13/js/select2.min.js'
SELECT2_CSS = 'https://cdnjs.cloudflare.com/ajax/libs/select2/4.0.13/css/select2.min.css'
SELECT2_I18N = 'https://cdnjs.cloudflare.com/ajax/libs/select2/4.0.13/js/i18n/fr.js'

# Django Math Filters settings
MATHJAX = {
    'url': 'https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.9/MathJax.js',
    'config': 'TeX-AMS_HTML',
    'TeX': {'extensions': ['AMSmath.js', 'AMSsymbols.js']},
}

# Django Filters settings
FILTERS_HELP_TEXT_FILTER = False
FILTERS_HELP_TEXT_EXCLUDE = False

# Django Debug Toolbar settings
INTERNAL_IPS = [
    'localhost',
]

# Django Celery settings
CELERY_RESULT_EXTENDED = True
CELERY_CACHE_BACKEND='django-cache'
CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True
CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL', REDIS_URL)
CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND', REDIS_URL)
CELERY_BROKER_TRANSPORT_URL=os.getenv('CELERY_BROKER_TRANSPORT_URL', REDIS_URL)


# Sentry settings
SENTRY_DSN = "https://61630e2ac1f3c024ffa6a3d4a7207f57@o4505861077204992.ingest.us.sentry.io/4507582424612864"
SENTRY_DSN = os.getenv("SENTRY_DSN", SENTRY_DSN)

import sentry_sdk
sentry_sdk.init(dsn=SENTRY_DSN, traces_sample_rate=1.0, profiles_sample_rate=1.0,)

# cors header
CORS_ALLOW_ALL_ORIGINS = True
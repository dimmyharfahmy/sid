from pathlib import Path
import os
import sys
from django.conf import settings
import logging

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-n1z6eftvc(hkjpq4f!bt-)#wez7cx8438rd5*v2spb)g*u45by'
DEBUG = False
ALLOWED_HOSTS = ['sidfoundation.or.id', 'www.sidfoundation.or.id', '52.148.84.253']

# CSRF settings
CSRF_TRUSTED_ORIGINS = [
    'http://sidfoundation.or.id',
    'http://www.sidfoundation.or.id',
    'https://sidfoundation.or.id',
    'https://www.sidfoundation.or.id'
]

CSRF_COOKIE_DOMAIN = '.sidfoundation.or.id'
SESSION_COOKIE_DOMAIN = '.sidfoundation.or.id'
CSRF_COOKIE_SECURE = True  # Change to True if using HTTPS
SESSION_COOKIE_SECURE = True  # Change to True if using HTTPS
CSRF_COOKIE_HTTPONLY = True
CSRF_COOKIE_SAMESITE = 'Lax'  # or 'Strict' if appropriate

# Security settings
SECURE_CROSS_ORIGIN_OPENER_POLICY = 'same-origin'
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_SSL_REDIRECT = True  # Set to True if using HTTPS
X_FRAME_OPTIONS = 'DENY'

# Logging for CSRF
logger = logging.getLogger('django.security.csrf')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(BASE_DIR / 'csrf_debug.log')
handler.setLevel(logging.DEBUG)
logger.addHandler(handler)


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'debug.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}

IS_RUNNING_TESTS = len(sys.argv) > 1 and sys.argv[1] == 'test'

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    'myapp',
    'django_ckeditor_5',
    'django_extensions',
]

SITE_ID = 1

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
)

LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'logout'

STATIC_URL = '/static/'
# STATICFILES_DIRS = []
STATIC_ROOT = '/home/sidadmin/myproject/collected_static/'

MEDIA_URL = '/media/'
MEDIA_ROOT = '/home/sidadmin/myproject/media/'


# Contoh konfigurasi tambahan untuk CKEditor 5
DJANGO_CKEDITOR_5_FILE_STORAGE = "django_ckeditor_5.storage.FileSystemStorage"
CKEDITOR_5_ALLOW_ALL_FILE_TYPES = True
CKEDITOR_5_UPLOAD_FILE_TYPES = ['jpeg', 'jpg', 'pdf', 'png', 'gif'] # optional

CKEDITOR_5_CONFIGS = {
    'default': {
        'toolbar': {
            'items': [
                'heading', '|',
                'bold', 'italic', 'link', 'bulletedList', 'numberedList', 'blockQuote', '|',
                'imageUpload', 'mediaEmbed', 'insertTable', 'tableColumn', 'tableRow', 'mergeTableCells', '|',
                'undo', 'redo'
            ]
        },
        'image': {
            'toolbar': [
                'imageTextAlternative', 'imageStyle:full', 'imageStyle:side', '|',
                'resizeImage'
            ],
            'styles': [
                'full', 'side'
            ],
            'resizeUnit': '%',
            'resizeOptions': [
                {
                    'name': 'resizeImage:original',
                    'value': '',
                    'icon': 'original'
                },
                {
                    'name': 'resizeImage:25',
                    'value': '25',
                    'icon': 'small'
                },
                {
                    'name': 'resizeImage:50',
                    'value': '50',
                    'icon': 'medium'
                },
                {
                    'name': 'resizeImage:75',
                    'value': '75',
                    'icon': 'large'
                }
            ]
        },
        'table': {
            'contentToolbar': [
                'tableColumn', 'tableRow', 'mergeTableCells'
            ]
        },
        'language': 'en',
        'contentsCss': ['/static/myapp/css/style.css']
    }
}

def show_toolbar(request):
    if not settings.DEBUG:
        return False

    # Hide the toolbar by default
    if request.GET.get('djdt') == 'show':
        return True

    return False

DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': show_toolbar,
}

if not IS_RUNNING_TESTS:
    INSTALLED_APPS += [
        'debug_toolbar',
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

if not IS_RUNNING_TESTS:
    MIDDLEWARE += [
        'debug_toolbar.middleware.DebugToolbarMiddleware',
    ]

# DEBUG_TOOLBAR_CONFIG = {
#     'SHOW_TOOLBAR_CALLBACK': lambda request: DEBUG,
# }

INTERNAL_IPS = [
    '127.0.0.1', '52.148.84.253'
]

ROOT_URLCONF = 'myproject.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'myproject', 'templates')],
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

WSGI_APPLICATION = 'myproject.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'mydatabase',
        'USER': 'sidadmin',
        'PASSWORD': 'S1D4dm1n.123!',
        'HOST': 'localhost',
        'PORT': '5432',
        'TEST': {
            'NAME': 'test_my_database',
        },
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
    }
}


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

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

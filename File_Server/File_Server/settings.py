
from pathlib import Path
from decouple import config
import os

BASE_DIR = Path(__file__).resolve().parent.parent


SECRET_KEY = config('SECRET_KEY')


DEBUG = False

ALLOWED_HOSTS = ['127.0.0.1', ".vercel.app"]


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'files.apps.FilesConfig',
    'accounts.apps.AccountsConfig',
    'activity.apps.ActivityConfig',
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

ROOT_URLCONF = 'File_Server.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'File_Server/templates')],
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

WSGI_APPLICATION = 'File_Server.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': config("DEV_DATABASE_NAME"),
        'USER': config("DEV_DATABASE_USER"),
        'PASSWORD': config("DEV_DATABASE_PASSWORD"),
        'HOST': config("DEV_DATABASE_HOST"),
        'PORT': config("DEV_DATABASE_PORT"),
        'OPTIONS': {
            'sslmode': 'require',
        },
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
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_TZ = True


STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'File_Server/static/')
]

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR,'static')

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
#MEDIA_ROOT = os.path.join(BASE_DIR,'media')
#MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR,'media')
# MEDIA_URL = '/media/'
MEDIAFILES_LOCATION = 'media'

AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % config('AWS_STORAGE_BUCKET_NAME')


AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = config('AWS_STORAGE_BUCKET_NAME')
AWS_S3_SIGNATURE_NAME = config('AWS_S3_SIGNATURE_NAME')
AWS_S3_REGION_NAME = config('AWS_S3_REGION_NAME')
AWS_S3_FILE_OVERWRITE = config('AWS_S3_FILE_OVERWRITE', cast = bool)
AWS_DEFAULT_ACL =  None
AWS_S3_VERITY = config('AWS_S3_VERITY', cast=bool)
DEFAULT_FILE_STORAGE = config('DEFAULT_FILE_STORAGE')


MEDIA_URL = "https://%s/%s/" % (AWS_S3_CUSTOM_DOMAIN, MEDIAFILES_LOCATION)
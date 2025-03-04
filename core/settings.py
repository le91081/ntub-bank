"""
Django settings for core project.

Generated by 'django-admin startproject' using Django 2.1.5.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os
from . import secret
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'ttuv9pfyc1%wjy1l!42^7=uh(m@l^r0=jk@*eq2gc+x7yu17ud'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
USE_SQLITE = False

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'bootstrap4',
    'chartjs',
    'customer',
    'account',
    'staff',
    'api',
    'recognize',
    'transaction',
    'blacklist',
    'alertlog',
    'preset'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
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

WSGI_APPLICATION = 'core.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases
if USE_SQLITE:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': secret.DB['ENGINE'],
            'HOST': secret.DB['HOST'],
            'PORT': secret.DB['PORT'],
            'USER': secret.DB['USER'],
            'PASSWORD': secret.DB['PASSWORD'],
            'NAME': secret.DB['NAME'],
            'OPTIONS': {
                'driver': secret.DB['driver'],
            }
        }
    }


# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'zh-Hant'

TIME_ZONE = 'Asia/Taipei'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, 'assets')

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]

LOGIN_URL = '/login/'

LOGIN_REDIRECT_URL = '/'

LOGOUT_REDIRECT_URL = '/login/'

IMAGE_ROOT = os.path.join(BASE_DIR, 'images')
IMAGE_CUSTOMER_ROOT = os.path.join(BASE_DIR, 'images/customer')
IMAGE_UNKNOWN_ROOT = os.path.join(BASE_DIR, 'images/unknown')
IMAGE_BLACK_LIST_ROOT = os.path.join(BASE_DIR, 'images/black_list')

FAKE_DATA_DIR = os.path.join(BASE_DIR, 'fake_data')


# email
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = secret.EMAIL['USER']
EMAIL_HOST_PASSWORD = secret.EMAIL['PASSWORD']
EMAIL_USE_TLS = 'True'
EMAIL_POST = '587'

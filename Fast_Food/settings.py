"""
Django settings for mysite project.

Generated by 'django-admin startproject' using Django 3.0.5.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'lub6p8i@cl7b$a310&#_%j-@c50x92q@*bcdxzhk!h1hl-$2*t'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['127.0.0.1','food-mania-tayebur.herokuapp.com']

# Application definition

INSTALLED_APPS = [
    'account',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_cleanup',
    'crispy_forms',
    'food',
    'order',
]
CRISPY_TEMPLATE_PACK = 'bootstrap4'

AUTH_USER_MODEL = 'account.User'  # change from built-in user model to ours
# <app_name>.custom_model_name


# for capital or small letter email
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.AllowAllUsersModelBackend',
    'account.backends.CaseInsensitiveModelBackend',
)

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'Fast_Food.urls'  # Change project name

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates', # singular template ModuleNotFoundError: No module named 'django.templates'
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug', # singular template
                'django.template.context_processors.request', # singular template, # Dynamic back link
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',

            ],
        },
    },
]

WSGI_APPLICATION = 'Fast_Food.wsgi.application'  # Change project name

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/


MEDIA_URL = '/media/'  # to make a url
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
# This is where we are going to upload the pictures


STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
# Heroku runs collectstatic and puts all static files here

# point to static outside app directory
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]


STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = 'tayebur@canadaeducationbd.com'  # must have 'Less secure app access' turned on go to https://myaccount.google.com/u/1/security
EMAIL_HOST_PASSWORD = '687687687687'
DEFAULT_FROM_EMAIL = 'no-reply<no_reply@domain.com>'

# BASE_DIR = 'http://127.0.0.1:8000'

#
# CART_SESSION_ID = 'cart'

'''
create a repository 
Copy paste the code from the git page (similar to bottom and run in on git bash)
git remote add origin git@github.com:TayeburAH/food_website.git
git branch -M master
git push -u origin master
From Git Bash
fetch origin/master
merge origin
'''

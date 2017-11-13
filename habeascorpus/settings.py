# -*- coding: utf-8 -*-

"""
Django settings for habeascorpus project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Les fichiers .tsv, .mm, ... doivent se trouver dans le dossier courant
DATA_DIR = os.getcwd()


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the sdatabase directoryecret key used in production secret!
SECRET_KEY = '$7zi5j4_+^mx(r2zoi*5+$m(#jx$x@nr+9$vltvwb*%6$h$(2k'

# SECURITY WARNING: don't run with  debug turned on in production!
DEBUG = False
#DEBUG = True

TEMPLATE_DEBUG = False

ALLOWED_HOSTS = ['127.0.0.1', 'localhost']

STATIC_URL = '/static/'

# La racine de l'application qui consomme l'API
STATICFILES_DIRS = (
    os.path.join(os.path.join(BASE_DIR, 'browser'), 'app/'),
)

# Application definition

INSTALLED_APPS = (
    'django.contrib.contenttypes',
    'django.contrib.staticfiles',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',    
    'django.middleware.clickjacking.XFrameOptionsMiddleware',   
)

ROOT_URLCONF = 'habeascorpus.urls'

WSGI_APPLICATION = 'habeascorpus.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(DATA_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'fr'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Corpus
CORPUS_NAME = 'articles-fr'
METHOD = 'tfidf'
METHODS = {'tfidf' : 'tfidf', 'lda' :'lda100', 'lsi': 'lsi100' }
DATA_DIR = os.path.join(BASE_DIR, 'data')
MODELS_DIR = os.path.join(BASE_DIR, 'models')
MAX_ARTICLES = 20


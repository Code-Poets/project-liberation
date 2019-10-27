"""
Django settings for project_liberation project.

Generated by 'django-admin startproject' using Django 2.2.3.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
from typing import List

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: It should be located in your local_settings.py.
# SECRET_KEY = ''


ALLOWED_HOSTS = []  # type: List


# Application definition

INSTALLED_APPS = [
    # Django
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 3rd party
    'pipeline',
    'hamlpy',
    'sorl.thumbnail',
    # project-liberation
    'company_website.apps.CompanyWebsiteConfig',
    'project_liberation.apps.ProjectLiberationConfig',
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

ROOT_URLCONF = 'project_liberation.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'loaders': (
                'hamlpy.template.loaders.HamlPyFilesystemLoader',
                'hamlpy.template.loaders.HamlPyAppDirectoriesLoader',
            )
        },
    },
]

WSGI_APPLICATION = 'project_liberation.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "project_liberation",
        "ATOMIC_REQUESTS": True,
        # 'USER':     'postgres',
        # 'PASSWORD': '',
        # 'HOST':     '',
        # 'PORT':     '',
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'pipeline.finders.PipelineFinder',
]

PIPELINE = {
    "CSS_COMPRESSOR": 'pipeline.compressors.cssmin.CSSMinCompressor',
    "JS_COMPRESSOR": 'pipeline.compressors.uglifyjs.UglifyJSCompressor',
    "CSSMIN_BINARY": os.path.join(BASE_DIR, '../node_modules/.bin/cssmin'),
    "UGLIFYJS_BINARY": os.path.join(BASE_DIR, '../node_modules/.bin/uglifyjs'),
    "SASS_BINARY": os.path.join(BASE_DIR, '../node_modules/.bin/sass'),
    'STYLESHEETS': {
        'main': {
            'source_filenames': (
                'main_page/*.sass',
            ),
            'output_filename': 'css/main.css',
        },
        'team_introduction': {
            'source_filenames': (
                'team_introduction_page/*.sass',
            ),
            'output_filename': 'css/team_introduction.css',
        },
        'css_reset': {
            'source_filenames': (
                'css_reset.sass',
            ),
            'output_filename': 'css/css_reset.css',
        },
        'common': {
            'source_filenames': (
                'common/*.sass',
            ),
            'output_filename': 'css/common.css',
        },
    },
    'JAVASCRIPT': {
        'main': {
            'source_filenames': (
                'main_page/scripts/*.js',
            ),
            'output_filename': 'js/main.js'
        },
        'common': {
            'source_filenames': (
                'common/scripts/*.js',
            ),
            'output_filename': 'js/common.js',
        },
        'team_introduction': {
            'source_filenames': (
                'team_introduction_page/scripts/*.js',
            ),
            'output_filename': 'js/team_introduction.js',
        },
    },
    'COMPILERS': ('pipeline.compilers.sass.SASSCompiler',)
}

STATICFILES_STORAGE = 'pipeline.storage.PipelineStorage'

# A key for Google API, necessary for accessing the map on the mainpage.
# GOOGLE_API_KEY = ''
MEDIA_URL = '/media/'

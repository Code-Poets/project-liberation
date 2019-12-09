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
    'django.contrib.sites',
    'django.contrib.sitemaps',
    'django.contrib.staticfiles',
    # Wagtail
    'wagtail.contrib.forms',
    'wagtail.contrib.redirects',
    'wagtail.contrib.modeladmin',
    'wagtail.contrib.table_block',
    'wagtail.embeds',
    'wagtail.sites',
    'wagtail.users',
    'wagtail.snippets',
    'wagtail.documents',
    'wagtail.images',
    'wagtail.search',
    'wagtail.admin',
    'wagtail.core',
    'modelcluster',
    'taggit',
    # 3rd party
    'pipeline',
    'hamlpy',
    'sorl.thumbnail',
    'wagtailmarkdown',
    'google_analytics',
    'robots',
    # project-liberation
    'blog.apps.BlogConfig',
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

    'wagtail.core.middleware.SiteMiddleware',
    'wagtail.contrib.redirects.middleware.RedirectMiddleware',
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

USE_L10N = False

USE_TZ = True


LOGGING = {
    'version':                  1,
    'disable_existing_loggers': False,
    'formatters':               {
        'console': {
            'format':  '%(asctime)s %(levelname)-8s | %(message)s',
            'datefmt': '%H:%M:%S',
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        }
    },
    'handlers': {
        'mail_admins': {
            'level':   'ERROR',
            'filters': ['require_debug_false'],
            'class':   'django.utils.log.AdminEmailHandler',
        },
        'console': {
            'level':     'INFO',
            'class':     'logging.StreamHandler',
            'formatter': 'console',
        },
    },
    'loggers': {
        # NOTE: There are a few important caveats you need to consider when tweaking logging:
        # - If a message is logged to logger 'a.b' and propagates to logger 'a', only the level of logger
        #   'a.b' counts. Level of logger 'a' is ignored. Not kidding. See the diagram:
        #   https://docs.python.org/3/howto/logging.html#logging-flow
        # - level of logger 'a.b' determines not only what it handles but also what it propagates to parent.
        # - If a logger has no level, it inherits level from parent. Root logger (the one called '') has level WARNING by default.

        # RULES: Try to stick to the following conventions:
        # - Don't set level of a logger unless you explicitly want to prevent some messages from being handled or propagated.
        # - In most cases it's better to leave level at DEBUG here and set level in handler instead.
        # - Set level explicitly if you don't propagate. Such a logger should not be dependent on parent's level.
        # - Don't propagate to the root logger if the output is very verbose. Use a separate handler/file instead.
        # - Log at INFO level should be concise and contain only important stuff. Enough to understand what
        #   is happening but not necessarily why. DEBUG level can be more spammy.

        '': {
            # Logging to the console. The application is primarily going to run in foreground inside Docker container
            # and we want Docker to capture all that output. You can add an extra file handler in your local_settings.py
            # if you think you really need it. Do keep in mind though that log files need to be rotated or they'll eat
            # a lot of disk space.
            'handlers':  ['console'],
            # NOTE: Changing level of this logger will change levels of loggers from plugins
            # because they often don't have a level set explicitly and inherit this one instead.
            'level':     'DEBUG',
            'propagate': False,
        },
        'py.warnings': {
            # Prevent Python from printing its warnings to the console. Our top-level logger already handles and prints them.
            # I'm not entirely sure why this works but I think that the default py.warnings has a custom console handler
            # attached and by defining it here we're overwriting it and disabling the handler.
            'level':     'DEBUG',
            'propagate': True,
        },
        'django': {
            # Redefine django logger without handlers. Otherwise errors propagated from django.request
            # get logged to the console twice.
            'handlers':  [],
            'level':     'DEBUG',
            'propagate': True,
        },
        'django.db': {
            # Filter out DEBUG messages. There are too many of them. Django logs all DB queries at this level.
            'level':     'INFO',
            'propagate': True,
        },
        'django.request': {
            # Level is DEBUG because we're leaving filtering up to the handler.
            'handlers':  ['console'],
            'level':     'DEBUG',
            'propagate': True,
        },
        'project_liberation.crash': {
            # Level is DEBUG because we're leaving filtering up to the handler.
            'handlers':  ['console'],
            'level':     'DEBUG',
            'propagate': True,
        },
    },
}


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'pipeline.finders.AppDirectoriesFinder',
    'pipeline.finders.FileSystemFinder',
    'pipeline.finders.CachedFileFinder',
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
        'blog': {
            'source_filenames': (
                'blog/*.sass',
            ),
            'output_filename': 'css/blog.css',
        },
        'blog_post': {
            'source_filenames': (
                'blog_post/*.sass',
            ),
            'output_filename': 'css/blog_post.css',
        },
        'how_we_work': {
            'source_filenames': (
                'how_we_work/how_we_work.sass',
            ),
            'output_filename': 'css/how_we_work.css'
        },
        'career': {
            'source_filenames': (
                'career/*.sass',
            ),
            'output_filename': 'css/career.css',
        },
        'blog_posts_list': {
            'source_filenames': (
                'blog_posts_list/*.sass',
            ),
            'output_filename': 'css/blog_posts_list.css',
        },
        'privacy_and_policy': {
            'source_filenames': (
                'privacy_and_policy/privacy_and_policy.sass',
            ),
            'output_filename': 'css/privacy_and_policy.css'
        },
        'estimate_project': {
            'source_filenames': (
                'estimate_project/*.sass',
            ),
            'output_filename': 'css/estimate_project.css',
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
        'estimate_project': {
            'source_filenames': (
                'estimate_project/scripts/*.js',
            ),
            'output_filename': 'js/estimate_project.js',
        },
        'team_introduction': {
            'source_filenames': (
                'team_introduction_page/scripts/*.js',
            ),
            'output_filename': 'js/team_introduction.js',
        },
        'how_we_work': {
            'source_filenames': (
                'how_we_work/scripts/*.js',
            ),
            'output_filename': 'js/how_we_work.js'
        },
        'blog_post': {
            'source_filenames': (
                'blog_post/scripts/*.js',
            ),
            'output_filename': 'js/blog_post.js'
        },
    },
    'COMPILERS': ('pipeline.compilers.sass.SASSCompiler',)
}

STATICFILES_STORAGE = 'pipeline.storage.PipelineCachedStorage'

# A key for Google API, necessary for accessing the map on the mainpage.
# GOOGLE_API_KEY = ''
MEDIA_URL = '/media/'
COMPANY_EMPLOYEES_STORAGE = 'company_employees_storage'
TESTIMONIAL_PHOTOS_STORAGE = "testimonials/customers-profile-pictures"
MEDIA_ROOT = os.path.join(BASE_DIR, "../storage")

# Wagtail setting variables
WAGTAIL_SITE_NAME = 'blog'
WAGTAIL_APPEND_SLASH = False

WAGTAILIMAGES_MAX_UPLOAD_SIZE = 25 * 1024 * 1024

SITE_ID = 1

# Setting need to be set up in production settings with proper google analytics id
# GOOGLE_ANALYTICS = {
#     'google_analytics_id': '',
# }

DATE_FORMAT = "M. d, Y"

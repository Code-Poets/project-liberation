from .base import *

DEBUG = False

GOOGLE_ANALYTICS = {
    'google_analytics_id': 'UA-128369632-1',
}

INSTALLED_APPS.append("raven.contrib.django.raven_compat")

LOGGING["handlers"]["sentry"] = {  # type: ignore
    'level': 'ERROR',
    'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
}

LOGGING["loggers"]["django.request"]["handlers"] = ['sentry']  # type: ignore
LOGGING["loggers"]["project_liberation.crash"]["handlers"] = ['sentry']  # type: ignore

URL_PREFIX = "https"

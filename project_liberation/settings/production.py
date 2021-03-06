from .base import *

DEBUG = False

GOOGLE_ANALYTICS = {
    'google_analytics_id': 'UA-128369632-1',
}

GOOGLE_ADS_CONVERSION_ID = "AW-607460288"
GOOGLE_ADS_CONVERSION_TARGET_ADDRESS = f"{GOOGLE_ADS_CONVERSION_ID}/pqT6CMvlzdkBEMC31KEC"

GOOGLE_TAG_MANAGER_ID = "GTM-TCWZK7N"

INSTALLED_APPS.append("raven.contrib.django.raven_compat")

LOGGING["handlers"]["sentry"] = {  # type: ignore
    'level': 'ERROR',
    'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
}

LOGGING["loggers"]["django.request"]["handlers"] = ['sentry']  # type: ignore
LOGGING["loggers"]["project_liberation.crash"]["handlers"] = ['sentry']  # type: ignore

URL_PREFIX = "https"

DEFAULT_EMAIL_RECIPIENTS = ("contact@codepoets.it",)
USE_DEFAULT_RECIPIENTS = False

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

from .base import *

DEBUG = True

SECRET_KEY = 'test-key'

DATABASES['default']['USER']     = 'postgres'
DATABASES['default']['PASSWORD'] = ''
DATABASES['default']['HOST']     = ''
DATABASES['default']['PORT']     = ''

GOOGLE_ANALYTICS = {
    'google_analytics_id': 'test_id',
}

GOOGLE_ADS_CONVERSION_ID = "AW-test_id"
GOOGLE_ADS_CONVERSION_TARGET_ADDRESS = f"{GOOGLE_ADS_CONVERSION_ID}/test_address"

STATICFILES_STORAGE = "pipeline.storage.PipelineStorage"

PIPELINE["PIPELINE_ENABLED"] = False

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

from os.path import *
from website.settings import *

INSTALLED_APPS += ('django_nose',)

DATABASES = {
    'default': {
        'ENGINE':'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

PASSWORD_HASHERS = (
    'django.contrib.auth.hashers.MD5PasswordHasher',
)

EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'
SOUTH_TEST_MIGRATE = False

#TEST_RUNNER = 'website.testrunner.NodeCoverageTestRunner'


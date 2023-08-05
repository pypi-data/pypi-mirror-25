from .test_settings import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.oracle',
        'HOST': '127.0.0.1',
        'PORT': '1521',
        'NAME': 'orcl',
    },
}

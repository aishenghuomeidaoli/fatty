from settings import *

ALLOWED_HOSTS = ['api.weblist.site']

DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': 'localhost',
        'USER': 'root',
        'PASSWORD': 'cannot be seen',
        'NAME': 'fatty',
        'PORT': '3306',
        'CHARSET': 'utf-8',
    }
}

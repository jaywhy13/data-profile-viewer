import django_heroku

from .base import *  # noqa
from .base import env

SECRET_KEY = env('DJANGO_SECRET_KEY')
ALLOWED_HOSTS = env.list('DJANGO_ALLOWED_HOSTS', default=[])

INSTALLED_APPS += ['gunicorn']  # noqa F405

django_heroku.settings(locals())

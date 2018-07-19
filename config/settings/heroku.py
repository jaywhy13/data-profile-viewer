import django_heroku

from .base import *  # noqa
from .base import env

SECRET_KEY = env('DJANGO_SECRET_KEY')
ALLOWED_HOSTS = env.list('DJANGO_ALLOWED_HOSTS', default=[])

INSTALLED_APPS += ['gunicorn']  # noqa F405


# Setup for Webpack
STATICFILES_DIRS += [os.path.join(BASE_DIR, "frontend", "assets")]

WEBPACK_LOADER = {
    'DEFAULT': {
            'BUNDLE_DIR_NAME': 'bundles/',
            'STATS_FILE': os.path.join(BASE_DIR, 'webpack-stats.prod.json'),
        }
}


# This should be last
django_heroku.settings(locals())


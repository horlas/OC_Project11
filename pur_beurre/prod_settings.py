import dj_database_url
from pur_beurre.settings import *

DEBUG = False

TEMPLATE_DEBUG = False

SECRET_KEY = os.environ.get('SECRET_KEY')

ALLOWED_HOSTS = ['purbeurre.cedrix.org' , '*']


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'quality',
        'USER': 'admin',
        'PASSWORD': 'admin1234',
        'HOST': '',
        'PORT': '5432',
    }
}


# MIDDLEWARE += ['whitenoise.middleware.WhiteNoiseMiddleware']
#
#
# STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# used only for heroku deployment
# db_from_env = dj_database_url.config(conn_max_age=600, ssl_require=True)
#
# DATABASES['default'] = db_from_env

STATIC_ROOT = os.path.join(BASE_DIR , 'staticfiles')

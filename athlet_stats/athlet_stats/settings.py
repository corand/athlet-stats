"""
Django settings for athlet_stats project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
from django.utils.translation import ugettext_lazy as _
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '-n7)uxbrcci3)=8dyo%(t&9zi3*0-3g!55fm8d8r7t9u!h2e!_'
SITE_ID = 1

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

ADMIN_MEDIA_PREFIX = '/static/admin/'

LOGIN_REDIRECT_URL = '/login'
LOGIN_URL = '/login'



# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
MEDIA_ROOT = os.path.join(BASE_DIR,'athlet_stats/carga')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = 'http://localhost:8000/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"

STATIC_ROOT = ''



TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR,'athlet_stats/templates'),
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)
# Additional locations of static files
STATICFILES_DIRS = (
    os.path.join(BASE_DIR,'athlet_stats/static'),
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites', # Note this one is not included by default
    'django.contrib.comments', # Note this one is not included by default
    'durationfield',
    'rosetta',
    'blog',
    'races',
    'ckeditor',
    'profiles',
    'debug_toolbar',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.i18n',
    'django.core.context_processors.request',
    'django.core.context_processors.static',
)

ROOT_URLCONF = 'athlet_stats.urls'

WSGI_APPLICATION = 'athlet_stats.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'athlet_stats', # Or path to database file if using sqlite3.
        # The following settings are not used with sqlite3:
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': 'localhost', # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': '', # Set to empty string for default.
    }
}
# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'Europe/Madrid'

LANGUAGES = (
    ('es', _('Spanish')),
    ('eu', _('Basque')),
)

# TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True



LANGUAGE_CODE = 'es-es'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

LOCALE_PATHS = (
    os.path.join(BASE_DIR,'locale'),
)


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'

CKEDITOR_UPLOAD_PATH = "media/"
CKEDITOR_RESTRICT_BY_USER = True

CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'full',
        'extraPlugins': 'oembed',
        'height': 400,
        'width': 800,
    },
}

DEBUG_TOOLBAR_PATCH_SETTINGS = False

AUTH_USER_MODEL = "profiles.UserProfile"
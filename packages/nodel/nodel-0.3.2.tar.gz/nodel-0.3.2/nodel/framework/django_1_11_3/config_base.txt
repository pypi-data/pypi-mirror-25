import os
import sys
from os import environ

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SITE_ROOT = os.path.dirname(BASE_DIR)
SITE_NAME = os.path.basename(SITE_ROOT)

sys.path.append(BASE_DIR)

DEBUG = False
ALLOWED_HOSTS = ['*']
WSGI_APPLICATION = 'core.wsgi.application'

LANGUAGE_CODE = 'en_US'

TIME_ZONE = 'UTC'
DEFAULT_CHARSET = 'utf-8'
USE_I18N = True
USE_L10N = True
USE_TZ = True

STATIC_URL = '/static/'
MEDIA_URL = '/media/'
MEDIA_ROOT = '%s/media' % SITE_ROOT
STATIC_ROOT = '%s/static' % SITE_ROOT
ROOT_URLCONF = 'core.urls'

SECRET_KEY = environ.get('SECRET_KEY')

STATICFILES_DIRS = (
	'%s/assets' % SITE_ROOT,
)

LOCALE_PATHS = (
	'%s/locale' % SITE_ROOT,
)

DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.sqlite3',
		'NAME': '%s/database.db' % BASE_DIR
	}
}


INSTALLED_APPS = (
	'django.contrib.admin',
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.messages',
	'django.contrib.staticfiles'
)


MIDDLEWARE_CLASSES = (
	'django.contrib.sessions.middleware.SessionMiddleware',
	'django.middleware.common.CommonMiddleware',
	'django.middleware.csrf.CsrfViewMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
	'django.contrib.messages.middleware.MessageMiddleware',
	'django.middleware.clickjacking.XFrameOptionsMiddleware',
	'django.middleware.security.SecurityMiddleware',
)

TEMPLATES = [
	{
		'BACKEND': 'django.template.backends.django.DjangoTemplates',
		'DIRS': (
			'%s/templates' % BASE_DIR,
		),
		'APP_DIRS': True,
		'OPTIONS': {
			'context_processors': [
				'django.template.context_processors.debug',
				'django.template.context_processors.request',
				'django.contrib.auth.context_processors.auth',
				'django.contrib.messages.context_processors.messages',
			],
		},
	},
]

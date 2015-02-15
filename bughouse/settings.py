"""
Django settings for bughouse-rankings project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import excavator
from dj_database_url import config as dj_config


BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = excavator.env_string('DJANGO_SECRET_KEY', required=True)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = excavator.env_bool('DJANGO_DEBUG', required=True)

ALLOWED_HOSTS = excavator.env_list("DJANGO_ALLOWED_HOSTS", required=True)

TEMPLATE_DEBUG = DEBUG


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # local
    'bughouse',
    # 3rd party
    'pipeline',
    'argonauts',
    'rest_framework',
    'sorl.thumbnail',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'bughouse.urls'

WSGI_APPLICATION = 'bughouse.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': dj_config(),
}


# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images) and Media
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = excavator.env_string(
    'DJANGO_STATIC_URL', default='/static/', required=False,
)
STATIC_ROOT = os.path.abspath(
    excavator.env_string('DJANGO_STATIC_ROOT', required=True),
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'pipeline.finders.CachedFileFinder',
    'pipeline.finders.PipelineFinder',
)

MEDIA_URL = excavator.env_string(
    'DJANGO_MEDIA_URL', default='/media/', required=False,
)
MEDIA_ROOT = os.path.abspath(
    excavator.env_string('DJANGO_MEDIA_ROOT', required=True),
)

DEFAULT_FILE_STORAGE = excavator.env_string('DEFAULT_FILE_STORAGE')
STATICFILES_STORAGE = excavator.env_string('STATICFILES_STORAGE')


# Pipeline
PIPELINE_ENABLED = excavator.env_bool('DJANGO_PIPELINE_ENABLED', default=not DEBUG)

PIPELINE_DISABLE_WRAPPER = True

PIPELINE_CSS = {
    'base': {
        'source_filenames': (
            "css/bootstrap.css",
            "css/bootstrap-theme.css",
            "css/custom.css",
        ),
        'output_filename': 'css/base.css',
    },
}

PIPELINE_JS = {
    'base': {
        'source_filenames': (
            "js/jquery.js",
            "js/d3.js",
            "js/bootstrap.js",
            "js/handlebars.js",
            "js/underscore.js",
            "js/backbone.js",
            "js/backbone.wreqr.js",
            "js/backbone.babysitter.js",
            "js/backbone.marionette.js",
            "js/backbone.marionette.export.js",
            # Config
            "js/config.js",
        ),
        'output_filename': 'js/base.js',
    },
    'player-roster-templates': {
        'source_filenames': (
            "js/player-roster/templates/**.handlebars",
        ),
        'output_filename': 'js/player-roster-templates.js',
    },
    'player-roster': {
        'source_filenames': (
            "js/player-roster/templates/**.handlebars",
            "js/player-roster/models.js",
            "js/player-roster/collections.js",
            "js/player-roster/views.js",
            "js/player-roster/layouts.js",
            "js/player-roster/app.js",
        ),
        'output_filename': 'js/player-roster.js',
    },
    'report-game-templates': {
        'source_filenames': (
            "js/report-game/templates/**.handlebars",
        ),
        'output_filename': 'js/report-game-templates.js',
    },
    'report-game': {
        'source_filenames': (
            "js/report-game/templates/**.handlebars",
            "js/report-game/models.js",
            "js/report-game/collections.js",
            "js/report-game/views.js",
            "js/report-game/layouts.js",
            "js/report-game/app.js",
        ),
        'output_filename': 'js/report-game.js',
    },
    'player-rating-visualizations-templates': {
        'source_filenames': (
            "js/player-rating-visualizations/templates/**.handlebars",
        ),
        'output_filename': 'js/player-rating-visualizations-templates.js',
    },
    'player-rating-visualizations': {
        'source_filenames': (
            "js/player-rating-visualizations/app.js",
            "js/player-rating-visualizations/layouts.js",
            "js/player-rating-visualizations/views.js",
            "js/player-rating-visualizations/models.js",
            "js/player-rating-visualizations/collections.js",
        ),
        'output_filename': 'js/player-rating-visualizations.js',
    },
}
PIPELINE_CSS_COMPRESSOR = 'pipeline.compressors.NoopCompressor'
PIPELINE_JS_COMPRESSOR = 'pipeline.compressors.NoopCompressor'

PIPELINE_TEMPLATE_EXT = '.handlebars'
PIPELINE_TEMPLATE_FUNC = 'Handlebars.compile'
PIPELINE_TEMPLATE_NAMESPACE = 'Handlebars.templates'

# Ratings Engines
ELO_RATING_ENGINES = (
    'bughouse.ratings.engines.overall.OverallPlayerRatings',
    'bughouse.ratings.engines.overall.OverallPlayerRatingsAsWhite',
    'bughouse.ratings.engines.overall.OverallPlayerRatingsAsBlack',
    'bughouse.ratings.engines.overall.OverallTeamRatings',
    # Experimental
    'bughouse.ratings.engines.batman.BatmanRatings',
)

# ELO constants
ELO_K = 4.0
ELO_WIN_TEAM = 50.0 / ELO_K
ELO_LOSE_TEAM = - ELO_WIN_TEAM

ELO_WIN_SELF = 55 / ELO_K
ELO_WIN_PARTNER = 45 / ELO_K

ELO_LOSE_SELF = (-1) * ELO_WIN_SELF
ELO_LOSE_PARTNER = (-1) * ELO_WIN_PARTNER

ELO_PARTNER_WEIGHT = 1.0 / 5
ELO_SELF_WEIGHT = 1 - ELO_PARTNER_WEIGHT
ELO_PROVISIONAL_GAME_LIMIT = 10
ELO_PROVISIONAL_GAME_MODIFIER = 4

# Sorl Thumbnailer
THUMBNAIL_FORMAT = "PNG"

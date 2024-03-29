"""
Django settings for stopwatch project.

Generated by 'django-admin startproject' using Django 3.2.3.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import re
import dj_database_url

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = os.path.dirname(PROJECT_DIR)


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/


# Application definition

INSTALLED_APPS = [
    'stopwatch',
    'search',
    'projects',

    'commonknowledge.bootstrap',
    'commonknowledge.django',
    'commonknowledge.wagtail',

    'wagtail_content_import',
    'import_export',

    'wagtail.contrib.forms',
    'wagtail.contrib.redirects',
    'wagtail.contrib.settings',
    'wagtail.embeds',
    'wagtail.sites',
    'wagtail.users',
    'wagtail.snippets',
    'wagtail.documents',
    'wagtail.images',
    'wagtail.search',
    'wagtail.admin',
    'wagtail.core',
    'wagtail_transfer',
    'wagtailmetadata',
    "wagtail.contrib.routable_page",

    'modelcluster',
    'taggit',
    'webpack_loader',
    "anymail",
    "rest_framework",
    'django_bootstrap5',
    'colorfield',

    'django.contrib.gis',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'wagtail.contrib.redirects.middleware.RedirectMiddleware',
]

ROOT_URLCONF = 'stopwatch.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(PROJECT_DIR, 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'wagtail.contrib.settings.context_processors.settings',
            ],
        },
    },
]

WSGI_APPLICATION = 'stopwatch.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

if os.getenv('SKIP_DB') != '1':
    DATABASES = {
        'default': dj_database_url.parse(
            re.sub(
                r"^postgres(ql)?",
                "postgis",
                os.getenv('DATABASE_URL')
            ),
            conn_max_age=600,
            ssl_require=False
        )
    }

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

AUTH_USER_MODEL = 'stopwatch.User'


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'dist'),
    os.path.join(BASE_DIR, 'stopwatch', 'static')
]

WEBPACK_LOADER = {
    'DEFAULT': {
        'BUNDLE_DIR_NAME': '',  # must end with slash
        'STATS_FILE': os.path.join(BASE_DIR, 'dist/webpack-stats.json'),
        'POLL_INTERVAL': 0.1,
        'IGNORE': [r'.+\.hot-update.js', r'.+\.map'],
        # CACHE
        # Additional
        'TIMEOUT': None,
        'LOADER_CLASS': 'webpack_loader.loader.WebpackLoader',
    }
}

# ManifestStaticFilesStorage is recommended in production, to prevent outdated
# JavaScript / CSS assets being served from cache (e.g. after a Wagtail upgrade).
# See https://docs.djangoproject.com/en/3.2/ref/contrib/staticfiles/#manifeststaticfilesstorage
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'

STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'


# Wagtail settings

WAGTAIL_SITE_NAME = "stopwatch"

WAGTAILADMIN_BASE_URL = 'https://www.stop-watch.org'

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'
WAGTAILIMAGES_IMAGE_MODEL = 'stopwatch.StopwatchImage'
WAGTAILDOCS_DOCUMENT_MODEL = 'stopwatch.StopWatchDocument'

WAGTAILSEARCH_BACKENDS = {
    'default': {
         'BACKEND': 'wagtail.search.backends.database',
        'AUTO_UPDATE': True,
    }
}

WAGTAILEMBEDS_FINDERS = [
    {
        'class': 'commonknowledge.wagtail.embed_providers.flourish.FlourishFinder',
    },
    {
        'class': 'commonknowledge.wagtail.embed_providers.shiny.ShinyFinder',
    },
    {
        'class': 'commonknowledge.wagtail.embed_providers.youtube.YouTubeFinder',
    },
    {
        'class': 'wagtail.embeds.finders.oembed',
    },
]

WAGTAILEMBEDS_RESPONSIVE_HTML = True

# Rest settings

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ]
}


# Logging

DJANGO_LOG_LEVEL = os.getenv('DJANGO_LOG_LEVEL', 'INFO')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        '': {
            'handlers': ['console'],
            'level': DJANGO_LOG_LEVEL,
        },
    },
}

"""
Django settings for demovibes project.

Generated by 'django-admin startproject' using Django 4.2.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Application definition

# If PREPEND_WWW is True, URLs that lack a leading “www.” will be redirected to the same URL with a leading “www.”
#PREPEND_WWW = True

INSTALLED_APPS = [
    # Key-Value store for site settings
    #  also contains 'common' abstract models etc
    'demovibes.core.apps.CoreConfig',

    # events system
    'demovibes.events.apps.EventsConfig',

    # Backend control pages
    'demovibes.backend.apps.BackendConfig',

    # Generic Collection (artist, album, group, label, tag, etc)
    'demovibes.collections.apps.CollectionsConfig',
    # Individual song, the basic unit of the site
    'demovibes.songs.apps.SongsConfig',

    # Playlist (queue)
    'demovibes.playlist.apps.PlaylistConfig',

    # Other site areas
    'demovibes.player.apps.PlayerConfig',
    'demovibes.chat.apps.ChatConfig',

    'demovibes.user_profiles.apps.UserProfilesConfig',

    # Admin panel, user auth, and dependencies
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    # django-allauth settings
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # https://docs.djangoproject.com/en/4.2/ref/contrib/admin/admindocs/#included-bookmarklets
    'django.contrib.admindocs.middleware.XViewMiddleware',
    'django.contrib.sites.middleware.CurrentSiteMiddleware',
]

ROOT_URLCONF = 'demovibes.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [ BASE_DIR / 'templates' ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
#                'django.template.context_processors.i18n',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',

                'demovibes.core.context_processors.settings',
                'demovibes.playlist.context_processors.now_playing',
                'demovibes.collections.context_processors.collection_types',
                'demovibes.chat.context_processors.chat_recent',
            ],
        },
    },
]

WSGI_APPLICATION = 'demovibes.wsgi.application'

LOGIN_REDIRECT_URL = 'index'

SITE_ID = 1


# Database
#  see local_settings.py


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = False

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'

STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

MEDIA_URL = 'media/'

MEDIA_ROOT = BASE_DIR / 'media'


# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Authentication Settings
#  see local_settings.py


# Email
#  see local_settings.py


from demovibes.local_settings import *

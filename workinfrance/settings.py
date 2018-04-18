import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = os.environ.get('WIF_SECRET_KEY')

DEBUG = os.environ.get('WIF_DEBUG')

ALLOWED_HOSTS = []

DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

THIRD_PARTY_APPS = [
    'prettyjson',  # https://github.com/kevinmickey/django-prettyjson
]

WORKINFRANCE_APPS = [
    'workinfrance.stats',
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + WORKINFRANCE_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'workinfrance.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'workinfrance/templates'),
        ],
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

WSGI_APPLICATION = 'workinfrance.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get('WIF_DATABASE_NAME'),
        'USER': os.environ.get('WIF_DATABASE_USER', default='postgres'),
        'PASSWORD': os.environ.get('WIF_DATABASE_PASSWORD', default=''),
        'HOST': os.environ.get('WIF_DATABASE_HOST', default='localhost'),
        'PORT': os.environ.get('WIF_DATABASE_PORT', default=5432),
        'ATOMIC_REQUESTS': True,
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'fr-FR'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = '/static/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'workinfrance/media/')

# Settings for demarches-simplifiees.fr (DS)
DS_PROCEDURE_ID_APT = os.environ.get('DEMARCHES_SIMPLIFIEES_PROCEDURE_ID_APT')
DS_API_TOKEN = os.environ.get('DEMARCHES_SIMPLIFIEES_API_TOKEN')
DS_API_BASE_URL = 'https://www.demarches-simplifiees.fr/api/v1'

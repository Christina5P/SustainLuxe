import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
    '8000-christina5p-sustainluxe-5tw6roijx8w.ws.codeinstitute-ide.net'
]

AUTHENTICATION_BACKENDS = [
     'django.contrib.auth.backends.ModelBackend',
     'allauth.account.auth_backends.AuthenticationBackend',
 ]

CSRF_TRUSTED_ORIGINS = [
    'https://8000-christina5p-sustainluxe-5tw6roijx8w.ws.codeinstitute-ide.net',
]

SITE_ID = 1

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


ACCOUNT_AUTHENTICATION_METHOD = 'username_email'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
ACCOUNT_SIGNUP_EMAIL_ENTER_TWICE = True
ACCOUNT_USERNAME_MIN_LENGTH = 3
LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/'

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'rest_framework',
    'corsheaders',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'home',
    'products',
    'checkout',
    'django_countries',
    'profiles',
    'bag',
    'crispy_forms',
    'crispy_bootstrap5',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.http.ConditionalGetMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]

ROOT_URLCONF = 'sustainluxe.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
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

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"


WSGI_APPLICATION = 'sustainluxe.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

#DATABASES = {
#    'default': {
 #       'ENGINE': 'django.db.backends.sqlite3',
  #      'NAME': BASE_DIR / 'db.sqlite3',
   # }
#}

DATABASES = {
    'default': dj_database_url.parse('postgres://u2sgdioodl0:4g0rBitWsuih@ep-gentle-mountain-a23bxz6h-pooler.eu-central-1.aws.neon.tech/cable_snowy_mummy_751580')
    }

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)


# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CORS_ORIGIN_ALLOW_ALL = True

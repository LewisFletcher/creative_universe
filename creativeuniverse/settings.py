from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

#NPM_BIN_PATH = r'C:\Program Files\\nodejs\\npm.cmd'

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!


SECRET_KEY = os.environ['SECRET_KEY']

ALLOWED_HOSTS = ['.creativeuniverseproductions.com', 'creativeuniverseproductions.com']

CSRF_TRUSTED_ORIGINS = ['https://creativeuniverseproductions.com', 'https://www.creativeuniverseproductions.com']

AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']

AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']

AWS_STORAGE_BUCKET_NAME = 'creativeuniverse-media'

STRIPE_WEBHOOK_SECRET = os.environ['STRIPE_WEBHOOK_SECRET']

STRIPE_PUBLISHABLE_KEY = 'pk_live_51OeLuqG86heXUEazstgiRNL17oocJ6UoD2rJX4jm4lZ6ujuqm33b7cLKT5QiYxhupqghVvF0w13342796SEiMAkC00y0yUFZiR'

STRIPE_SECRET_KEY = os.environ['STRIPE_SECRET_KEY']

DEFAULT_FROM_EMAIL = 'support@creativeuniverseproductions.com'

AWS_SES_RETURN_PATH  = 'katelynS80@gmail.com'

SERVER_EMAIL = 'admin@creativeuniverseproductions.com'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ADMINS = [('lewis', 'lew.fletcher3@gmail.com')]

TAILWIND_APP_NAME = 'theme' #tailwind src
# Application definition

INSTALLED_APPS = [
    'grappelli',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    #Dependencies
    'tailwind',
    'theme',
    #'django_browser_reload',
    #"debug_toolbar",
    "storages",
    "django_htmx",
    'markdownx',
    "crispy_forms",
    "crispy_tailwind",

    #Apps
    'home.apps.HomeConfig',
    'about.apps.AboutConfig',
    'shop.apps.ShopConfig',
    'artpage.apps.ArtpageConfig',
    'contact.apps.ContactConfig',
    'staff.apps.StaffConfig',
    'faq.apps.FaqConfig',
]

CRISPY_ALLOWED_TEMPLATE_PACKS = "tailwind"

CRISPY_TEMPLATE_PACK = "tailwind"

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    #"debug_toolbar.middleware.DebugToolbarMiddleware",
    #"django_browser_reload.middleware.BrowserReloadMiddleware",
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "django_htmx.middleware.HtmxMiddleware",
]

ROOT_URLCONF = 'creativeuniverse.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'creativeuniverse.wsgi.application'

CSRF_COOKIE_SECURE = True

SESSION_COOKIE_SECURE = True


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/Los_Angeles'

USE_I18N = True

USE_TZ = True

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

SECURE_SSL_REDIRECT = True

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

SECURE_HSTS_SECONDS = 86400

SECURE_HSTS_INCLUDE_SUBDOMAINS = True

SECURE_HSTS_PRELOAD = True

SECURE_CONTENT_TYPE_NOSNIFF = True

SECURE_BROWSER_XSS_FILTER = True

X_FRAME_OPTIONS = 'DENY'

RECAPTCHA_PUBLIC_KEY = os.environ['RECAPTCHA_PUBLIC_KEY']

RECAPTCHA_PRIVATE_KEY = os.environ['RECAPTCHA_PRIVATE_KEY']

RECAPTCHA_REQUIRED_SCORE = 0.85

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / "staticfiles"
MEDIA_URL = 'https://d3fjin3vuqewzx.cloudfront.net/'

AWS_S3_CUSTOM_DOMAIN = 'd3fjin3vuqewzx.cloudfront.net'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media').replace('\\', '/')

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

import dj_database_url
db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(db_from_env)

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

AWS_S3_FILE_OVERWRITE = False

AWS_DEFAULT_ACL = None

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

AWS_SES_REGION_NAME = 'us-west-2'

AWS_SES_REGION_ENDPOINT = 'email.us-west-2.amazonaws.com'

ADMINS = [('lewis', 'lew.fletcher3@gmail.com')]

EMAIL_BACKEND = 'django_ses.SESBackend'
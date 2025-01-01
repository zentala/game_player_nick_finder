# game_player_nick_finder/game_player_nick_finder/settings.py
# Ustawienia Django

# Build paths inside the project like this: BASE_DIR / 'subdir'.
import os
from dotenv import load_dotenv

# Load ENVs from .env file
load_dotenv()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'your-secret-key'  # Domyślnie zazwyczaj 'django-insecure-SECRET_KEY'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Define the ALLOWED_HOSTS list for production
# Add other allowed hosts when deploying to the production server
ALLOWED_HOSTS = ['localhost', '127.0.0.1', '[::1]', 'gpnf.zentala.io']

# Sites
SITE_ID = 1

# Application definition
INSTALLED_APPS = [
    'app',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google', #for google aut|
    'corsheaders',
    'crispy_forms',
    'crispy_bootstrap5',
    'django.contrib.admin',
    'django_registration',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    # 'main.apps.MainConfig',
    'rest_framework',
    'widget_tweaks'
]

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware'
]

# Define the URLConf for your application (e.g., your_app_name.urls)
ROOT_URLCONF = 'game_player_nick_finder.urls'


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'app', 'templates')],
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

WSGI_APPLICATION = 'game_player_nick_finder.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
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


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'


# Session settings
# Docs: https://docs.djangoproject.com/en/4.2/topics/http/sessions/

SESSION_ENGINE = 'django.contrib.sessions.backends.signed_cookies' # Set the session engine to use cookies
SESSION_COOKIE_SECURE = False  # Set to True in production
SESSION_COOKIE_HTTPONLY = True  # Set the session cookies to be accessible only to the server (not accessible from the browser)
SESSION_COOKIE_SAMESITE = 'Lax'  # Require that the session cookie is sent only with requests originating from the same site
SESSION_COOKIE_AGE = 3600 # Optionally, you can set the age of the session cookies (in seconds), eg. set to one hour (3600 seconds)

# Login settings
LOGIN_REDIRECT_URL = '/'  # Redirect to homepage after login
LOGIN_URL = '/accounts/login/'  # Login page URL

# Django Registration settings
# Docs: https://django-registration.readthedocs.io/en/latest/settings.html

ACCOUNT_ACTIVATION_DAYS = 7 # One-week activation window
REGISTRATION_OPEN = True # is registration possible
REGISTRATION_SALT = os.getenv('REGISTRATION_SALT', '')


AUTHENTICATION_BACKENDS = (
 #used for default signin such as loggin into admin panel
 'django.contrib.auth.backends.ModelBackend',

 #used for social authentications
 'allauth.account.auth_backends.AuthenticationBackend',
 )

# LOGIN_REDIRECT_URL = '/tutorials'

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        }
    }
}



# E-mail server settings
# Docs: https://docs.djangoproject.com/en/4.2/topics/email/

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.getenv('EMAIL_HOST', 'localhost')
EMAIL_PORT = int(os.getenv('EMAIL_PORT', '587'))
EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS', 'True').lower() == 'true'
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD', '')

DEFAULT_FROM_EMAIL='zentala@gmail.com'

CORS_ALLOW_ALL_ORIGINS = True  # TODO for devs onlny

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
    ],
}

CSRF_TRUSTED_ORIGINS = [
    'https://gpnf.zentala.io',
]

# SESSION_COOKIE_DOMAIN = '.zentala.io'  # Enable only in production

# Dodaj ustawienie do włączania/wyłączania mocków
ENABLE_MOCK_MESSAGES = True

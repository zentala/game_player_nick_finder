# game_player_nick_finder/settings/local.py
# Local development settings

from .base import *

# Load local environment variables
load_dotenv(os.path.join(BASE_DIR, '.env.local'))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'your-secret-key-for-development')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1', '[::1]']

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Session settings
SESSION_ENGINE = 'django.contrib.sessions.backends.signed_cookies'
SESSION_COOKIE_SECURE = False  # No HTTPS in development
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'
SESSION_COOKIE_AGE = 3600

# CORS settings
CORS_ALLOW_ALL_ORIGINS = True  # Only for development!

# Email settings
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'  # Print emails to console in development

# Django Allauth settings for development
# Rate limiting for login attempts (0 = disabled in development)
ACCOUNT_LOGIN_ATTEMPTS_LIMIT = 0  # Disable rate limiting in development
ACCOUNT_LOGIN_ATTEMPTS_TIMEOUT = 0  # Disable timeout
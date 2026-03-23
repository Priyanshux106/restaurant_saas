from .base import *
from dotenv import load_dotenv
import os
import dj_database_url

load_dotenv()

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# Render sets this environment variable
ALLOWED_HOSTS = [os.environ.get('RENDER_EXTERNAL_HOSTNAME', 'localhost')]

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases
DATABASES = {
    'default': dj_database_url.config(
        default=os.environ.get('DATABASE_URL'),
        conn_max_age=600
    )
}

# CORS settings for production (restrict to frontend domain)
CORS_ALLOWED_ORIGINS = [
    os.environ.get('CORS_ALLOWED_ORIGIN', 'https://restaurant-site.vercel.app'),
]

# Static files (CSS, JavaScript, Images) for production (WhiteNoise)
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Add WhiteNoise middleware right after SecurityMiddleware
# Find the index of SecurityMiddleware to insert WhiteNoise after it
try:
    security_idx = MIDDLEWARE.index('django.middleware.security.SecurityMiddleware')
    MIDDLEWARE.insert(security_idx + 1, 'whitenoise.middleware.WhiteNoiseMiddleware')
except ValueError:
    MIDDLEWARE.append('whitenoise.middleware.WhiteNoiseMiddleware')

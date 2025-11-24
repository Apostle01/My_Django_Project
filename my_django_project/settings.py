
import os
from pathlib import Path
import dj_database_url
from django.core.exceptions import ImproperlyConfigured

BASE_DIR = Path(__file__).resolve().parent.parent

# Load .env if available
try:
    from dotenv import load_dotenv
    load_dotenv(BASE_DIR / ".env")
except Exception:
    pass

# Security
SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-please-change')
if not SECRET_KEY:
    raise ImproperlyConfigured('SECRET_KEY environment variable is required')

DEBUG = os.getenv('DEBUG', 'False') == 'True'

ALLOWED_HOSTS = (
    os.getenv('ALLOWED_HOSTS').split(',')
    if os.getenv('ALLOWED_HOSTS')
    else ['127.0.0.1', 'localhost', '.railway.app']
)

CSRF_TRUSTED_ORIGINS = []
if os.getenv('RAILWAY_APP_URL'):
    CSRF_TRUSTED_ORIGINS.append(f"https://{os.getenv('RAILWAY_APP_URL')}")

# Apps
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    'whitenoise.runserver_nostatic',
    'cloudinary',
    'cloudinary_storage',
    'crispy_forms',
    'crispy_bootstrap4',

    # Your apps
    'home',
    'products',
    'category',
    'bag',
    'store',
    'checkout',
    'profiles',
    'accounts',
    # Allauth
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
]

# Middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # Required by django-allauth
    'allauth.account.middleware.AccountMiddleware',
]

ROOT_URLCONF = 'my_django_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'my_django_project.wsgi.application'

# Database
DATABASE_URL = os.getenv('DATABASE_URL')
if DATABASE_URL:
    DATABASES = {
        'default': dj_database_url.parse(
            DATABASE_URL,
            conn_max_age=600,
            ssl_require=('postgres' in DATABASE_URL),
        )
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# International
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Media / Cloudinary
CLOUDINARY_URL = os.getenv('CLOUDINARY_URL')
if CLOUDINARY_URL:
    DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
else:
    MEDIA_URL = '/media/'
    MEDIA_ROOT = BASE_DIR / 'media'

# Default Primary Key Field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Stripe
STRIPE_PUBLIC_KEY = os.getenv('STRIPE_PUBLIC_KEY', '')
STRIPE_SECRET_KEY = os.getenv('STRIPE_SECRET_KEY', '')

# Site ID
SITE_ID = 1 # int(os.getenv('SITE_ID', 1))

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {'console': {'class': 'logging.StreamHandler'}},
    'root': {'handlers': ['console'], 'level': 'INFO'},
}

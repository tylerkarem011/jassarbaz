# intc_jassarbaz/settings.py

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-change-this-in-production!!!'

DEBUG = True
ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core',
    'crispy_forms',
    'crispy_bootstrap5',
]

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'intc_jassarbaz.urls'

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

WSGI_APPLICATION = 'intc_jassarbaz.wsgi.application'

# ==================== БАЗА ДАННЫХ ====================
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

if os.environ.get('DATABASE_URL'):
    import dj_database_url
    DATABASES['default'] = dj_database_url.config(conn_max_age=600, ssl_require=True)

LANGUAGE_CODE = 'ru'
TIME_ZONE = 'Asia/Almaty'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

DATA_UPLOAD_MAX_MEMORY_SIZE = 524288000
FILE_UPLOAD_MAX_MEMORY_SIZE = 524288000

STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# ==================== JAZZMIN — БЕЗ ЛОГОТИПА ВООБЩЕ ====================
JAZZMIN_SETTINGS = {
    "site_title": "Jas Sarbaz Admin",
    "site_header": "ЖАС САРБАЗ",
    "site_brand": "Jas Sarbaz",
    "welcome_sign": "Панель управления военно-патриотического клуба",
    "copyright": "Innovative Technical College © 2026",

    # === ПОЛНОСТЬЮ УБИРАЕМ ЛОГОТИП ОТОВСЮДУ ===
    "site_logo": None,
    "site_logo_classes": "",
    "site_icon": None,
    "login_logo": None,
    "login_logo_dark": None,
    "show_login_logo": False,

    "theme": "darkly",
    "primary_color": "#0d6efd",
    "secondary_color": "#003087",
    "accent_color": "#ffc107",

    "icons": {
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",
        "auth.Group": "fas fa-users",
        "core.ClubMember": "fas fa-user-graduate",
        "core.Achievement": "fas fa-trophy",
        "core.Training": "fas fa-dumbbell",
        "core.News": "fas fa-newspaper",
        "core.Event": "fas fa-calendar-alt",
        "core.GalleryImage": "fas fa-images",
        "core.Video": "fas fa-video",
    },
    "show_ui_builder": False,
}

JAZZMIN_UI_TWEAKS = {
    "custom_css": "admin/css/custom.css",
    "custom_js": "admin/js/hide-logo.js",
}
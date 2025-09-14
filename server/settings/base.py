from pathlib import Path
from config.env import DEBUG_SECRET

from django.templatetags.static import static
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

BASE_DIR = Path(__file__).resolve().parent.parent

DEBUG = DEBUG_SECRET


ROOT_URLCONF = 'server.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'server.wsgi.application'

AUTH_USER_MODEL = "user.User"

AUTHENTICATION_BACKENDS = [
    "user.backends.CustomBackend",             
    "django.contrib.auth.backends.ModelBackend" 
]

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




STATIC_URL = 'static/'
STATICFILES_DIRS = [
    BASE_DIR / "static",
]
STATIC_ROOT = BASE_DIR / 'staticfiles'
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / "media"



LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Africa/Lagos'

USE_I18N = True

USE_TZ = True

UNFOLD = {
    "SITE_TITLE": "CodeFuse Admin",
    "SITE_HEADER": "CodeFuse Dashboard",
    "SITE_URL": "/",
    "SITE_ICON": {
        "light": lambda request: static("images/icon.png"),
        "dark": lambda request: static("images/icon.png"),
    },

    "SHOW_PROFILE": True,
    "THEME": "auto",  
    "EXPORT": True,   

    "COLORS": {
        "primary": {
            "50": "#eef2ff",
            "100": "#e0e7ff",
            "200": "#c7d2fe",
            "300": "#a5b4fc",
            "400": "#818cf8",
            "500": "#667eea",
            "600": "#3a84f3",
            "700": "#3730a3",
            "800": "#312e81",
            "900": "#1e1b4b",
        },
        "accent": {"DEFAULT": "#3a84f3"},
        "success": {"DEFAULT": "#10b981"},
        "warning": {"DEFAULT": "#f59e0b"},
        "error": {"DEFAULT": "#ef4444"},
        "info": {"DEFAULT": "#3b82f6"},
    },

    "SITE_FAVICONS": [
        {
            "rel": "icon",
            "sizes": "32x32",
            "type": "image/png",
            "href": lambda request: static("images/icon.png"),
        },
    ],
}

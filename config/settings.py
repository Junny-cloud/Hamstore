"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 3.2.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from django.contrib.messages import constants as messages
import os
from pathlib import Path
from decouple import config
from config import db
from datetime import datetime, timedelta
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

# Application definition

DJANGO_PACKAGES = [
    'jazzmin',
    #configuration graphene
    'corsheaders',
    'graphene_django',
    #config graphene auth
    "graphql_jwt.refresh_token.apps.RefreshTokenConfig",
    "graphql_auth",
    "django_filters",
    'tinymce',
   
]

DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

LOCAL_APPS = [
    'users',
    'banners',
    'newsletters',
    'products',
    'purchases',
    
   
]

INSTALLED_APPS = DJANGO_PACKAGES + DJANGO_APPS + LOCAL_APPS

AUTH_USER_MODEL = 'users.CustomUser'

REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema' , # <-- Here
    'DEFAULT_FILTER_BACKENDS': ('django_filters.rest_framework.DjangoFilterBackend',),

}



MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    
   
]

X_FRAME_OPTIONS = 'ALLOWALL'

CORS_ALLOW_ALL_ORIGINS =True


#CORS_ALLOWED_ORIGINS = ['*']


ROOT_URLCONF = 'config.urls'
LOGIN_URL = '/'
LOGIN_REDIRECT_URL = '/admin/purchases/commandes/'
LOGOUT_REDIRECT_URL = '/admin/'
TEMPLATE_DIR = os.path.join(
    BASE_DIR, "config/templates")  # ROOT dir for templates

CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]
'''CORS_ALLOWED_ORIGINS = [
    'http://127.0.0.1:8000/',
] '''# If this is used, then not need to use `CORS_ALLOW_ALL_ORIGINS = True`

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"

CRISPY_TEMPLATE_PACK = "bootstrap5"

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATE_DIR],
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


WSGI_APPLICATION = 'config.wsgi.application'




# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = db.MYSQL

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 8,  # Remplacez la valeur par la longueur minimale souhaitée
        }
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'fr-FR'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

DATE_FORMAT = 'Y-m-d'
TIME_FORMAT = 'H:i:s'
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

'''STATIC_URL = '/static/'
STATIC_ROOT = '/home/c2154647c/public_html/hamstore/static/'

MEDIA_URL = '/media/'
MEDIA_ROOT = '/home/c2154647c/public_html/hamstore/media/'

# Extra places for collectstatic to find static files.
STATICFILES_DIRS = (os.path.join('static'),)'''


STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

# Extra places for collectstatic to find static files.
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'config/../config/static/'),
)
#TINYMCE_JS_URL = os.path.join(STATIC_URL, "path/to/tiny_mce/tiny_mce.js")

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

JAZZMIN_SETTINGS = {
    # title of the window (Will default to current_admin_site.site_title if absent or None)
    "site_title": "Library Admin",

   
}




GRAPHENE = {
    'SCHEMA': 'config.schema.schema' ,# Where your Graphene schema lives
    'MIDDLEWARE': [
        'graphql_jwt.middleware.JSONWebTokenMiddleware',
    ],
}

'''GRAPHENE_DJANGO_EXTRAS = {
    'DEFAULT_PAGINATION_CLASS': 'graphene_django_extras.paginations.LimitOffsetGraphqlPagination',
    'DEFAULT_PAGE_SIZE': 20,
    'MAX_PAGE_SIZE': 50,
    'CACHE_ACTIVE': True,
    'CACHE_TIMEOUT': 300    # seconds
}'''

AUTHENTICATION_BACKENDS = [
    'graphql_auth.backends.GraphQLAuthBackend',
    'django.contrib.auth.backends.ModelBackend',
    #'graphql_jwt.backends.JSONWebTokenBackend',   
]



GRAPHQL_JWT = {
    'JWT_ALLOW_ARGUMENT': True,
    
    "JWT_VERIFY_EXPIRATION": True,
    "JWT_EXPIRATION_DELTA": timedelta(minutes=5),
    # optional
    "JWT_LONG_RUNNING_REFRESH_TOKEN": True,
    'JWT_PAYLOAD_HANDLER': 'users.schema.jwt_payload',
    "JWT_ALLOW_ANY_CLASSES": [
        "graphql_auth.mutations.Register",
        "graphql_auth.mutations.VerifyAccount",
        "graphql_auth.mutations.ResendActivationEmail",
        "graphql_auth.mutations.SendPasswordResetEmail",
        "graphql_auth.mutations.PasswordReset",
        "graphql_auth.mutations.ObtainJSONWebToken",
        "graphql_auth.mutations.VerifyToken",
        "graphql_auth.mutations.RefreshToken",
        "graphql_auth.mutations.RevokeToken",
        "graphql_auth.mutations.VerifySecondaryEmail",
    ],
}


GRAPHQL_AUTH = {
   
    'REGISTER_MUTATION_FIELDS' : {
   
    'email': "String",
    'first_name': "String",
    'last_name': "String",
    'date_naissance': "String",
    'telephone': "String",
    #'abonnes_newsletters':'Boolean',
    
    },
    'REGISTER_MUTATION_FIELDS_OPTIONAL':['username', 'password2'],
    'LOGIN_ALLOWED_FIELDS': ['email'],
    'UPDATE_MUTATION_FIELDS':["first_name", "last_name", "date_naissance", "telephone"],
    "USE_JWT_REFRESH_TOKENS": True,

}

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_TIMEOUT = 20
EMAIL_USE_TLS = True
#EMAIL_USE_SSL = True
EMAIL_HOST = 'mail.cabinetfirdaws.org'
EMAIL_HOST_USER = 'contact@cabinetfirdaws.org'
EMAIL_HOST_PASSWORD = 'Abdelakim8810@'
EMAIL_PORT =  587
EMAIL_SUBJECT_PREFIX = 'Athehams : '
#---------------------- EMAIL CONFIG ----------------------
'''EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST ='mail.athehams.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True 
DEFAULT_FROM_EMAIL = "Athehams Boutique" 
EMAIL_HOST_USER =  "contact@athehams.com"
EMAIL_HOST_PASSWORD = "Hamed@2023"'''





JAZZMIN_SETTINGS = {
    "site_title": "Athehams",
    "site_header": "Boutique Athehams",
    "site_brand": "Athehams",
    "site_icon": "assets/img/logo.png",    
    # Add your own branding here
    "site_logo": "assets/img/oh.png",
    "welcome_sign": "Bienvenue sur Athehams",
    # Copyright on the footer
    "copyright": "IT System",
    "user_avatar": None,
    ############
    # Top Menu #
    ############
    # Links to put along the top menu
    "topmenu_links": [
        # Url that gets reversed (Permissions can be added)
        {"name": "Accueil",  "url": "admin:index", "permissions": ["auth.view_user"]},
        {"model": "auth.User"},
    ],
    #############
    # Side Menu #
    #############
    # Whether to display the side menu
    "show_sidebar": True,
    # Whether to aut expand the menu
    "navigation_expanded": True,
    # Custom icons for side menu apps/models See https://fontawesome.com/icons?d=gallery&m=free&v=5.0.0,5.0.1,5.0.10,5.0.11,5.0.12,5.0.13,5.0.2,5.0.3,5.0.4,5.0.5,5.0.6,5.0.7,5.0.8,5.0.9,5.1.0,5.1.1,5.2.0,5.3.0,5.3.1,5.4.0,5.4.1,5.4.2,5.13.0,5.12.0,5.11.2,5.11.1,5.10.0,5.9.0,5.8.2,5.8.1,5.7.2,5.7.1,5.7.0,5.6.3,5.5.0,5.4.2
    #"hide_apps": [ "auth", "refresh_token"],
    "hide_models": ['products.descriptionprecise'],
    "order_with_respect_to": ["banners", "newsletters", "products", "purchases", "users", "sessions"],
    "icons": {
        
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",
        "auth.Group": "fas fa-users",
        "users.customuser": "fas fa-users",
        "products.category":"fas fa-tags",
        "products.products":"fas fa-shopping-cart",
        "products.event":"fas  fa-universal-access",
        "products.commentaires":"fas fa-comment",
        "products.subcategory":"fas fa-tag",
        "products.variantes":"fas fa-store",
        "banners.banners":"fas fa-bullhorn",
        "purchases.commandes":"fas fa-chart-bar",
        "purchases.produitscommandes":"fas fa-calendar-check",
         "purchases.transactions":"fas fa-chart-line",

    },
    # for the full list of 5.13.0 free icon classes
    # # Icons that are used when one is not manually specified
    "default_icon_parents": "fas fa-chevron-circle-right",
    "default_icon_children": "fas fa-arrow-circle-right",
    #################
    # Related Modal #
    #################
    # Use modals instead of popups
    "related_modal_active": True,
    #############
    # UI Tweaks #
    #############
    # Relative paths to custom CSS/JS scripts (must be present in static files)
    # Uncomment this line once you create the bootstrap-dark.css file
    "custom_css": "assets/css/customiz_admin.css",
    # Background image for the login page
    "login_bg": "assets/img/bg.jpg",
    "custom_js": "assets/js/customiz_admin.js",
    # Whether to show the UI customizer on the sidebar
    "show_ui_builder": True,
    ###############
    # Change view #
    ###############
    "changeform_format": "horizontal_tabs",
    # override change forms on a per modeladmin basis
    "changeform_format_overrides": {
        "auth.user": "collapsible",
        "auth.group": "vertical_tabs",
    },
}

JAZZMIN_UI_TWEAKS = {
    "navbar_small_text": False,
    "footer_small_text": True,
    "body_small_text": False,
    "brand_small_text": False,
    "brand_colour": "navbar-info",
    "accent": "accent-info",
    "navbar": "navbar-info navbar-dark",
    "no_navbar_border": True,
    "navbar_fixed": False,
    "layout_boxed": False,
    "footer_fixed": True,
    "sidebar_fixed": True,
    "sidebar": "sidebar-light-info",
    "sidebar_nav_small_text": False,
    "sidebar_disable_expand": True,
    "sidebar_nav_child_indent": True,
    "sidebar_nav_compact_style": False,
    "sidebar_nav_legacy_style": False,
    "sidebar_nav_flat_style": True,
    "theme": "pulse",
    "dark_mode_theme": None,
    "button_classes": {
        "primary": "btn-outline-primary",
        "secondary": "btn-outline-secondary",
        "info": "btn-outline-info",
        "warning": "btn-outline-warning",
        "danger": "btn-outline-danger",
        "success": "btn-outline-success"
    },
    "actions_sticky_top": True
}

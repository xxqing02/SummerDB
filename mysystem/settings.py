"""
Django settings for mysystem project.

Generated by 'django-admin startproject' using Django 3.2.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from pathlib import Path
import os
# Build paths inside the project like this: BASE_DIR / 'subdir'.


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-gqk=shjay3ltisipnxvf0oo%(-+#b&$i(3ou@v@klk6wn76svz'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*","47.121.116.241","app6321.acapp.acwing.com.cn","127.0.0.1"]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'mmm',
]
#CORS_ALLOW_ALL_ORIGINS = True

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    #'corsheaders.middleware.CorsMiddleware',#解决跨域访问
    #'django.middleware.common.CommonMiddleware',#解决跨域访问
]

# SESSION_ENGINE = "django.contrib.sessions.backends.cache"
# SESSION_COOKIE_NAME  = "sessionid"
# SESSION_COOKIE_PATH  = "/"
# SESSION_COOKIE_DOMAIN = None
# SESSION_COOKIE_SECURE = False
# SESSION_COOKIE_HTTPONLY = True
# SESSION_COOKIE_AGE = 1209600
# SESSION_EXPIRE_AT_BROWSER_CLOSE = False
# SESSION_SAVE_EVERY_REQUEST = False

ROOT_URLCONF = 'mysystem.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join('template')],
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

WSGI_APPLICATION = 'mysystem.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'dragon',
        'USER': 'root',
        'PASSWORD': '123456',
        'HOST': 'localhost',
        'PORT': '3306',
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
BASE_DIR = Path(__file__).resolve().parent.parent
ROOT_DIR = Path(__file__).resolve().parent.parent.parent

STATIC_ROOT = os.path.join(BASE_DIR,'staticfiles')

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]


# media
MEDIA_URL = "/media/"  # 自定义
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')  # 自定义
if os.path.isdir(MEDIA_ROOT) == False:
    os.mkdir(MEDIA_ROOT)

CSRF_TRUSTED_ORIGINS = [
    'https://servicewechat.com',
]

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

"""
Django settings for VirtualBank project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'qg2vb7c+hgj&wzomrxq@z+-1vvsrq#*h+4z5#)9p28+uc69!26'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

#ALLOWED_HOSTS = ["127.0.0.1"]
ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'myBank',
    #'captcha',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    #'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'VirtualBank.urls'

WSGI_APPLICATION = 'VirtualBank.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', 
        'NAME': 'VirtualBankDB_1',    
        'USER': 'root',
        'PASSWORD': 'root',
        'HOST': '',
        'PORT': '3306',

    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

SESSION_EXPIRE_AT_BROWSER_CLOSE = True
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'


TEMPLATE_DIRS = (
'./myBank/TEMPLATE/',
)

#--Email set--#
EMAIL_HOST = 'smtp.sina.com'                   #SMTP Address
EMAIL_PORT = 25                                 #SMTP Port
EMAIL_HOST_USER = 'virtualbankbylcl@sina.com'       #My Emailname
EMAIL_HOST_PASSWORD = 'lcldeVirtualBank'                  #My Emailpassword
EMAIL_SUBJECT_PREFIX = u'[VirtualBank]'           #set Subject-line prefix,default is '[django]'
EMAIL_USE_TLS = True                            #default is false
#Manager
SERVER_EMAIL = 'lclbangong@163.com'           #The email address that error messages come from, such as those sent to ADMINS and MANAGERS.


#-----#
#SOUTH_MIGRATION_MODULES = {
#    'captcha': 'captcha.south_migrations',

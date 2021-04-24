from neige_soleil_django.settings.commons import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = 'True'

ALLOWED_HOSTS = ['*']

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'BTS_Neige_Soleil',
        'USER': 'root',
        'PASSWORD': 'root',
        'PORT': '3306',
        'HOST': '/Applications/MAMP/tmp/mysql/mysql.sock',
    }
}

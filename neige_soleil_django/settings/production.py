import os
import custom_azure
from neige_soleil_django.settings.commons import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ['SECRET_KEY']

# SECURITY WARNING: don't run with debug turned on in production!
# TODO: Check the String value of Debug for implementing Boolean
DEBUG = False

ALLOWED_HOSTS = ['127.0.0.1', 'neigesoleil-app.azurewebsites.net']

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ['DB_NAME'],
        'USER': os.environ['DB_USER'],
        'PASSWORD': os.environ['DB_PASSWORD'],
        'HOST': os.environ['DB_HOST'],
        'PORT': os.environ['DB_PORT']
    }
}


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

DEFAULT_FILE_STORAGE = 'custom_azure.AzureMediaStorage'
STATICFILES_STORAGE = 'custom_azure.AzureStaticStorage'

# any static paths you want to publish
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
]


STATIC_LOCATION = "neigesoleil-static"
MEDIA_LOCATION = "neigesoleil-media"

AZURE_ACCOUNT_NAME = "neigesoleilstorage"
AZURE_CUSTOM_DOMAIN = f'{AZURE_ACCOUNT_NAME}.blob.core.windows.net'
STATIC_URL = f'https://{AZURE_CUSTOM_DOMAIN}/{STATIC_LOCATION}/'
MEDIA_URL = f'https://{AZURE_CUSTOM_DOMAIN}/{MEDIA_LOCATION}/'









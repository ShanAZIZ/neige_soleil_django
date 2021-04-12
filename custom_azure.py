import os

from storages.backends.azure_storage import AzureStorage
from decouple import config

if os.environ['DJANGO_SETTINGS_MODULE'] == 'neige_soleil_django.settings.development':
    STORAGE_ACCOUNT_NAME = config('STORAGE_ACCOUNT_NAME')
    STORAGE_KEY = config('STORAGE_KEY')
else:
    STORAGE_ACCOUNT_NAME = os.environ['STORAGE_ACCOUNT_NAME']
    STORAGE_KEY = os.environ['STORAGE_KEY']

# STORAGE_ACCOUNT_NAME = os.environ['STORAGE_ACCOUNT_NAME']
# STORAGE_KEY = os.environ['STORAGE_KEY']


class AzureStaticStorage(AzureStorage):
    def path(self, name):
        pass

    def get_accessed_time(self, name):
        pass

    def get_created_time(self, name):
        pass

    account_name = STORAGE_ACCOUNT_NAME
    account_key = STORAGE_KEY
    azure_container = 'neigesoleil-static'
    expiration_secs = None


class AzureMediaStorage(AzureStorage):
    def path(self, name):
        pass

    def get_accessed_time(self, name):
        pass

    def get_created_time(self, name):
        pass

    account_name = STORAGE_ACCOUNT_NAME
    account_key = STORAGE_KEY
    azure_container = 'neigesoleil-media'
    expiration_secs = None

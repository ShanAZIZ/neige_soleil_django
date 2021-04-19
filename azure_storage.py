from storages.backends.azure_storage import AzureStorage
from decouple import config


class AzureMediaStorage(AzureStorage):
    def get_accessed_time(self, name):
        pass

    def get_created_time(self, name):
        pass

    def path(self, name):
        pass

    account_name = 'neigesoleilstorage'
    account_key = config('STORAGE_KEY')
    azure_container = 'neigesoleil-media'
    expiration_secs = None


class AzureStaticStorage(AzureStorage):
    def path(self, name):
        pass

    def get_accessed_time(self, name):
        pass

    def get_created_time(self, name):
        pass

    account_name = 'neigesoleilstorage'
    account_key = config('STORAGE_KEY')
    azure_container = 'neigesoleil-static'
    expiration_secs = None
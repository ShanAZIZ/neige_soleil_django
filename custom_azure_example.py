from storages.backends.azure_storage import AzureStorage


class AzureStaticStorage(AzureStorage):
    def path(self, name):
        pass

    def get_accessed_time(self, name):
        pass

    def get_created_time(self, name):
        pass

    account_name = ''
    account_key = ''
    azure_container = 'neigesoleil-static'
    expiration_secs = None
    

class AzureMediaStorage(AzureStorage):
    def path(self, name):
        pass

    def get_accessed_time(self, name):
        pass

    def get_created_time(self, name):
        pass

    account_name = ''
    account_key = ''
    azure_container = ''
    expiration_secs = None
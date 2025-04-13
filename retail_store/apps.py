from django.apps import AppConfig

class RetailStoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'retail_store'

    def ready(self):
        import retail_store.signals

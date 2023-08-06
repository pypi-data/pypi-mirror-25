from django.apps import AppConfig


class PlenarioApiConfig(AppConfig):
    name = 'plenario_api'

    def ready(self):
        from . import signals

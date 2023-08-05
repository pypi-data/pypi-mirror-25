from django.apps import AppConfig as DjangoAppConfig


class AppConfig(DjangoAppConfig):
    name = 'tsdummy'
    verbose_name = "Dummy Service"
    label = 'services_dummy'

    def ready(self):
        from .handler import DummyServicePlugin

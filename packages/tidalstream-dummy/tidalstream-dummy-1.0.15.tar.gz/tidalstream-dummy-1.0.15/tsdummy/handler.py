import urllib

from django.conf.urls import url

from marshmallow import Schema, fields

from tidalstream.plugins import ServicePlugin

from .views import DummyView


class DummyServicePlugin(ServicePlugin):
    plugin_name = 'dummy'
    config_schema = Schema
    permission_classes = DummyView.permission_classes

    def get_urls(self):
        return [
            url('^/?$', DummyView.as_view(service=self))
        ]

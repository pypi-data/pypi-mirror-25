import logging

from django.http import Http404

from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response

from tidalstream.jsonapi import JSONAPIObject, JSONAPIRoot
from tidalstream.plugins import CascadingPermission

logger = logging.getLogger(__name__)


class DummyView(APIView):
    service = None

    permission_classes = (permissions.AllowAny , )

    def get(self, request):
        logger.debug('Dummy module called')

        root = JSONAPIRoot()
        obj = JSONAPIObject('dummy', 'dummy_id')
        root.append(obj)

        return Response(root.serialize(request))

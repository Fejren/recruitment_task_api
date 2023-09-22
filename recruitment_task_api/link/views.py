from rest_framework import mixins, viewsets
from rest_framework.response import Response

from .models import ExpiringLink
from .serializers import ExpiringLinkSerializer


class ExpiringLinkViewSet(mixins.CreateModelMixin,
                          mixins.RetrieveModelMixin,
                          viewsets.GenericViewSet):
    queryset = ExpiringLink.objects.none()
    serializer_class = ExpiringLinkSerializer

    def retrieve(self, request, *args, **kwargs):
        link_id = kwargs.get('id')
        return Response(
            {
                'link_id': link_id
            }
        )

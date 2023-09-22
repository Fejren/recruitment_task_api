from django.http import HttpResponseRedirect
from django.utils import timezone
from rest_framework import mixins, viewsets, status
from rest_framework.generics import get_object_or_404
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
        expiring_link_model = get_object_or_404(ExpiringLink, id=link_id)
        current_time = timezone.now()
        if expiring_link_model.expires_at <= current_time:
            return Response({'message': 'Link expired'},
                            status=status.HTTP_400_BAD_REQUEST)
        else:
            return HttpResponseRedirect(redirect_to=expiring_link_model.image)

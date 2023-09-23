from django.http import HttpResponseRedirect

from rest_framework import mixins, viewsets, status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from .generate_expiring_link import is_link_expired
from .models import ExpiringLink
from .serializers import ExpiringLinkSerializer


class ExpiringLinkViewSet(mixins.CreateModelMixin,
                          mixins.RetrieveModelMixin,
                          viewsets.GenericViewSet):
    queryset = ExpiringLink.objects.none()
    serializer_class = ExpiringLinkSerializer

    def retrieve(self, request, *args, **kwargs):
        link_id = kwargs.get('id')  # Get link id from the url
        expiring_link_model = get_object_or_404(ExpiringLink, id=link_id)
        if is_link_expired(expiring_link_model):
            return Response({'message': 'Link expired'},
                            status=status.HTTP_400_BAD_REQUEST)
        else:
            # Redirect to image
            return HttpResponseRedirect(redirect_to=expiring_link_model.image)

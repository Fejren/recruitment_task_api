from django.urls import path

from .views import ExpiringLinkViewSet

app_name = 'link'

urlpatterns = [
    path('<uuid:id>', ExpiringLinkViewSet.as_view({'get': 'retrieve'}), name='expiring-link-retrieve'),
]

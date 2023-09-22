from django.urls import path

from .views import ImageCreateViewSet


urlpatterns = [
    path('', ImageCreateViewSet.as_view({'post': 'create'}), name='image-create'),
]

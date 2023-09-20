from django.urls import path

from .views import ImageCreateAndRetrieveViewSet


urlpatterns = [
    path('', ImageCreateAndRetrieveViewSet.as_view({'post': 'create'}), name='image-create-retrieve'),
]

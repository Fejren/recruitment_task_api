from django.urls import path

from image.views import ImageCreateViewSet, ImageRetrieveViewSet

app_name = 'image'

urlpatterns = [
    path('', ImageCreateViewSet.as_view({'post': 'create'}),
         name='image-create'),

    path('<uuid:user>', ImageRetrieveViewSet.as_view({'get': 'retrieve'}),
         name='image-retrieve'),
]

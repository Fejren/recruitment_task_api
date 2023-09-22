from django.urls import path

from .views import ImageCreateViewSet

app_name = 'image'

urlpatterns = [
    path('', ImageCreateViewSet.as_view({'post': 'create'}), name='image-create'),
]

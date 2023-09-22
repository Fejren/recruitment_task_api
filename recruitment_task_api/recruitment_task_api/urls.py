from django.conf import settings
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/images/', include('image.urls')),
    path('api/images/link/', include('link.urls')),
]
if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()

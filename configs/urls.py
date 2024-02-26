from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api-auth/", include("rest_framework.urls")),
    path("api_v1/", include("api.routes")),
]

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()

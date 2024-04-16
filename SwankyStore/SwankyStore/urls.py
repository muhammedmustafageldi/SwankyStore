from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns # new
from django.views.static import serve

urlpatterns = [
    path("", include("mainApp.urls")),
    path("admin/", admin.site.urls),
    path("", include("django.contrib.auth.urls")),
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

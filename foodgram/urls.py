"""foodgram URL Configuration."""
import debug_toolbar
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("auth/", include("users.urls")),
    path("auth/", include("django.contrib.auth.urls")),
    path("admin/", admin.site.urls),
    path("api/", include("api.urls")),
    path("about/", include("about.urls", namespace='about')),
    path("", include("recipes.urls")),
]

handler404 = "foodgram.views.page_not_found"  # noqa
handler500 = "foodgram.views.server_error"  # noqa


if settings.DEBUG:
    # for django-debug-toolbar
    urlpatterns += (path("__debug__/", include(debug_toolbar.urls)),)

    # for debug media
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
    urlpatterns += static(
        settings.STATIC_URL, document_root=settings.STATIC_ROOT
    )

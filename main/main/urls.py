from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


handler404 = 'news.views.error_404'

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', include('news.urls')),
    path('users/', include('users.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if settings.DEBUG:
    import debug_toolbar
    urlpatterns= [
        path("__debug/__", include(debug_toolbar.urls)), ] + urlpatterns

    urlpatterns +static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


admin.site.site_header = 'Административная панель'
admin.site.index_title = 'Административная панель'
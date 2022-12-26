from django.contrib import admin
from django.urls import path, include
from . import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
    path('account/', include('account.urls')),
    path('contact/', include('contact.urls')),
    path('shop/', include('shop.urls')),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()
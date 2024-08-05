from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from books.views import index


urlpatterns = [
    path('', index, name='index'),
    path("admin/", admin.site.urls),
    path('api/books/', include('books.urls')),
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])

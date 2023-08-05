"""labeler_site URL Configuration

References:
  [Django docs](https://docs.djangoproject.com/en/1.11/topics/http/urls/)
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include('labeler.urls')),
    # url(r'^', include('example_app.urls', namespace='example_app')),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

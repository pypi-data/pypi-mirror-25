from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static

from . import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    # class-based REST API view ov images
    url(r'^api/images/$', views.ListImages.as_view()),
    url(r'^upload/$', views.form_file_upload, name='form_file_upload'),
    url(r'^api/$', views.ListImages.as_view(), name='image_list'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^(?P<artist_id>[0-9]+)$', views.detail, name='artists-detail'),
    url(r'^$', views.index, name='index'),
]

from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^(?P<song_id>[0-9]+)$', views.detail, name='songs-detail'),
    url(r'^$', views.index, name='songs-index'),
]

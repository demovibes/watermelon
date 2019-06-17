from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^songs/', include('watermelon.apps.songs.urls')),
    url(r'^artists/', include('watermelon.apps.artists.urls')),
    url(r'^streams/', include('watermelon.apps.streams.urls')),
    url(r'^admin/', admin.site.urls),
]

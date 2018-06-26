from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^songs/', include('songs.urls')),
    url(r'^artists/', include('artists.urls')),
    url(r'^streams/', include('streams.urls')),
    url(r'^admin/', admin.site.urls),
]

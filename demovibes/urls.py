"""
URL configuration for demovibes project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView

urlpatterns = [
    # User_profile functions fit under user/
    path('user/', include('demovibes.user_profiles.urls')),
    # Other user account creation / mgmt
    path('accounts/', include('allauth.urls')),

    path('song/', include('demovibes.songs.urls')),
    path('artist/', include('demovibes.artists.urls')),

    path('collection/', include('demovibes.collections.urls')),

    # player / streams app
    path('', include('demovibes.player.urls')),
    path('playlist/', include('demovibes.playlist.urls')),

    path('chat/', include('demovibes.chat.urls')),

    # backend svc monitoring
    path('backend/', include('demovibes.backend.urls')),

    # events
    path('events/', include('demovibes.events.urls')),

    # admin documentation and main site
    path('admin/doc/', include('django.contrib.admindocs.urls')),
    path('admin/', admin.site.urls),

    path('', TemplateView.as_view(template_name='base/base.html'), name='index'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

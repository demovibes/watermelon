"""demovibes URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
    path('song/', include('songs.urls')),
    path('artist/', include('artists.urls')),

    # player / streams app
    path('', include('player.urls')),
    path('playlist/', include('playlist.urls')),

    path('user/', include('user_profiles.urls')),
    path('chat/', include('chat.urls')),

    path('backend/', include('backend.urls')),
    path('accounts/', include('django.contrib.auth.urls')),

    # events
    path('events/', include('events.urls')),

    # admin documentation and main site
    path('admin/doc/', include('django.contrib.admindocs.urls')),
    path('admin/', admin.site.urls),

    path('', TemplateView.as_view(template_name='base/base.html'), name='index'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

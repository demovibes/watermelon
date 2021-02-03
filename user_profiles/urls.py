from django.urls import path, re_path

from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from .models import Profile
from .views import ProfileUpdate

app_name = 'user_profiles'

urlpatterns = [
    re_path(r'^(?P<slug>[\w.@+-]+)/update/$', ProfileUpdate.as_view(), name='profile-update'),
    re_path(r'^(?P<slug>[\w.@+-]+)/$', DetailView.as_view( model=Profile, slug_field='user__username' ), name='profile-detail'),
    path('', ListView.as_view( model=Profile, paginate_by=100 ), name='profile-list'),
]

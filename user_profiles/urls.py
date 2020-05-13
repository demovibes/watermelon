from django.urls import path, re_path

from .views import ProfileDetail, ProfileList, ProfileUpdate

app_name = 'user_profiles'

urlpatterns = [
    re_path(r'^(?P<slug>[\w.@+-]+)/update/$', ProfileUpdate.as_view(), name='profile-update'),
    re_path(r'^(?P<slug>[\w.@+-]+)/$', ProfileDetail.as_view(), name='profile-detail'),
    path('', ProfileList.as_view(), name='profile-list'),
]

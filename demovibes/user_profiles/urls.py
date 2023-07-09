from django.urls import path

from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from .models import Profile
from .views import ProfileUpdate

app_name = 'user_profiles'

urlpatterns = [
    path('<slug>/update/', ProfileUpdate.as_view(), name='profile-update'),
    path('<slug>/', DetailView.as_view( model=Profile, slug_field='user__username' ), name='profile-detail'),
    path('', ListView.as_view( model=Profile, paginate_by=100 ), name='profile-list'),
]

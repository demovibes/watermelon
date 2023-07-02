from django.urls import path

from django.views.generic.list import ListView

from .models import Message
from .views import MessagePost

app_name = 'chat'

urlpatterns = [
    path('post/', MessagePost.as_view(), name='message-post'),
    path('', ListView.as_view( model=Message, paginate_by=100 ), name='message-list'),
]

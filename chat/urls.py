from django.urls import path

from .views import MessageList, MessagePost

app_name = 'chat'

urlpatterns = [
    path('', MessageList.as_view(), name='message-list'),
    path('post/', MessagePost.as_view(), name='message-post'),
]

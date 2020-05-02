from django.urls import path
from .views import MessageListView, MessagePostView

urlpatterns = [
    path('', MessageListView.as_view(), name='message-list-view'),
    path('post/', MessagePostView.as_view(), name='message-post-view'),
]

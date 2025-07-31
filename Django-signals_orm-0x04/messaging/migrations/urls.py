from django.urls import path
from messaging.views import (
    CachedConversationView,
    UnreadMessagesView,
    MessageListCreateView
)

urlpatterns = [
    path('messages/', MessageListCreateView.as_view(), name='message-list-create'),
    path('messages/conversation/', CachedConversationView.as_view(), name='cached-conversation'),
    path('messages/unread/', UnreadMessagesView.as_view(), name='unread-messages'),
]
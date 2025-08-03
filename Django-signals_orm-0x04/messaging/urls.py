from django.urls import path
from .views import delete_user
from .views import ThreadedMessageListView, UnreadMessagesView
urlpatterns = [
    path('delete/account', delete_user, name="delete_account"),
    path('messages/threaded/', ThreadedMessageListView.as_view(), name='threaded-messages'),
    path('messages/unread', UnreadMessagesView.as_view(), name="unread-messages")
]
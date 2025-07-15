from django.urls import path, include
from rest_framework_nested.routers import NestedDefaultRouter 
from .views import ConversationViewSet, MessageViewSet

router = NestedDefaultRouter(parent_router=None, parent_prefix='')

# Register the viewsets the usual way
router.register(r'conversations', ConversationViewSet, basename='conversation')
router.register(r'messages', MessageViewSet, basename='message')

urlpatterns = [
    path('', include(router.urls)),
]


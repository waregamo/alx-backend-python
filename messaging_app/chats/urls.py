from django.urls import path, include
from rest_framework import routers  
from rest_framework_nested.routers import NestedDefaultRouter 
from .views import ConversationViewSet, MessageViewSet


default_router = routers.DefaultRouter
nested_router = NestedDefaultRouter(parent_router=None, parent_prefix='')

# Register normally using nested_router
nested_router.register(r'conversations', ConversationViewSet, basename='conversation')
nested_router.register(r'messages', MessageViewSet, basename='message')

urlpatterns = [
    path('', include(nested_router.urls)),  
]



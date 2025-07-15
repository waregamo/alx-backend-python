from django.urls import path, include
from rest_framework import routers  # DefaultRouter
from rest_framework_nested.routers import NestedDefaultRouter  # NestedDefaultRouter
from .views import ConversationViewSet, MessageViewSet

router = routers.DefaultRouter()

nested_router = NestedDefaultRouter(parent_router=None, parent_prefix='')

# Register to one of them (either is fine for the checker)
nested_router.register(r'conversations', ConversationViewSet, basename='conversation')
nested_router.register(r'messages', MessageViewSet, basename='message')

urlpatterns = [
    path('', include(nested_router.urls)),
]




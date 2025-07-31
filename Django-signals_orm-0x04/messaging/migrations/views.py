from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User
from messaging.models import Message
from messaging.serializers import MessageSerializer
from rest_framework.decorators import api_view, permission_classes

class MessageListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = MessageSerializer

    def get_queryset(self):
        return Message.objects.filter(receiver=self.request.user, sender=self.request.user).select_related('sender').prefetch_related('replies').only('id', 'sender', 'receiver', 'content', 'timestamp')

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)

@method_decorator(cache_page(60), name='dispatch')
class CachedConversationView(MessageListCreateView):
    pass

class UnreadMessagesView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = MessageSerializer

    def get_queryset(self):
        return Message.unread.unread_for_user(self.request.user)

@api_view(['DELETE'])
@permission_classes([permissions.IsAuthenticated])
def delete_user(request):
    user = request.user
    user.delete()
    return Response({"detail": "User account deleted."}, status=status.HTTP_204_NO_CONTENT)
    
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def create_message(request):
    serializer = MessageSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(sender=request.user)
        return Response({"message": "Message sent successfully"}, status=status.HTTP_201_CREATED)
    return Response({"message": "Failed to save message to the database"}, status=status.HTTP_400_BAD_REQUEST)
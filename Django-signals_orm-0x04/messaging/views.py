from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.views import APIView
from .serializers import MessageThreadSerializer, MessageSerializer
from .models import Message
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page


@api_view(['DELETE'])
def delete_user(request):
    user = request.user
    user.delete()
    return Response({"detail": "User account deleted successfully."}, status=HTTP_204_NO_CONTENT)
class ThreadedMessageListView(APIView):
    @method_decorator(cache_page(60))
    def get(self, request):
        messages = Message.objects.filter(
                parent_message__isnull=True,
                sender=request.user
                ) | Message.objects.filter(
                    parent_message__isnull=True,
                    receiver=request.user
                )\
            .select_related("receiver")\
                .prefetch_related(
                    'replies',
                    'replies__replies',
                    'replies__sender',
                    'replies__replies__sender'
                )
        serializer = MessageThreadSerializer(messages, many=True)
        return Response(serializer.data)

class UnreadMessagesView(APIView):
    def get(self, request):
        unread_messages = Message.unread.unread_for_user(request.user).only('id', 'sender', 'content', 'timestamp')
        serializer = MessageSerializer(unread_messages, many=True)
        return Response(serializer.data)
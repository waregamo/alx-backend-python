from rest_framework import serializers
from messaging.models import Message, MessageHistory

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'sender', 'receiver', 'content', 'timestamp', 'edited', 'edited_by', 'parent_message', 'read']

class MessageHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = MessageHistory
        fields = ['id', 'message', 'old_content', 'edited_at']
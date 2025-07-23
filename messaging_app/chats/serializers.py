from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Conversation, Message

User = get_user_model()

# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user_id', 'username', 'email', 'bio']


# Message Serializer
class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    conversation = serializers.UUIDField(write_only=True)

    class Meta:
        model = Message
        fields = ['message_id', 'sender', 'conversation', 'message_body', 'sent_at']
        read_only_fields = ['sender', 'sent_at']

    def create(self, validated_data):
        validated_data['sender'] = self.context['request'].user
        return super().create(validated_data)


# Conversation Serializer
class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    messages = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants', 'messages', 'created_at']
        read_only_fields = ['created_at']

    def get_messages(self, obj):
        """Returns serialized messages for a conversation"""
        messages = obj.messages.order_by('sent_at')
        return MessageSerializer(messages, many=True, context=self.context).data

    def validate(self, data):
        if self.context.get('request') and self.context['request'].method == 'POST':
            if not self.context['request'].user.is_authenticated:
                raise serializers.ValidationError("User must be authenticated.")
        return data



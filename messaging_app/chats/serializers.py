from rest_framework import serializers
from .models import User, Conversation, Message

# User Serializer
class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField()  # 

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'bio']

# Message Serializer
class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)

    class Meta:
        model = Message
        fields = ['id', 'sender', 'conversation', 'content', 'timestamp']
        read_only_fields = ['sender', 'timestamp']

# Conversation Serializer with nested messages
class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    messages = serializers.SerializerMethodField()  

    class Meta:
        model = Conversation
        fields = ['id', 'participants', 'messages', 'created_at']
        read_only_fields = ['created_at']

    def get_messages(self, obj):
        """Returns serialized messages for a conversation"""
        messages = obj.messages.order_by('timestamp')
        return MessageSerializer(messages, many=True).data

    def validate(self, data):
        """Example validation to include ValidationError"""
        if self.context.get('request') and self.context['request'].method == 'POST':
            if not self.context['request'].user.is_authenticated:
                raise serializers.ValidationError("User must be authenticated.")
        return data


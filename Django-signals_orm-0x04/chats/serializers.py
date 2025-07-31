from rest_framework import serializers
from .models import CustomUser, Conversation, Message

class UserSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField()
    class Meta:
        model = CustomUser
        fields = ['user_id', 'username', 'email', 'display_name', 'first_name', 'last_name', 'phone_number']

class MessageSerializer(serializers.ModelSerializer):
    sender_name = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = ['message_id', 'sender', 'sender_name', 'message_body', 'sent_at', 'conversation']

    def get_sender_name(self, obj):
        return obj.sender.username

class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants', 'messages', 'created_at']

    def validate(self, data):
        if not data.get("participants"):
            raise serializers.ValidationError("A conversation must have participants.")
        return data
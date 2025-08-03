from rest_framework import serializers
from .models import Message

class RecursiveMessageSerializer(serializers.Serializer):
    def to_representation(self, value):
        serializer = MessageThreadSerializer(value, context=self.context)
        return serializer


class MessageThreadSerializer(serializers.ModelSerializer):
    replies = RecursiveMessageSerializer(many=True, read_only=True)

    class Meta:
        model=Message
        fields = ['id', 'sender','receiver', 'content', 'timestamp', 'replies']

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'sender', 'content', 'timestamp']  # Only necessary fields
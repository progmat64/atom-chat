from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from chat.models import Channel, Message
from users.models import User


class RegistrationSerializer(serializers.ModelSerializer):
    def validate_password(self, value):
        return make_password(value)  # Хеширование пароля

    class Meta:
        model = User
        fields = ("email", "username", "first_name", "last_name", "password")


class UserPublicSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            "email",
            "username",
            "first_name",
            "last_name",
        )


class UserModeratorSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            "email",
            "username",
            "first_name",
            "last_name",
            "is_blocked",
        )


class ChannelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Channel
        fields = ("id", "name", "description", "created_at", "updated_at")


class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.ReadOnlyField(source="sender.username")

    class Meta:
        model = Message
        fields = ("id", "channel", "sender", "content", "timestamp")
        extra_kwargs = {"channel": {"required": False}}

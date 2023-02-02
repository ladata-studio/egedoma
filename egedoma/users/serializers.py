from django.contrib.auth import authenticate
from rest_framework.serializers import (
    Serializer, ReadOnlyField, ModelSerializer, CharField, IntegerField, 
    ValidationError
)
from users.models import AuthHash, User

class TimestampField(ReadOnlyField):
    def to_representation(self, value):
        return int(value.timestamp())

class AuthHashSerializer(ModelSerializer):
    user = IntegerField(source='user.telegram_id')
    created_at = TimestampField()

    class Meta:
        model = AuthHash
        fields = ['hash', 'user', 'created_at', 'is_expired']


class UserSerializer(ModelSerializer):
    created_at = TimestampField()
    updated_at = TimestampField()

    class Meta:
        model = User
        fields = [
            'telegram_id', 'telegram_username', 'last_name', 'first_name',
            'photo', 'is_active', 'created_at', 'updated_at', 'is_superuser', 
        ]
        read_only_fields = ['updated_at']

    def update(self, instance, validated_data):
        for (key, value) in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance
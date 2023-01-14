from rest_framework.serializers import ReadOnlyField, ModelSerializer, CharField
from users.models import AuthHash, User

class TimestampField(ReadOnlyField):
    def to_representation(self, value):
        return int(value.timestamp())

class AuthHashSerializer(ModelSerializer):
    created = TimestampField()

    class Meta:
        model = AuthHash
        fields = ['hash', 'created_at', 'is_expired']


class UserSerializer(ModelSerializer):
    created_at = TimestampField()
    token = CharField(max_length=255, read_only=True)

    class Meta:
        model = User
        fields = [
            'telegram_id', 'telegram_username', 'last_name', 'first_name',
            'photo', 'is_active', 'created_at', 'token'
        ]

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
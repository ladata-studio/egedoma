from rest_framework.serializers import ReadOnlyField, ModelSerializer

from users.models import AuthHash, User

class TimestampField(ReadOnlyField):
    def to_representation(self, value):
        return int(value.timestamp())

class AuthHashSerializer(ModelSerializer):
    created = TimestampField()

    class Meta:
        model = AuthHash
        fields = ['hash', 'created', 'is_expired']


class UserSerializer(ModelSerializer):
    created = TimestampField()

    class Meta:
        model = User
        fields = [
            'telegram_id', 'telegram_username', 'last_name',
            'first_name', 'photo', 'is_active', 'created'
        ]
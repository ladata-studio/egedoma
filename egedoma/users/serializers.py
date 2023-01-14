from django.contrib.auth import authenticate
from rest_framework.serializers import Serializer, ReadOnlyField, ModelSerializer, CharField, IntegerField, ValidationError
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
    class Meta:
        model = User
        fields = [
            'telegram_id', 'telegram_username', 'last_name', 'first_name',
            'photo', 'is_active', 'created_at', 'updated_at', 'token'
        ]
        read_only_fields = ['token', 'updated_at']

    def update(self, instance, validated_data):
        for (key, value) in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance


class SignUpSerializer(ModelSerializer):
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


class SignInSerializer(Serializer):
    telegram_id = IntegerField()
    token = CharField(max_length=255, read_only=True)

    def validate(self, data):
        telegram_id = data.get('telegram_id', None)

        if telegram_id is None:
            raise ValidationError(
                'A telegram id is required to log in.'
            )

        user = authenticate(telegram_id=telegram_id)

        if user is None:
            raise ValidationError(
                'A user with this telegram id was not found or is not active.'
            )

        return {
            'telegram_id': user.telegram_id,
            'token': user.token
        }
from rest_framework_simplejwt.tokens import RefreshToken
import os

from django.utils import timezone

from users.models import AuthHash, User
from users.serializers import AuthHashSerializer


def verify_hash(hash):
    try:
        queryset = AuthHash.objects.get(hash=hash)
    except:
        return None

    serializer = AuthHashSerializer(queryset)
    data = serializer.data

    if data.get('is_expired'):
        return None

    timestamp = int(timezone.now().timestamp())
    data['timestamp'] = timestamp

    if timestamp - data.get('created_at') > int(os.getenv('HASH_LIFETIME')):
        queryset.is_expired = True
        queryset.save()

        serializer = AuthHashSerializer(queryset)
        data = serializer.data
        return None

    return queryset.user


def create_tokens(user: User):
    refresh = RefreshToken.for_user(user)
    tokens = {
        "access": str(refresh.access_token),
        "refresh": str(refresh)
    }

    return tokens

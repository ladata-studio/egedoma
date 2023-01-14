import os

from django.utils import timezone
from rest_framework.response import Response

from users.models import AuthHash, User
from users.serializers import AuthHashSerializer


def verify_hash(hash, telegram_id):
    try:
        user = User.objects.get(telegram_id=telegram_id)
        queryset = AuthHash.objects.get(hash=hash, user=user)
    except:
        return Response({
            'hash': {'hash': f'Hash {hash} for user {telegram_id} not found \
                in database.'
        }}, status=500)

    serializer = AuthHashSerializer(queryset)
    data = serializer.data

    if data.get('is_expired'):
        data = {'hash': data, 'error': 'This hash has expired'}
        return Response(data, status=500)

    timestamp = int(timezone.now().timestamp())
    data['timestamp'] = timestamp

    if timestamp - data.get('created_at') > int(os.getenv('HASH_LIFETIME')):
        queryset.is_expired = True
        queryset.save()

        serializer = AuthHashSerializer(queryset)
        data = serializer.data
        data = {'hash': data, 'error': 'This hash has expired'}
        return Response(data, status=500)

    data = {'hash': data}
    return Response(data, status=200)

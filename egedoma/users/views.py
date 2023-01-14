import os

from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response

from users.models import AuthHash, User
from users.serializers import AuthHashSerializer, UserSerializer


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class AuthHashViewSet(ModelViewSet):
    queryset = AuthHash.objects.all()
    serializer_class = AuthHashSerializer


class VerifyHash(APIView):
    def post(self, request):
        hash = request.data['hash']

        try:
            queryset = AuthHash.objects.get(hash=hash)
        except AuthHash.DoesNotExist:
            return Response({'hash': f'Hash {hash} not found in database.'}, status=500)

        serializer = AuthHashSerializer(queryset)
        data = serializer.data
        if data['is_expired']:
            return Response({'hash': f'Hash {hash} is expired.'}, status=500)

        timestamp = int(timezone.now().timestamp())
        data['timestamp'] = timestamp
        if timestamp - data['created'] > int(os.getenv('HASH_LIFETIME')):
            queryset.is_expired = True
            queryset.save()
            return Response({'hash': f'Hash {hash} is expired.'}, status=500)

        return Response(data, status=200)

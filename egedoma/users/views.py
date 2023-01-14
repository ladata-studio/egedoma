import os

from django.utils import timezone
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response

from users.models import AuthHash, User
from users.serializers import AuthHashSerializer, UserSerializer


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class SignUpAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer

    def post(self, request):
        user = request.data.get('user', {})
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=201)


class AuthHashViewSet(ModelViewSet):
    queryset = AuthHash.objects.all()
    serializer_class = AuthHashSerializer


class VerifyHashAPIView(APIView):
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

        # Если пользователь не найден в БД, то создать профиль и залогинить
        # Если пользователь найден, то просто залогинить
        # Но это сделать отдельными view

        return Response(data, status=200)

from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response

from users.models import AuthHash
from users.renderers import UserJSONRenderer
from users.serializers import AuthHashSerializer, SignUpSerializer, SignInSerializer, UserSerializer
from users.utils import verify_hash


class UserRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = UserSerializer

    def retrieve(self, request, *args, **kwargs):
        serializer = self.serializer_class(request.user)
        return Response(serializer.data, status=200)

    def update(self, request, *args, **kwargs):
        serializer_data = request.data.get('user', {})
        serializer = self.serializer_class(
            request.user, data=serializer_data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=200)


class SignUpAPIView(APIView):
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = SignUpSerializer

    def post(self, request):
        hash = request.data.get('hash', None)
        user = request.data.get('user', {})

        if hash is None:
            return Response({'hash': 'A hash must to be provided.'}, status=500)
        hash_response = verify_hash(hash)

        if hash_response.status_code != 200:
            return hash_response

        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=201)


class SignInAPIView(APIView):
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = SignInSerializer

    def post(self, request):
        hash = request.data.get('hash', None)
        user = request.data.get('user', {})

        if hash is None:
            return Response({'hash': 'A hash must to be provided.'}, status=500)
        hash_response = verify_hash(hash)

        if hash_response.status_code != 200:
            return hash_response

        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=200)


class AuthHashViewSet(ModelViewSet):
    queryset = AuthHash.objects.all()
    serializer_class = AuthHashSerializer
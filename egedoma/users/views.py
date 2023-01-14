from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from users.models import AuthHash, User
from users.renderers import UserJSONRenderer
from users.serializers import (
        AuthHashSerializer, SignInSerializer, SignUpSerializer, UserSerializer
)
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
        user = request.data.get('user', {})
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = serializer.data

        return Response(data, status=201)


class SignInAPIView(APIView):
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = SignInSerializer

    def post(self, request):
        user = request.data.get('user', {})

        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        data = serializer.data

        return Response(data, status=200)


class AuthHashAPIView(APIView):
    def post(self, request):
        try:
            user = request.data.get('user')
            try:
                user = User.objects.get(telegram_id=user['telegram_id'])
            except Exception as e:
                response = SignUpAPIView().post(request)
                if response.status_code != 201:
                    return response
                user = User.objects.get(telegram_id=user['telegram_id'])
            
            hash = request.data.get('hash')
            if hash is None:
                return Response(
                    {'hash': 'A hash must to be provided.'}, status=500
                )
        
            queryset = AuthHash.objects.create(hash=hash, user=user)
            serializer = AuthHashSerializer(queryset)
            data = serializer.data
            
            return Response(status=201, data=data)
        except Exception as e:
            return Response(status=500, data={'error': str(e)})
    
    def get(self, request):
        queryset = AuthHash.objects.all()
        serializer = AuthHashSerializer(queryset, many=True)
        data = serializer.data
        return Response(status=200, data=data)



class VerifyHash(APIView):
    def post(self, request):
        hash = request.data.get('hash', None)
        user = request.data.get('user', {})
        if hash is None:
            return Response({'hash': 'A hash must to be provided.'}, status=500)
        
        hash_response = verify_hash(hash, user['telegram_id'])
        if hash_response.status_code != 200:
            return hash_response
        
        # TODO: GENERATE JWT TOKEN
        # 

        token = ''
        
        data = {'user': user, 'token': token}
        
        return Response(data, status=200)

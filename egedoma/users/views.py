from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from users.models import AuthHash, User
from users.renderers import UserJSONRenderer
from users.serializers import UserSerializer
from users.utils import verify_hash, create_tokens


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


class CreateHashAPIView(APIView):
    def post(self, request):
        try:
            user = request.data.get('user', None)
            if user is None:
                return Response({'user': 'A user must to be provided.'}, status=500)
            try:
                telegram_id = user.pop('telegram_id')
                user, _ = User.objects.update_or_create(
                    telegram_id=telegram_id, defaults=user)
            except Exception as e:
                return Response(
                    {'user': f'Couldn\'t create or update a user. {e}'}, status=500
                )
            
            hash = request.data.get('hash')
            if hash is None:
                return Response(
                    {'hash': 'A hash must to be provided.'}, status=500
                )
        
            AuthHash.objects.create(hash=hash, user=user)
            
            return Response(status=201, data={'status': 'ok'})
        except Exception as e:
            return Response(status=500, data={'error': str(e)})


class VerifyHashAPIView(APIView):
    def post(self, request):
        hash = request.data.get('hash', None)
        if hash is None:
            return Response({'hash': 'A hash must to be provided.'}, status=500)
        
        user = verify_hash(hash)
        if user is None:
            return Response({'hash': 'Provided hash is not valid.'}, status=500)
    
        tokens = create_tokens(user)
        
        return Response(tokens, status=200)

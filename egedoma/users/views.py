from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response

from users.models import AuthHash, Student
from users.serializers import AuthHashSerializer, StudentSerializer


class StudentViewSet(ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    def create(self, request):
        response = super().create(request)
        instance = response.data
        return Response(instance, status=201)


class AuthHashViewSet(ModelViewSet):
    queryset = AuthHash.objects.all()
    serializer_class = AuthHashSerializer

    def create(self, request):
        response = super().create(request)
        instance = response.data

        print(request.data, flush=True)

        return Response(instance, status=201)
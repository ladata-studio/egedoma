from django.urls import path
from rest_framework.routers import SimpleRouter
from users.views import (UserRetrieveUpdateAPIView,
                         VerifyHash, CreateHashAPIView)

router = SimpleRouter()

urlpatterns = [
    path('create_hash/', CreateHashAPIView.as_view()),
    path('verify/', VerifyHash.as_view()),
    path('user/', UserRetrieveUpdateAPIView.as_view())
]
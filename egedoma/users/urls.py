from django.urls import path
from rest_framework.routers import SimpleRouter
from users.views import (
    SignUpAPIView, SignInAPIView, UserRetrieveUpdateAPIView, 
    VerifyHash, AuthHashAPIView
)

router = SimpleRouter()

urlpatterns = [
    path('signin/', SignInAPIView.as_view()),
    path('auth_hash/', AuthHashAPIView.as_view()),
    path('verify/', VerifyHash.as_view()),
    path('user/', UserRetrieveUpdateAPIView.as_view())
]
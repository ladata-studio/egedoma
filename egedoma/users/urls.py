from django.urls import path
from rest_framework.routers import SimpleRouter
from users.views import AuthHashViewSet, SignUpAPIView, SignInAPIView, UserRetrieveUpdateAPIView

router = SimpleRouter()
router.register('auth_hash', AuthHashViewSet)

urlpatterns = [
    path('signup/', SignUpAPIView.as_view()),
    path('signin/', SignInAPIView.as_view()),
    path('user/', UserRetrieveUpdateAPIView.as_view())
]
from django.urls import path
from rest_framework.routers import SimpleRouter
from users.views import AuthHashViewSet, UserViewSet, VerifyHashAPIView, SignUpAPIView

router = SimpleRouter()
router.register(r'auth_hash', AuthHashViewSet)
router.register(r'student', UserViewSet)

urlpatterns = [
    path('verify-hash/', VerifyHashAPIView.as_view()),
    path('signup/', SignUpAPIView.as_view()),
]
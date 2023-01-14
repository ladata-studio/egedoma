from rest_framework.routers import SimpleRouter

from users.views import AuthHashViewSet, UserViewSet

router = SimpleRouter()
router.register(r'auth_hash', AuthHashViewSet)
router.register(r'student', UserViewSet)
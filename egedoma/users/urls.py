from rest_framework.routers import SimpleRouter

from users.views import AuthHashViewSet, StudentViewSet

router = SimpleRouter()
router.register(r'auth_hash', AuthHashViewSet)
router.register(r'student', StudentViewSet)
from api.views import (
    GetS3PresignedURLAPIView, TaskFormAPIView, ExamFormAPIView, 
    ExamSubjectViewSet, TaskViewSet, HomeworkListAPIView, HomeworkViewSet,
    SolutionViewSet
)
from django.urls import path
from rest_framework.routers import SimpleRouter


urlpatterns = [
    path('get_upload_link/', GetS3PresignedURLAPIView.as_view()),
    path('task_form_data/', TaskFormAPIView.as_view()),
    path('exam_form_data/<int:exam_id>/<int:subject_id>/', ExamFormAPIView.as_view()),
    path('homeworks/', HomeworkListAPIView.as_view())
]

router = SimpleRouter()
router.register(r'exam', ExamSubjectViewSet)
router.register(r'task', TaskViewSet)
router.register(r'homework', HomeworkViewSet)
router.register(r'solution', SolutionViewSet)

urlpatterns += router.urls

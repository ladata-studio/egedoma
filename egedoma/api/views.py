import os
import json
import boto3

from api.models import (
    Exam, ExamSource, ExamSubject, Source, Subject, Task, TaskExam, 
    CoursCustomer, CoursHomework, Homework, UserSolution, HomeworkTask
)
from api.serializers import (
    ExamSerializer, ExamSubjectSerializer, SourceSerializer, SubjectSerializer,
    TaskSerializer, HomeworkSerializer, CoursSerializer, UserSolutionSerializer
)

from botocore.client import Config

from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet


class GetS3PresignedURLAPIView(APIView):
  def post(self, request):
    ENDPOINT = "https://storage.yandexcloud.net"
    ACCESS_KEY = os.environ.get('YC_ACCESS_KEY')
    SECRET_KEY = os.environ.get('YC_SECRET_KEY')
    BUCKET_NAME = os.environ.get('YC_BUCKET_NAME')

    session = boto3.Session(
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY,
        region_name="ru-central1",
    )

    s3 = session.client(
        "s3", endpoint_url=ENDPOINT, config=Config(signature_version="s3v4")
    )

    filename = request.data.get('filename', None)
    presigned_url = s3.generate_presigned_post(BUCKET_NAME, filename, ExpiresIn=3600)

    return Response(presigned_url, status=200)


# TODO: разбить на три отдельных класса, чтобы можно было делать запрос 
# асинхронно
# TODO: добавить проверку токена (авторизация)
class TaskFormAPIView(APIView):
    def get(self, request):
        subjects = SubjectSerializer(Subject.objects.all(), many=True).data
        exams = ExamSerializer(Exam.objects.all(), many=True).data
        sources = SourceSerializer(Source.objects.all(), many=True).data

        data = {
            'subjects': subjects,
            'exams': exams,
            'sources': sources
        }

        return Response(data, status=200)
    

class ExamFormAPIView(APIView):
    def get(self, request, exam_id, subject_id):
        queryset = ExamSubject.objects.get(
            exam__id=exam_id, subject__id=subject_id)
        data = ExamSubjectSerializer(queryset).data
        return Response(data, status=200)
      

class ExamSubjectViewSet(ModelViewSet):
    queryset = ExamSubject.objects.all()
    serializer_class = ExamSubjectSerializer


class TaskViewSet(ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthenticated]
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def create(self, request):
        data = request.data
        data['created_by'] = request.user

        source = None
        is_new_source = data.pop('is_new_source')
        if not is_new_source:
            data['source'] = Source.objects.get(pk=data['source']['id'])
        else:
            try:
                data['source'] = Source.objects.get(
                    name=data['source']['name'],
                    link=data['source']['link']
                )
                source = data['source']
            except:
                data['source']['created_by'] = request.user
                data['source'] = Source.objects.create(**data['source'])

        kim_number = data.pop('kim_number')
        subject = data.pop('subject')
        exam = data.pop('exam')

        task = Task.objects.create(**data)

        exam_data = {
            'task': task,
            'exam': ExamSubject.objects.get(
                exam__id=exam['id'],
                subject__id=subject['id']
            ),
            'kim_number': kim_number,
        }

        if is_new_source and source is None:
            ExamSource.objects.create(exam=exam_data['exam'], source=task.source)

        exam = TaskExam.objects.create(**exam_data)

        task.exams.set = ([exam])
        task.save()
        data = TaskSerializer(task).data

        return Response(data, status=201)


class HomeworkListAPIView(APIView):
    def get(self, request):
        user = request.user
        user_courses = CoursCustomer.objects.filter(customer=user)
        courses = [item.cours for item in user_courses]

        homeworks = []
        for cours in courses:
            homeworks.append(
                [{'homework': item.homework, 'deadline': item.deadline}
                 for item in CoursHomework.objects.filter(cours=cours.cours)]
            )

        data = []

        for i in range(len(courses)):
            data.append({
                'exam': ExamSerializer(courses[i].exam.exam).data,
                'subject': SubjectSerializer(courses[i].exam.subject).data,
                'cours': CoursSerializer(courses[i].cours).data,
                'homeworks': [
                    {
                        'deadline': homework['deadline'],
                        'homework': HomeworkSerializer(homework['homework']).data, 
                    } for homework in homeworks[i]
                ]
                                                                                                                                        
            })

        return Response(data, status=201)


class HomeworkViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Homework.objects.all()
    serializer_class = HomeworkSerializer

    def retrieve(self, request, pk=None):
        user = request.user
        user_courses = CoursCustomer.objects.filter(customer=user)
        courses = [item.cours for item in user_courses]

        homework = None
        for cours in courses:
            for item in CoursHomework.objects.filter(cours=cours.cours):
                if str(item.homework.id) == str(pk):
                    homework = item
                    break

        if homework:
            data = {
                'exam': ExamSerializer(cours.exam.exam).data,
                'subject': SubjectSerializer(cours.exam.subject).data,
                'cours': CoursSerializer(cours.cours).data,
                'deadline': homework.deadline,
                'homework': HomeworkSerializer(homework.homework).data,
            }
            return Response(data, status=200)
        
        return Response({'error': 'homework is not found'}, status=500)


class SolutionViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = UserSolution.objects.all()
    serializer_class = UserSolutionSerializer

    def create(self, request):
        user = request.user
        task = request.data.get('task')
        homework = request.data.get('homework')
        user_answer = request.data.get('answer')

        try:
            homework_task = HomeworkTask.objects.get(homework=homework, task=task)
            task = homework_task.task.task
            if task.manual_check:
                params = {
                    'user': user,
                    'task': homework_task,
                    'answer': user_answer,
                    'status': 3,
                }
            else:
                params = {
                    'user': user,
                    'task': homework_task,
                    'answer': user_answer,
                }
                if user_answer == task.answer:
                    params['status'] = 1
                else: 
                    params['status'] = 2
            
            queryset = UserSolution.objects.create(**params)
            data = UserSolutionSerializer(queryset).data

            return Response(data, status=200)
            
        except:
            return Response("Homework task is not found", status=404)

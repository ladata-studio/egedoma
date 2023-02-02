from api.models import (
    Exam, ExamSubject, Source, Subject, Task, TaskExam, Homework, Cours,
    CoursExam, UserSolution
)
from rest_framework.fields import SerializerMethodField
from rest_framework import serializers


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ['id', 'name', 'name_dative']


class ExamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exam
        fields = ['id', 'name', 'grade']


class ExamSubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExamSubject
        fields = '__all__'


class SourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Source
        fields = ['id', 'name', 'link']


class TaskListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'name']


# class ExamSubjectListSerializer(serializers.ModelSerializer):
#     exam = ExamSerializer()
#     subject = SubjectSerializer()

#     class Meta:
#         model = ExamSubject
#         fields = ['exam', 'subject']


class TaskExamSerializer(serializers.ModelSerializer):
    task = TaskListSerializer()

    class Meta:
        model = TaskExam
        fields = ['id', 'kim_number', 'task']
        read_only_fields = ['task']


# class TaskSerializer(serializers.ModelSerializer):
#     created_by = UserSerializer()
#     source = SourceSerializer()
#     exams = TaskExamSerializer(many=True)

#     class Meta:
#         model = Task

#     class Meta:
#         model = Task
#         fields = [
#             'id', 'name', 'created_by', 'created_at', 'updated_at', 'task_image_url',
#             'task_files_urls', 'answer_type', 'answer', 'source', 'manual_check', 'exams'
#         ]


class SizeField(SerializerMethodField):
    def to_representation(self, value):
        answer = value.answer
        if type(answer) == list:
            if type(answer[0]) == list:
                return len(answer[0])
            return len(answer)
        return 1


class TaskSerializer(serializers.ModelSerializer):
    answer_size = SizeField()

    class Meta:
        model = Task
        fields = [
            'id', 'name', 'task_image_url', 'task_files_urls', 'answer_type',
            'answer_size', 'source', 'manual_check'
        ]


class HomeworkSerializer(serializers.ModelSerializer):
    tasks = TaskExamSerializer(many=True)

    class Meta:
        model = Homework
        fields = '__all__'


class CoursSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cours
        fields = '__all__'


class CoursExamSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoursExam
        fields = '__all__'


class UserSolutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSolution
        fields = '__all__'

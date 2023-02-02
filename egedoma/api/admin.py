from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.db import models
from django.forms import Textarea

from .models import (
    Source, Subject, Task, Exam, ExamSubject, TaskExam, ExamSource, Cours, 
    CoursExam, CoursCustomer, Homework, HomeworkTask, UserSolution, 
    CoursHomework
)


@admin.register(Task)
class TaskAdmin(ModelAdmin):
    readonly_fields = ('id', 'created_by', 'created_at', 'updated_at')
    list_display = ('id', 'created_by', 'created_at', 'updated_at')
    list_filter = ('created_by',)
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 10, 'cols': 130})},
        models.JSONField: {'widget': Textarea(attrs={'rows': 10, 'cols': 130})},
    }

    def save_model(self, request, obj, form, change):
        obj.created_by = request.user
        super().save_model(request, obj, form, change)

    class Meta:
        model = Task


@admin.register(Subject)
class SubjectAdmin(ModelAdmin):
    class Meta:
        model = Subject


@admin.register(Exam)
class ExamAdmin(ModelAdmin):
    class Meta:
        model = Exam


@admin.register(ExamSubject)
class ExamSubjectAdmin(ModelAdmin):
    class Meta:
        model = ExamSubject


@admin.register(TaskExam)
class TaskExamAdmin(ModelAdmin):
    class Meta:
        model = TaskExam


@admin.register(Source)
class SourceAdmin(ModelAdmin):
    readonly_fields = ('id', 'created_by')

    class Meta:
        model = Source


@admin.register(ExamSource)
class ExamSourceAdmin(ModelAdmin):
    class Meta:
        model = ExamSource


@admin.register(Cours)
class CoursAdmin(ModelAdmin):
    class Meta:
        model = Cours


@admin.register(CoursExam)
class CoursExamAdmin(ModelAdmin):
    class Meta:
        model = CoursExam


@admin.register(CoursCustomer)
class CoursCustomerAdmin(ModelAdmin):
    class Meta:
        model = CoursCustomer


@admin.register(Homework)
class HomeworkAdmin(ModelAdmin):
    class Meta:
        model = Homework


@admin.register(CoursHomework)
class CoursHomeworkAdmin(ModelAdmin):
    class Meta:
        model = CoursHomework


@admin.register(HomeworkTask)
class HomeworkTaskAdmin(ModelAdmin):
    class Meta:
        model = HomeworkTask


@admin.register(UserSolution)
class UserSolutionAdmin(ModelAdmin):
    class Meta:
        model = UserSolution
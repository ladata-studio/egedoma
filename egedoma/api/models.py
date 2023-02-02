from django.db import models
from users.models import User
from django.utils.translation import gettext_lazy as _


class Source(models.Model):
    name = models.CharField(max_length=125)
    link = models.CharField(null=True, blank=True, max_length=250)
    created_by = models.ForeignKey(
        User, null=True, blank=True,
        on_delete=models.SET_NULL, editable=False,
        verbose_name="источник добавил"
    )

    class Meta:
        verbose_name = 'источник заданий'
        verbose_name_plural = 'источники заданий'

    def __str__(self):
        return f'{self.name} ({self.link})'
    

class Task(models.Model):
    class AnswerType(models.IntegerChoices):
        SIMPLE = 1, _('Простой ответ')
        MULTIPLE = 2, _('Несколько ответов')
        TABLE = 3, _('Таблица ответов')
        QUILL = 4, _('Развернутый ответ')
        __empty__ = _('(Не указано)')

    name = models.CharField(max_length=128, verbose_name="название задания")
    created_by = models.ForeignKey(
        User, null=True, blank=True,
        on_delete=models.SET_NULL, editable=False,
        verbose_name="источник добавил"
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="добавлено")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="обновлено")
    task_image_url = models.CharField(
        null=True, blank=True, max_length=128, verbose_name="ссылка на условие задания")
    task_files_urls = models.JSONField(null=True, blank=True, verbose_name="ссылки на файлы для задания")
    answer_type = models.IntegerField(
        choices=AnswerType.choices, default=None, null=True, blank=True, verbose_name="тип ответа")
    answer = models.JSONField(verbose_name="ответ")
    source = models.ForeignKey(
        Source, on_delete=models.SET_NULL,
        null=True, blank=True, verbose_name="источник задания"
    )
    manual_check = models.BooleanField(
        default=False,
        verbose_name="нужна проверка преподавателя"
    )
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'задание'
        verbose_name_plural = 'задания'

    def __str__(self):
        return f'ID {self.id}'
    

class Subject(models.Model):
    name = models.CharField(max_length=50, unique=True,
                            verbose_name="название")
    name_dative = models.CharField(max_length=50,
                                   verbose_name="название в форме 'по <предмету>'")

    class Meta:
        ordering = ['name']
        verbose_name = 'предмет'
        verbose_name_plural = 'предметы'

    def __str__(self):
        return f'{self.name}'


class Exam(models.Model):
    class Grade(models.IntegerChoices):
        GRADE_1 = 1, _('1 класс')
        GRADE_2 = 2, _('2 класс')
        GRADE_3 = 3, _('3 класс')
        GRADE_4 = 4, _('4 класс')
        GRADE_5 = 5, _('5 класс')
        GRADE_6 = 6, _('6 класс')
        GRADE_7 = 7, _('7 класс')
        GRADE_8 = 8, _('8 класс')
        GRADE_9 = 9, _('9 класс')
        GRADE_10 = 10, _('10 класс')
        GRADE_11 = 11, _('11 класс')

    name = models.CharField(max_length=50, verbose_name="название")
    grade = models.IntegerField(choices=Grade.choices)
    subjects = models.ManyToManyField('Subject', through='ExamSubject')

    class Meta:
        ordering = ['-grade', 'name']
        verbose_name = 'экзамен'
        verbose_name_plural = 'экзамены'
        unique_together = ('name', 'grade')

    def __str__(self):
        return f'{self.name}, {self.get_grade_display()}'


class ExamSubject(models.Model):
    exam = models.ForeignKey(
        'Exam', on_delete=models.CASCADE,
        verbose_name="экзамен"
    )
    subject = models.ForeignKey(
        'Subject', on_delete=models.CASCADE,
        verbose_name="предмет"
    )
    tasks = models.ManyToManyField(
        'Task', through='TaskExam',
        verbose_name="задания"
    )
    kim_numbers = models.JSONField(
        verbose_name="номера заданий в КИМ", null=True, blank=True
    )
    points_conversion = models.JSONField(
        verbose_name="перевод баллов в 100-балльную систему", null=True, blank=True
    )
    task_points = models.JSONField(
        verbose_name="баллы за задания", null=True, blank=True)

    class Meta:
        verbose_name = 'экзамен по предмету'
        verbose_name_plural = 'экзамены по предметам'
        unique_together = ('exam', 'subject')

    def __str__(self):
        return f'{self.subject} — {self.exam}'


class TaskExam(models.Model):
    task = models.ForeignKey(
        'Task', on_delete=models.CASCADE, related_name='exams', verbose_name="задание")
    exam = models.ForeignKey(
        'ExamSubject', on_delete=models.CASCADE, verbose_name="экзамен")
    kim_number = models.CharField(max_length=5, verbose_name="Номер КИМ")

    class Meta:
        ordering = ['-task__created_at']
        verbose_name = 'задание по экзамену'
        verbose_name_plural = 'задания по экзаменам'
        unique_together = ('task', 'exam')

    def __str__(self):
        return f'ID {self.exam}: {self.task}'
    

class ExamSource(models.Model):
    exam = models.ForeignKey(
        ExamSubject, on_delete=models.CASCADE,
        verbose_name="экзамен"
    )
    source = models.ForeignKey(
        Source, on_delete=models.CASCADE,
        verbose_name="источник"
    )

    class Meta:
        verbose_name = 'источник для экзаменов'
        verbose_name_plural = 'источники для экзаменов'
        unique_together = ('exam', 'source')

    def __str__(self):
        return f'{self.exam} — {self.source}'


class Cours(models.Model):
    name = models.CharField(max_length=50, verbose_name="название")
    description = models.CharField(max_length=1000, verbose_name="описание")
    created_by = created_by = models.ForeignKey(
        User, null=True, blank=True,
        on_delete=models.SET_NULL, editable=False,
        verbose_name="источник добавил"
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="добавлено")
    
    class Meta:
        verbose_name = 'курс'
        verbose_name_plural = 'курсы'

    def __str__(self):
        return f'{self.name}'
    

class CoursExam(models.Model):
    cours = models.ForeignKey(
        Cours, on_delete=models.CASCADE,
        verbose_name="курс"
    )
    exam = models.ForeignKey(
        ExamSubject, on_delete=models.CASCADE,
        verbose_name="экзамен"
    )

    class Meta:
        verbose_name = 'курс по экзамену'
        verbose_name_plural = 'курсы по экзамену'
        unique_together = ('exam', 'cours')

    def __str__(self):
        return f'{self.cours} - {self.exam}'


class CoursCustomer(models.Model):
    cours = models.ForeignKey(
        CoursExam, on_delete=models.CASCADE,
        verbose_name="курс"
    )
    customer = models.ForeignKey(
        User, null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name="customer_courses",
        verbose_name="ученик"
    )
    curator = models.ForeignKey(
        User, null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name="curator_customers",
        verbose_name="куратор"
    )

    class Meta:
        verbose_name = 'ученик курса'
        verbose_name_plural = 'ученики курса'
        unique_together = ('cours', 'customer')

    def __str__(self):
        return f'{self.cours} - {self.customer}'


class Homework(models.Model):
    name = models.CharField(max_length=50, verbose_name="название")
    description = models.CharField(max_length=1000, verbose_name="описание")
    tasks = models.ManyToManyField(
        'TaskExam', through='HomeworkTask',
        verbose_name="задания"
    )
    created_by = models.ForeignKey(
        User, null=True, blank=True,
        on_delete=models.SET_NULL, editable=False,
        verbose_name="источник добавил"
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="добавлено")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="обновлено")

    
    class Meta:
        verbose_name = 'домашнее задание'
        verbose_name_plural = 'домашние задания'

    def __str__(self):
        return f'{self.name}'
    

class CoursHomework(models.Model):
    cours = models.ForeignKey(
        Cours, on_delete=models.CASCADE,
        verbose_name="курс"
    )
    homework = models.ForeignKey(
        Homework, on_delete=models.CASCADE,
        verbose_name="домашнее задание"
    )
    deadline = models.DateTimeField(
        verbose_name="дедлайн", null=True, blank=True)

    class Meta:
        verbose_name = 'ДЗ курса'
        verbose_name_plural = 'ДЗ курса'

    def __str__(self):
        return f'{self.cours} - {self.homework}'


class HomeworkTask(models.Model):
    task = models.ForeignKey(
        TaskExam, on_delete=models.CASCADE,
        verbose_name="задание"
    )
    homework = models.ForeignKey(
        Homework, on_delete=models.CASCADE,
        verbose_name="домашнее задание"
    )
    created_by = models.ForeignKey(
        User, null=True, blank=True,
        on_delete=models.SET_NULL, editable=False,
        verbose_name="источник добавил"
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="добавлено")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="обновлено")


    class Meta:
        verbose_name = 'задание в ДЗ'
        verbose_name_plural = 'задания в ДЗ'
        unique_together = ('task', 'homework')

    def __str__(self):
        return f'{self.task.id} -> {self.homework}'


class UserSolution(models.Model):
    class Status(models.IntegerChoices):
        STATUS_1 = 1, _('правильно')
        STATUS_2 = 2, _('неверно')
        STATUS_3 = 3, _('ожидает проверки')

    user = models.ForeignKey(
        User, null=True, blank=True,
        on_delete=models.SET_NULL, editable=False,
        verbose_name="ученик"
    )
    task = models.ForeignKey(
        HomeworkTask, on_delete=models.CASCADE,
        verbose_name="задание"
    )
    answer = models.JSONField(verbose_name="ответ")
    status = models.IntegerField(choices=Status.choices)
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="добавлено")

    class Meta:
        verbose_name = 'решение ученика'
        verbose_name_plural = 'решения учеников'

    def __str__(self):
        return f'{self.task} - {self.user}'

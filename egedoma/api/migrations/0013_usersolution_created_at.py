# Generated by Django 4.1.5 on 2023-01-28 02:59

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0012_homework_tasks'),
    ]

    operations = [
        migrations.AddField(
            model_name='usersolution',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='добавлено'),
            preserve_default=False,
        ),
    ]
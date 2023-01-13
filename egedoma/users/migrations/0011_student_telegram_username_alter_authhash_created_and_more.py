# Generated by Django 4.1.5 on 2023-01-13 00:22

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_rename_firstname_student_first_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='telegram_username',
            field=models.CharField(blank=True, max_length=32, null=True),
        ),
        migrations.AlterField(
            model_name='authhash',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2023, 1, 13, 0, 22, 11, 294040, tzinfo=datetime.timezone.utc), editable=False),
        ),
        migrations.AlterField(
            model_name='student',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2023, 1, 13, 0, 22, 11, 294675, tzinfo=datetime.timezone.utc), editable=False),
        ),
    ]
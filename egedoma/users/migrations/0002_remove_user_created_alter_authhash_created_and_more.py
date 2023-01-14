# Generated by Django 4.1.5 on 2023-01-13 22:56

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='created',
        ),
        migrations.AlterField(
            model_name='authhash',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2023, 1, 13, 22, 56, 17, 353950, tzinfo=datetime.timezone.utc), editable=False),
        ),
        migrations.AlterField(
            model_name='user',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2023, 1, 13, 22, 56, 17, 352339, tzinfo=datetime.timezone.utc), editable=False),
        ),
    ]
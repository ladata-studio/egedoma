# Generated by Django 4.1.5 on 2023-01-13 23:40

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_authhash_created_alter_user_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='authhash',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2023, 1, 13, 23, 40, 36, 259593, tzinfo=datetime.timezone.utc), editable=False),
        ),
        migrations.AlterField(
            model_name='user',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2023, 1, 13, 23, 40, 36, 257740, tzinfo=datetime.timezone.utc), editable=False),
        ),
    ]
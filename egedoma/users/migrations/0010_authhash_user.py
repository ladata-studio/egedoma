# Generated by Django 4.1.5 on 2023-01-14 08:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_alter_authhash_created_at_alter_user_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='authhash',
            name='user',
            field=models.ForeignKey(default=10, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]

# Generated by Django 4.1.5 on 2023-01-13 22:35

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='AuthHash',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hash', models.CharField(max_length=64)),
                ('created', models.DateTimeField(default=datetime.datetime(2023, 1, 13, 22, 35, 22, 605474, tzinfo=datetime.timezone.utc), editable=False)),
                ('is_expired', models.BooleanField(default=False, editable=False)),
            ],
            options={
                'verbose_name_plural': 'auth hashes',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('telegram_id', models.IntegerField(db_index=True, unique=True)),
                ('created', models.DateTimeField(default=datetime.datetime(2023, 1, 13, 22, 35, 22, 603489, tzinfo=datetime.timezone.utc), editable=False)),
                ('is_active', models.BooleanField(default=False, editable=False)),
                ('first_name', models.CharField(blank=True, max_length=64, null=True)),
                ('last_name', models.CharField(blank=True, max_length=64, null=True)),
                ('telegram_username', models.CharField(blank=True, max_length=32, null=True)),
                ('photo', models.CharField(blank=True, max_length=128, null=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(default=datetime.datetime(2023, 1, 13, 22, 35, 22, 603593, tzinfo=datetime.timezone.utc), editable=False)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]

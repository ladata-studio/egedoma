# Generated by Django 4.1.5 on 2023-01-27 08:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_remove_homework_cours_courshomework'),
    ]

    operations = [
        migrations.AddField(
            model_name='homework',
            name='cours',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='api.cours', verbose_name='ะบััั'),
            preserve_default=False,
        ),
    ]

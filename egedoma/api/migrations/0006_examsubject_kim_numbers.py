# Generated by Django 4.1.5 on 2023-01-26 22:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_alter_taskexam_options_alter_courscustomer_curator_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='examsubject',
            name='kim_numbers',
            field=models.JSONField(blank=True, null=True, verbose_name='номера заданий в КИМ'),
        ),
    ]

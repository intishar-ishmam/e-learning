# Generated by Django 2.2.1 on 2021-11-05 08:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teacher', '0002_teacher_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='teacher',
            name='password',
            field=models.CharField(default=None, max_length=255),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='full_name',
            field=models.CharField(default=None, max_length=255, verbose_name='Teacher name (Sir/Mam)'),
        ),
    ]

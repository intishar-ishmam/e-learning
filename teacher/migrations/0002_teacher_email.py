# Generated by Django 2.2.1 on 2021-11-05 08:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teacher', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='teacher',
            name='email',
            field=models.CharField(default=None, max_length=255),
        ),
    ]
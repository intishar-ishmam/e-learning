from django.db import models

# Create your models here.

from django.db import models
from web.models import Courses, Department

# Create your models here.


class Teacher(models.Model):
    id = models.AutoField(primary_key=True)
    full_name = models.CharField(max_length=255, null=False, blank=False, default=None, verbose_name='Teacher name (Sir/Mam)')
    email = models.CharField(max_length=255, null=False, blank=False, default=None)
    password = models.CharField(max_length=255, null=False, blank=False, default=None)
    department = models.ForeignKey(Department, null=False, blank=False, default=None, on_delete=models.CASCADE)
    course = models.ManyToManyField(Courses, null=False, blank=True, default=None)

    class Meta:
        db_table = 'teacher'


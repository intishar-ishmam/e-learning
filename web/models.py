from django.db import models
from froala_editor.fields import FroalaField

# Create your models here.

exam_type = [
    ('mid-term', 'Mid-Term'),
    ('final', 'Final'),
]


class Department(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(default=None)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'department'


class Courses(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    course_title = models.CharField(max_length=255)
    course_code = models.CharField(max_length=50)
    image = models.ImageField(default=None)

    def __str__(self):
        return self.course_title
    
    class Meta:
        db_table = 'courses'


class Smartbook(models.Model):
    title = models.CharField(max_length=255)
    course = models.ForeignKey(Courses, on_delete=models.CASCADE)
    chapter = models.IntegerField()
    content = FroalaField()

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'smartbooks'


class Video(models.Model):
    title = models.CharField(max_length=255)
    course = models.ForeignKey(Courses, on_delete=models.CASCADE)
    chapter = models.IntegerField()
    urls = models.CharField(max_length=255)

    def __str__(self):
        return self.title
    
    class Meta:
        db_table = 'videos'


class Quiz(models.Model):
    course = models.ForeignKey(Courses, on_delete=models.CASCADE)
    exam_type = models.CharField(max_length=50, choices=exam_type)
    question = models.CharField(max_length=255)
    choice_1 = models.CharField(max_length=255)
    choice_2 = models.CharField(max_length=255)
    choice_3 = models.CharField(max_length=255)
    choice_4 = models.CharField(max_length=255)
    answer_no = models.IntegerField()

    def __str__(self):
        return self.question

    class Meta:
        db_table = 'quiz'


class Students(models.Model):
    student = models.CharField(primary_key=True, max_length=50)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.CharField(max_length=255, default=None)
    mobile = models.CharField(max_length=100, null=True, default=None)
    password = models.CharField(max_length=255, default=None)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    intake = models.IntegerField()
    section = models.IntegerField()

    def __str__(self):
        return self.student
    
    class Meta:
        db_table = 'students'


class Enroll(models.Model):
    student = models.ForeignKey(Students, on_delete=models.CASCADE, default=None)
    course = models.ForeignKey(Courses, on_delete=models.CASCADE, default=None)
    status = models.CharField(max_length=100, default='pending')
    enroll_type = models.CharField(max_length=100, default='Regular')
    mid_term_marks = models.IntegerField(null=True)
    final_marks = models.IntegerField(null=True)
    total_marks = models.IntegerField(default=0)
    created_at = models.DateField()
    
    def __str__(self):
        return self.student_id
    
    class Meta:
        db_table = 'enroll'

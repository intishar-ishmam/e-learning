from django.contrib import admin
from .models import Department, Courses, Smartbook, Video, Quiz, Students, Enroll

# Register your models here.

class QuizAdmin(admin.ModelAdmin):
    list_display = ('question', 'course', 'exam_type')
    search_fields = ['course__course_title', 'exam_type']



admin.site.register(Department)
admin.site.register(Courses)
admin.site.register(Smartbook)
admin.site.register(Video)
admin.site.register(Quiz, QuizAdmin)
admin.site.register(Students)
admin.site.register(Enroll)
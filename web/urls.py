from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('course/<department_id>', views.course, name='course'),
    path('register', views.register, name='register'),
    path('enroll/<course_id>', views.enroll, name='enroll'),
    path('addcourse/<course_id>', views.addcourse, name='addcourse'),
    path('mycourse', views.mycourse, name='mycourse'),
    path('classroom/<course_id>/<topics_id>', views.classroom, name='classroom'),
    path('smartbook/<course_id>/<topics_id>', views.smartbook, name='smartbook'),
    path('video/<course_id>/<topics_id>', views.video, name='video'),
    path('quiz/<course_id>/<exam_type>', views.quiz, name='quiz'),
    path('examprocess/<course_id>/<exam_type>', views.examprocess, name='examprocess'),
    path('profile', views.profile, name='profile'),
    path('result/<course_id>/<exam_type>/<marks>', views.result, name='result'),
]
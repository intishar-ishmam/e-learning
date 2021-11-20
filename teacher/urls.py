from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login, name='teacher-login'),
    path('teacher-index/', views.teacher_index, name='teacher-index'),
    path('select-module/<int:course_id>', views.select_module, name='select-module'),
    path('video-display/<int:course_id>', views.video_display, name='video-display'),
    path('video-edit/<int:video_id>/<int:course_id>', views.video_edit, name='video-edit'),
    path('video-add/<int:course_id>', views.video_add, name='video-add'),
    path('video-delete/<int:video_id>/<int:course_id>', views.video_delete, name='video-delete'),
    path('smartbook-display/<int:course_id>', views.smartbook_display, name='smartbook-display'),
    path('smartbook-edit/<int:smartbook_id>/<int:course_id>', views.smartbook_edit, name='smartbook-edit'),
    path('smartbook-add/<int:course_id>', views.smartbook_add, name='smartbook-add'),
    path('smartbook-delete/<int:smartbook_id>/<int:course_id>', views.smartbook_delete, name='smartbook-delete'),
    path('quiz-display/<int:course_id>', views.quiz_display, name='quiz-display'),
    path('quiz-edit/<int:quiz_id>/<int:course_id>', views.quiz_edit, name='quiz-edit'),
    path('quiz-add/<int:course_id>', views.quiz_add, name='quiz-add'),
    path('quiz-delete/<int:quiz_id>/<int:course_id>', views.quiz_delete, name='quiz-delete'),

]

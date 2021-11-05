from django.shortcuts import render, redirect, HttpResponse
from .models import Teacher
from web.models import Courses, Smartbook, Video, Quiz
from django.contrib import messages
from .forms import VideoForm, SmartbookForm, QuizForm, SmartbookContentForm

# Create your views here.


# session handeling
def logged_in(request):
    try:
        return request.session['teacher_id']
    except KeyError:
        return False


def login(request):
    if logged_in(request):
        return redirect('teacher-index')

    if request.method == 'GET':
        return render(request, 'teacher/login.html')

    elif request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        try:
            T = Teacher.objects.get(email=email)
            if T.password == password:
                request.session['teacher_id'] = T.id
                messages.success(request, 'Successfully logged in!')
                return redirect('teacher-index')
            else:
                messages.error(request, 'Password does not matched!')
                return redirect('teacher-login')
        except:
            messages.error(request, 'Teacher does not exists!')
            return redirect('teacher-login')
    else:
        return None


def teacher_index(request):
    if not logged_in(request):
        return redirect('teacher-login')
    else:
        t = Teacher.objects.get(pk=request.session['teacher_id'])

    C = Courses.objects.filter(teacher__id=request.session['teacher_id'])
    return render(request, 'teacher/teacher-index.html', {"courses": C})


def select_module(request, course_id):
    if not logged_in(request):
        return redirect('teacher-login')

    return render(request, 'teacher/select-module.html', {"course_id": course_id})


def video_display(request, course_id):
    if not logged_in(request):
        return redirect('teacher-login')

    video = Video.objects.filter(course_id=course_id)
    return render(request, 'teacher/video-display.html', {"videos": video, "course_id": course_id})


def video_edit(request, video_id, course_id):
    if not logged_in(request):
        return redirect('teacher-login')

    videos = Video.objects.get(pk=video_id)
    if request.method == 'GET':
        return render(request, 'teacher/video-edit.html', {"videos": videos, "course_id": course_id})

    if request.method == 'POST':
        form = VideoForm(request.POST, instance=videos)
        if form.is_valid():
            form.save()
        else:
            print(form.errors)
        messages.success(request, "Video Updated")
        return redirect('video-display', course_id=course_id)


def video_add(request, course_id):
    if not logged_in(request):
        return redirect('teacher-login')

    if request.method == 'GET':
        return render(request, 'teacher/video-add.html', {"course_id": course_id})

    if request.method == 'POST':
        form = VideoForm(request.POST)
        if form.is_valid():
            form.save()
        else:
            print(form.errors)
        messages.success(request, "Video Added")
        return redirect('video-display', course_id=course_id)


def video_delete(request, video_id, course_id):
    if not logged_in(request):
        return redirect('teacher-login')

    try:
        Video.objects.get(pk=video_id).delete()
        messages.success(request, "Video deleted")
        return redirect('video-display', course_id=course_id)
    except:
        messages.error(request, "video not found")
        return redirect('video-display', course_id=course_id)


def smartbook_display(request, course_id):
    if not logged_in(request):
        return redirect('teacher-login')

    smartbook = Smartbook.objects.filter(course_id=course_id)
    return render(request, 'teacher/smartbook-display.html', {"smartbook": smartbook, "course_id": course_id})


def smartbook_edit(request, smartbook_id, course_id):
    if not logged_in(request):
        return redirect('teacher-login')

    smartbook = Smartbook.objects.get(pk=smartbook_id)
    if request.method == 'GET':
        form = SmartbookContentForm(instance=smartbook)
        return render(request, 'teacher/smartbook-edit.html', {"smartbook": smartbook, "course_id": course_id, "form": form})

    if request.method == 'POST':
        form = SmartbookForm(request.POST, instance=smartbook)
        if form.is_valid():
            form.save()
        else:
            print(form.errors)
        messages.success(request, "Smartbook Updated")
        return redirect('smartbook-display', course_id=course_id)


def smartbook_add(request, course_id):
    if not logged_in(request):
        return redirect('teacher-login')

    if request.method == 'GET':
        form = SmartbookContentForm()
        return render(request, 'teacher/smartbook-add.html', {"course_id": course_id, "form": form})

    if request.method == 'POST':
        form = SmartbookForm(request.POST)
        if form.is_valid():
            form.save()
        else:
            print(form.errors)
        messages.success(request, "Smartbook Added")
        return redirect('smartbook-display', course_id=course_id)


def smartbook_delete(request, smartbook_id, course_id):
    if not logged_in(request):
        return redirect('teacher-login')

    try:
        Smartbook.objects.get(pk=smartbook_id).delete()
        messages.success(request, "Smartbook deleted")
        return redirect('smartbook-display', course_id=course_id)
    except:
        messages.error(request, "Smartbook not found")
        return redirect('smartbook-display', course_id=course_id)

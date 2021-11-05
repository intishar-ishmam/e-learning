from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from datetime import datetime
from django.db.models import F
from .models import Smartbook, Students, Department, Courses, Enroll, Video, Smartbook, Quiz
import requests

# Create your views here.


# session handeling
def logged_in(request):
    try:
        return request.session['student_id']
    except KeyError:
        return False


def check_required(request, fields):
    warning = False
    for field in fields:
        if not request.POST[field] or request.POST[field].isspace():
            warning = True
    return warning


#Set field to value or None for Null in db
def set_validate(request, field, sanitize):
    strings = ["\'", "\"", ";", ">", "<", "/", "(", ")", "{", "}"]
    try:
        if not request.POST[field] or request.POST[field].isspace():
            return None
    except:
        return None
    else:
        data = request.POST[field]
        if sanitize:
            for x in strings:
                data.replace(x, '')
        return data


def login(request):
    if logged_in(request):
        return redirect('index')
    
    if request.method == 'GET':
        return render(request, 'useraccount/login.html')
    
    elif request.method == 'POST':
        student_id = set_validate(request, 'student_id', sanitize=False)
        password = set_validate(request, 'password', sanitize=False)
        try:
            S = Students.objects.get(student=student_id)
            if S.password == password:
                request.session['student_id'] = student_id
                messages.success(request, 'Successfully logged in!')
                return redirect('index')
            else:
                messages.error(request, 'Password does not matched!')
                return redirect('login')
        except:
            messages.error(request, 'Student does not exists!')
            return redirect('login')
    else:
        return None


def logout(request):
    try:
        del request.session['student_id']
        request.session.flush()
    except:
        pass

    try:
        del request.session['teacher_id']
        request.session.flush()
    except:
        pass

    return redirect('index')


def register(request):
    if logged_in(request):
        return redirect('index')

    if request.method == 'GET':
        department = Department.objects.all()
        return render(request, 'useraccount/register.html', {"department": department})

    elif request.method == 'POST':
        if request.POST['password1'] != request.POST['password2']:
            messages.error(request, "Two Password does not matched!")
            return redirect('register')

        if Students.objects.filter(student=request.POST['student_id']):
            messages.error(request, "A student already registerd with this ID!")
            return redirect('register')

        #Inserting user in db
        dept = set_validate(request, 'department', sanitize=False)
        S = Students (
            student = set_validate(request, 'student_id', sanitize=True),
            first_name = set_validate(request, 'first_name', sanitize=True),
            last_name = set_validate(request, 'last_name', sanitize=True),
            email = set_validate(request, 'email', sanitize=True),
            mobile = set_validate(request, 'mobile', sanitize=True),
            password = set_validate(request, 'password1', sanitize=False),
            department = Department.objects.get(id=dept),
            intake = set_validate(request, 'intake', sanitize=True),
            section = set_validate(request, 'section', sanitize=True),
            )

        S.save() # Inserting user in database
        request.session['student_id'] = request.POST['student_id']
        messages.success(request, "Successfully registered! Good Luck :)")
        return redirect('index')

    else:
        return None

# ------------------------------------------------


def index(request):
    departments = Department.objects.all()
    return render(request, 'web/index.html', {"departments": departments})


def course(request, department_id):
    courses = Courses.objects.filter(department_id=department_id)
    return render(request, 'web/courselist.html', {"courses": courses} )


def enroll(request, course_id):
    course = Courses.objects.get(id=course_id)
    smartbook = Smartbook.objects.filter(course=course_id).count()
    video = Video.objects.filter(course=course_id).count()
    return render(request, 'web/enroll.html', {"course": course, "smartbook": smartbook, "video": video})


def addcourse(request, course_id):
    if not logged_in(request):
        messages.error(request, 'Please Login to continue.')
        return redirect('login')
    else:
        student_id = request.session['student_id']
    
    try:
        exists = Enroll.objects.get(student_id=student_id, course_id=course_id, final_marks=None)
        messages.error(request, 'You already took this course!')
        return redirect('enroll', course_id=course_id)
    except Exception as e:
        try:
            exists = Enroll.objects.filter(student_id=student_id, course_id=course_id, status='done')
            if exists:
                for item in exists:
                    if item.total_marks >= 40:
                        enroll_type = 'Improve'
                        break
                else:
                    enroll_type = 'Retake'
            else:
                enroll_type = 'Regular'
        except Exception as e:
            enroll_type = 'Regular'

        created_at = datetime.now().date()
        Enroll.objects.create(created_at=created_at,student_id=student_id,course_id=course_id, enroll_type=enroll_type)
        messages.success(request, 'Course enrolled!')
        return redirect('enroll', course_id=course_id)


def mycourse(request):
    if not logged_in(request):
        return redirect('login')
    else:
        student_id = request.session['student_id']
    
    courses = Enroll.objects.select_related('course', 'student').filter(student_id=student_id).order_by('-id')
    return render(request, 'useraccount/mycourse.html', {"courses": courses})


def classroom(request, course_id):
    return render(request, 'useraccount/classroom.html')


def smartbook(request, course_id, topics_id):
    if not logged_in(request):
        return redirect('login')

    smartbook = Smartbook.objects.filter(course=course_id).values('title', 'id')
    smartcontent = Smartbook.objects.filter(course=course_id, id=topics_id).values('title', 'content')
    return render(request, 'useraccount/smartbook.html', {"smartbook": smartbook, "course_id": course_id, "smartcontent": smartcontent})


def video(request, course_id, topics_id):
    if not logged_in(request):
        return redirect('login')
        
    video = Video.objects.filter(course=course_id).values('title', 'id')
    videocontent = Video.objects.filter(course=course_id, id=topics_id).values('title', 'urls')
    return render(request, 'useraccount/video.html', {"video": video, "course_id": course_id, "videocontent": videocontent})


def quiz(request, course_id, exam_type):
    if not logged_in(request):
        return redirect('login')

    quiz = Quiz.objects.filter(course=course_id, exam_type=exam_type)
    if exam_type == 'mid-term':
        quiz = quiz.order_by('?')[:40]
    else:
        quiz = quiz.order_by('?')[:60]
    return render(request, 'useraccount/quiz.html', {"quiz": quiz, "course_id": course_id, "exam_type": exam_type})


def examprocess(request, course_id, exam_type):
    if not logged_in(request):
        return redirect('login')
    else:
        student_id = request.session['student_id']

    enroll = Enroll.objects.filter(student=student_id, course=course_id).order_by('-id')[:1]
    if exam_type == 'mid-term':
        for item in enroll:
            if item.mid_term_marks != None:
                messages.error(request, "You have already done this examination.")
                return redirect('quiz',course_id=course_id,exam_type=exam_type)
    if exam_type == 'final':
        for item in enroll:
            if item.mid_term_marks == None:
                messages.error(request, "You have to give mid-term examination first.")
                return redirect('quiz',course_id=course_id,exam_type=exam_type)
    
    answers = Quiz.objects.filter(course_id=course_id, exam_type=exam_type).values('id', 'answer_no')
    marks = 0
    for key, value in request.POST.items():
        if key != 'csrfmiddlewaretoken':
            for item in answers:
                if int(key) == int(item['id']) and int(value) == int(item['answer_no']):
                    marks = marks + 1
    
    if exam_type == 'mid-term':
        Enroll.objects.filter(student=student_id,course=course_id,status='pending').update(mid_term_marks=marks,total_marks=marks)
    else:
        E = Enroll.objects.filter(student=student_id,course=course_id,status='pending').update(
            final_marks = marks,
            total_marks = F('total_marks') + marks,
            status = 'done')

    request.session['show_result'] = '1'
    return redirect('result', course_id=course_id, exam_type=exam_type, marks=marks)


def result(request, course_id, exam_type, marks):
    if not logged_in(request):
        return redirect('login')
    else:
        student_id = request.session['student_id']
    
    try:
        request.session['show_result']
    except:
        return redirect('index')
    
    del request.session['show_result']

    course_id = course_id
    exam_type = exam_type
    result = Quiz.objects.filter(course_id=course_id,exam_type=exam_type)

    std = Students.objects.get(student=student_id)
    crs = Courses.objects.get(id=course_id)

    messages.success(request, f"Quiz Received! Your marks is {marks}")

    return render(request, 'useraccount/result.html', {"result":result, "course_id": course_id, "exam_type": exam_type})


def profile(request):
    if not logged_in(request):
        return redirect('login')
    else:
        student_id = request.session['student_id']
    
    if request.method == 'GET':
        profile = Students.objects.get(student=student_id)
        return render(request, 'useraccount/std_profile.html', {"profile": profile})
    
    elif request.method == 'POST':
        first_name = set_validate(request, 'first_name', sanitize=True)
        last_name = set_validate(request, 'last_name', sanitize=True)
        email = set_validate(request, 'email', sanitize=True)
        mobile = set_validate(request, 'mobile', sanitize=True)

        Students.objects.filter(student=student_id).update(
            first_name = first_name,
            last_name = last_name,
            email = email,
            mobile = mobile,
            )
        messages.success(request, "Profile updated!")
        
        if not check_required(request, ['password1', 'password2']):
            password1 = request.POST['password1']
            password2 = request.POST['password2']

            if password1 != "" and password2 != "":
                if password1 != password2:
                    messages.error(request, "Two password does not matched. Password was not changed!")
                else:
                    Students.objects.filter(student=student_id).update(
                        password = password1
                    )
                    messages.success(request, "Password changed!")

        return redirect('profile')
    else:
        return None

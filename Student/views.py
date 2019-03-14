from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import logout, authenticate, login
from .forms import SignUpForm, ProfileForm, AssignmentForm, ExamForm, CourseForm, ProgramForm
from .models import Student, Assignment, Course, Exam, Program
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from datetime import datetime
# from django.http import HttpResponse
# Create your views here.


def index(request):
    if request.user.is_authenticated:
        return render(request, 'Student/dashboard.html')
    else:
        return redirect('accounts/login')


def register(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect("/")

        else:
            for msg in form.error_messages:
                print(form.error_messages[msg])

            return render(request, "registration/register.html", context={"form": form})

    form = SignUpForm()
    return render(request, "registration/register.html", {"form": form})


@login_required()
def profile(request):
    pk = request.user.id
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            post.picture = form.cleaned_data['picture']
            cat = Course.objects.get(pk=request.POST['course'])
            post.course.add(cat)
            messages.success(request, 'Successfully created new Profile')
            return redirect('profile')
    else:
        form = ProfileForm()
    args = {'profile': Student.objects.filter(user_id=pk).first(), 'form': form}
    return render(request, 'Student/profile.html', args)


@login_required()
def profile_edit(request):
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=request.user.student)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            post.picture = form.cleaned_data['picture']
            cat = Course.objects.get(pk=request.POST['course'])
            post.course.add(cat)
            messages.success(request, 'Successfully edited')
            return redirect('profile')
    else:
        form = ProfileForm(instance=request.user)
    args = {'form': form}
    return render(request, 'Student/edit_profile.html', args)


@login_required()
def assignment(request):
    assign = Assignment.objects.all()
    for assi in assign:
        if assi.due_date < datetime.now().date():
            assi.delete()
    pk = request.user.id
    args = {'profile': get_object_or_404(Student, user_id=pk), 'assign': assign}
    return render(request, 'Student/assignment.html', args)


@staff_member_required
def post_assignment(request):
    if request.method == "POST":
        form = AssignmentForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.file = form.cleaned_data['file']
            post.save()
            messages.success(request, 'Successfully added')
            return redirect('index')
    else:
        form = AssignmentForm()
    return render(request, 'Student/newassignment.html', {'form': form})


# @staff_member_required
# def attendance(request):
#     students = Student.objects.all()
#     courses = Course.objects.all()
#     if request.method == "POST":
#         form = request.POST
#         form.save()
#         return redirect('index')
#     return render(request, 'Student/attendance.html', {'students': students, 'courses': courses})


# @login_required()
# def attendance_view(request):
#     attend = Attendance.objects.all()
#     pk = request.user.id
#     args = {'profile': get_object_or_404(Student, user_id=pk), 'attend': attend}
#     return render(request, 'Student/attendance_view.html', args)


@staff_member_required()
def exam_new(request):
    if request.method == "POST":
        form = ExamForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            messages.success(request, 'Successfully added new Exam')
            return redirect('index')
    else:
        form = ExamForm()
    return render(request, 'Student/exam_new.html', {'form': form})


@login_required()
def exam(request):
    assign = Exam.objects.all()
    for assi in assign:
        if assi.date < datetime.now().date():
            assi.delete()
    pk = request.user.id
    args = {'profile': get_object_or_404(Student, user_id=pk), 'assign': assign}
    return render(request, 'Student/exam.html', args)


@staff_member_required()
def course_new(request):
    if request.method == "POST":
        form = CourseForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            messages.success(request, 'Successfully added new Course')
            return redirect('index')
    else:
        form = CourseForm()
    return render(request, 'Student/add_course.html', {'form': form})


@login_required()
def course(request):
    cou = Course.objects.all()
    args = {'course': cou}
    return render(request, 'Student/course.html', args)


@staff_member_required()
def program_new(request):
    if request.method == "POST":
        form = ProgramForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            messages.success(request, 'Successfully added new Exam')
            return redirect('index')
    else:
        form = ProgramForm()
    return render(request, 'Student/add_program.html', {'form': form})


@login_required()
def program(request):
    pro = Program.objects.all()
    args = {'course': pro}
    return render(request, 'Student/program.html', args)

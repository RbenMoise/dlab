from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, render, HttpResponse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.generic import CreateView, ListView, UpdateView
from .models import Course, LabReport, Laboratory, LabTemplate, Grade, User
# Assume these forms are defined in forms.py
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect

from .forms import GradeForm, LaboratoryForm, UserRegistrationForm, CourseForm, LabReportForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Course


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
        username = form.cleaned_data.get('username')
        messages.success(request, f'Account created for {username}')
        # Make sure you have a URL named 'login'
        return redirect('login')

    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})


class CourseCreateView(CreateView):
    model = Course
    form_class = CourseForm
    template_name = 'course/add_course.html'
    success_url = '/courses/'


class LabReportSubmitView(CreateView):
    model = LabReport
    form_class = LabReportForm
    template_name = 'lab_report/submit.html'

    def form_valid(self, form):
        form.instance.student = self.request.user
        return super().form_valid(form)


class GradeReportView(UpdateView):
    model = Grade
    form_class = GradeForm
    template_name = 'grading/grade_report.html'


def user_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            # Return an 'invalid login' error message.
            context = {'error': 'Invalid username or password'}
            return render(request, 'users/login.html', context)
    else:
        return render(request, 'users/login.html')

# logout view


def user_logout(request):
    logout(request)
    return redirect('login')

# views for landing page


# dashboard


@login_required
def dashboard(request):
    if request.user.role == User.Role.STUDENT:
        # Fetch data relevant to students
        courses = Course.objects.filter(
            student=request.user)  # Example query
        lab_reports = LabReport.objects.filter(
            student=request.user)  # Example query
        grades = Grade.objects.filter(
            lab_report__student=request.user)  # Example query
        enrolled_courses = request.user.enrolled_courses.all()
        # Assuming Course is your model name
        available_courses = Course.objects.exclude(
            id__in=enrolled_courses.values_list('id', flat=True))

        # Assuming you're fetching lab_reports and grades somehow
        lab_reports = LabReport.objects.filter(student=request.user)
        grades = Grade.objects.filter(lab_report__student=request.user)
        context = {
            'enrolled_courses': enrolled_courses,
            'available_courses': available_courses,
            'lab_reports': lab_reports,
            'grades': grades,
            'courses': courses
        }
        return render(request, 'users/student_dashboard.html', context)
    elif request.user.role == User.Role.LECTURER:
        # Fetch data relevant to lecturers
        courses_taught = Course.objects.filter(
            lecturer=request.user)  # Example query
        pending_reports = LabReport.objects.filter(
            laboratory__course__lecturer=request.user, status='Pending')  # Example query

        context = {
            'courses': courses_taught,
            'pending_reports': pending_reports,
        }
        return render(request, 'users/lecturer_dashboard.html', context)
    elif request.user.role == User.Role.LAB_TECH:
        # Fetch data relevant to lab technicians
        lab_reports_to_process = LabReport.objects.filter(
            status='Processing')  # Example query
        courses = Course.objects.all()
        course_id = Course.objects.first().id
        context = {
            'course_id': course_id,
            'courses': courses,
            'lab_reports_to_process': lab_reports_to_process,
        }
        return render(request, 'users/labtech_dashboard.html', context)
    else:
        # Default to a generic response or dashboard if the role is unknown
        return HttpResponse("Your role is not defined for a specific dashboard.")


def landing_page(request):
    return render(request, 'yourapp/landing_page.html')

# lecview for


@login_required
def grade_report(request, report_id):
    if not request.user.is_lecturer:
        return HttpResponseForbidden('not a lexc')
    # Logic for grading a report


class CourseCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Course
    form_class = CourseForm
    template_name = 'course/add_course.html'
    success_url = '/users/dashboard/'

    def form_valid(self, form):
        form.instance.lecturer = self.request.user
        return super().form_valid(form)

    def test_func(self):
        return self.request.user.role == User.Role.LECTURER


@login_required
def delete_course(request, course_id):
    # Ensure only lecturers can delete courses
    if request.user.role != User.Role.LECTURER:
        return HttpResponseForbidden("You are not authorized to delete courses.")

    course = get_object_or_404(Course, id=course_id, lecturer=request.user)
    course.delete()
    # Redirect to the dashboard after deletion
    return redirect('lecturer_dashboard')


@login_required
def enroll_course(request):
    if request.method == 'POST':
        course_id = request.POST.get('course_id')
        course = Course.objects.get(id=course_id)
        course.student.add(request.user)
        course.save()
        messages.success(request, "Enrolled successfully!")
        return redirect('student_dashboard')
    else:
        all_courses = Course.objects.all()
        return render(request, 'enroll_course.html', {'courses': all_courses})


def unenroll_course(request):
    if request.method == 'POST':
        course_id = request.POST.get('course_id')
        course = get_object_or_404(Course, id=course_id)
        request.user.enrolled_courses.remove(course)
        # Assuming 'enrolled_courses' is the ManyToManyField linking users to courses
        # Redirect to the dashboard or an appropriate view
        return redirect('student_dashboard')
    else:
        # Handle non-POST request; redirect as needed
        return redirect('student_dashboard')


@login_required
def upload_lab_report(request, course_id):
    course = Course.objects.get(id=course_id)
    if request.method == 'POST':
        form = LabReportForm(request.POST, request.FILES, course_id=course_id)
        if form.is_valid():
            lab_report = form.save(commit=False)
            lab_report.course = course
            lab_report.creator = request.user
            lab_report.save()
            return redirect('labtech_dashboard')
    else:
        form = LabReportForm(course_id=course_id)
    return render(request, 'course/upload_lab_report.html', {'form': form, 'course': course})


def add_laboratory(request):
    if request.method == 'POST':
        form = LaboratoryForm(request.POST)
        if form.is_valid():
            form.save()
            # Redirect to labtech dashboard or a page confirming successful creation
            return redirect('labtech_dashboard')
    else:
        form = LaboratoryForm()
    return render(request, 'users/add_laboratory.html', {'form': form})


@login_required
def my_creations(request):
    if not request.user.is_authenticated:
        # Redirect the user or show an error message
        return render(request, 'error_page.html', {'error': 'You need to be logged in to view this page.'})

    if request.user.role == 'LT':
        # Fetch lab reports and laboratories created by the logged-in lab technician
        my_lab_reports = LabReport.objects.filter(creator=request.user)
        my_laboratories = Laboratory.objects.filter(creator=request.user)

        context = {
            'my_lab_reports': my_lab_reports,
            'my_laboratories': my_laboratories,
        }
        return render(request, 'my_creations.html', context)
    else:
        # Redirect or show an error message if the user is not a lab technician
        return render(request, 'error_page.html', {'error': 'You do not have permission to view this page.'})

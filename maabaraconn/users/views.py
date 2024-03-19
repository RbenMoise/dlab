from django.shortcuts import render, HttpResponse
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

from .forms import GradeForm, UserRegistrationForm, CourseForm, LabReportForm


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
        # Logic for student dashboard
        return render(request, 'users/student_dashboard.html')
    elif request.user.role == User.Role.LECTURER:
        # Logic for lecturer dashboard
        return render(request, 'users/lecturer_dashboard.html')
    elif request.user.role == User.Role.LAB_TECH:
        # Logic for lab technician dashboard
        return render(request, 'users/labtech_dashboard.html')
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

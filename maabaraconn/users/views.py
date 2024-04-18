from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.forms import modelformset_factory
from django.shortcuts import get_object_or_404, render, HttpResponse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.generic import CreateView, ListView, UpdateView
from .models import Course, LabReport, Laboratory, LabTemplate, Grade, SectionType, StudentResponse, TemplateSection, User
# Assume these forms are defined in forms.py
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from .models import Laboratory
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import GradeForm, LabTemplateForm, LaboratoryForm, SectionFormset, SectionTypeForm, TemplateSectionForm, UserRegistrationForm, CourseForm, LabReportForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Course
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Prefetch


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
            creator=request.user)  # Example query
        grades = Grade.objects.filter(
            lab_report__creator=request.user)  # Example query
        enrolled_courses = request.user.enrolled_courses.all()
        # Assuming Course is your model name
        available_courses = Course.objects.exclude(
            id__in=enrolled_courses.values_list('id', flat=True))

        # Assuming you're fetching lab_reports and grades somehow
        lab_reports = LabReport.objects.filter(creator=request.user)
        grades = Grade.objects.filter(lab_report__creator=request.user)
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
        my_laboratories = Laboratory.objects.filter(creator=request.user)
        templates = LabTemplate.objects.all()
        my_lab_reports = LabReport.objects.filter(creator=request.user)
        section_types = SectionType.objects.all()
        context = {
            'templates': templates,
            'section_types': section_types,
            'my_laboratories': my_laboratories,
            'my_lab_reports': my_lab_reports,
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


def get_laboratories_for_course(request):
    course_id = request.GET.get('course_id')
    laboratories = list(Laboratory.objects.filter(
        course_id=course_id).values('id', 'name'))
    return JsonResponse(laboratories, safe=False)


@login_required
def add_laboratory(request):
    if request.method == 'POST':
        form = LaboratoryForm(request.POST)
        if form.is_valid():
            # Save the form temporarily without committing to the database
            laboratory = form.save(commit=False)
            laboratory.creator = request.user  # Set the current user as the creator
            laboratory.save()  # Now save the laboratory instance to the database
            return redirect('labtech_dashboard')  # Redirect to the desired URL
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
        return render(request, 'labtech_dashboard.html', context)
    else:
        # Redirect or show an error message if the user is not a lab technician
        return render(request, 'error_page.html', {'error': 'You do not have permission to view this page.'})


@login_required
def delete_laboratory(request, lab_id):
    # Ensure labtech owns the lab
    laboratory = get_object_or_404(Laboratory, id=lab_id, creator=request.user)
    laboratory.delete()
    messages.success(request, 'Laboratory successfully deleted.')
    # Replace 'labtech_dashboard' with the name of your dashboard URL
    return redirect(reverse('labtech_dashboard'))


def course_detail(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    # Assuming LabReport has a course FK
    lab_reports = LabReport.objects.filter(course=course)
    return render(request, 'users/course_detail.html', {'course': course, 'lab_reports': lab_reports})


@login_required
def student_dashboard(request):
    enrolled_courses = request.user.enrolled_courses.prefetch_related(
        'lab_reports').all()
    lab_reports = LabReport.objects.filter(course__in=enrolled_courses)
    return render(request, 'users/student_dashboard.html', {'lab_reports': lab_reports})


@login_required
def lab_report_detail(request, lab_report_id):
    lab_report = get_object_or_404(LabReport, pk=lab_report_id)
    template = lab_report.template
    sections = template.sections.all() if template else []

    if request.method == 'POST':
        for section in sections:
            response_text = request.POST.get(f'response_{section.id}', '')
            StudentResponse.objects.update_or_create(
                section=section, student=request.user,
                defaults={'response_text': response_text}
            )
        return redirect('student_dashboard')

    responses = {response.section.id: response.response_text for response in
                 StudentResponse.objects.filter(student=request.user, section__in=sections)}

    context = {
        'lab_report': lab_report,
        'sections': sections,
        'responses': responses,
    }
    return render(request, 'course/lab_report_detail.html', context)


def is_labtech(user):
    return user.role == User.Role.LAB_TECH


@login_required
@user_passes_test(is_labtech)
def lab_template_upload(request, lab_id):
    lab = Laboratory.objects.get(id=lab_id)
    if request.method == 'POST':
        form = LabTemplateForm(request.POST, request.FILES, instance=lab.template if hasattr(
            lab, 'template') else None)
        if form.is_valid():
            lab_template = form.save(commit=False)
            lab_template.laboratory = lab
            lab_template.save()
            return redirect('labtech_dashboard')
    else:
        form = LabTemplateForm(
            instance=lab.template if hasattr(lab, 'template') else None)
    return render(request, 'course/upload_lab_template.html', {'form': form})


# @login_required
# # @user_passes_test(is_labtech)
# def list_lab_templates(request):
#     templates = LabTemplate.objects.all()
#     return render(request, 'users/labtech_dashboard.html', {'templates': templates})

@login_required
def LabTemplateDelete(request, template_id):
    # Ensure only lab technicians can delete templates
    if request.user.role != request.user.Role.LAB_TECH:
        return HttpResponseForbidden()

    template = get_object_or_404(LabTemplate, id=template_id)
    template.delete()
    # Redirect to the page where templates are listed, adjust the URL as necessary
    return redirect('labtech_dashboard')


def laboratories_list(request):
    laboratories = Laboratory.objects.prefetch_related('lab_templates').all()
    return render(request, 'laboratories_list.html', {'laboratories': laboratories})


# def create_lab_template(request):
#     if request.method == 'POST':
#         form = LabTemplateForm(request.POST)
#         if form.is_valid():
#             lab_template = form.save()
#             return redirect('add_sections_to_template', lab_template_id=lab_template.id)
#     else:
#         form = LabTemplateForm()
#     return render(request, 'course/create_lab_template.html', {'form': form})


def add_sections_to_template(request, lab_template_id):
    template = LabTemplate.objects.get(id=lab_template_id)
    SectionFormset = modelformset_factory(
        TemplateSection, form=TemplateSectionForm, )
    if request.method == 'POST':
        formset = SectionFormset(
            request.POST, queryset=TemplateSection.objects.none())
        if formset.is_valid():
            sections = formset.save(commit=False)
            for section in sections:
                section.lab_template = template
                section.save()
            # Redirect after POST
            print("Redirecting to labtech_dashboard")
            return redirect('labtech_dashboard', )
    else:
        # print(formset.errors)
        formset = SectionFormset(queryset=template.sections.all())
    return render(request, 'course/add_sections_to_template.html', {'formset': formset, 'template': template})


def create_lab_template(request, lab_template_id):
    template = LabTemplate.objects.get(id=lab_template_id)
    if request.method == 'POST':
        form = LabTemplateForm(request.POST)
        if form.is_valid():
            lab_template = form.save()
            section_formset = SectionFormset(
                request.POST, instance=lab_template)
            if section_formset.is_valid():
                section_formset.save()
                return redirect('add_sections_to_template', lab_template_id=template.id)
    else:
        form = LabTemplateForm()
        section_formset = SectionFormset()
    return render(request, 'create_lab_template.html', {
        'form': form,
        'section_formset': section_formset,
    })


def add_section_type(request):
    if request.method == 'POST':
        form = SectionTypeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('labtech_dashboard')
    else:
        form = SectionTypeForm()
    return render(request, 'course/add_section_type.html', {'form': form})


def delete_section_type(request, section_type_id):
    if request.method == 'POST':
        SectionType.objects.filter(id=section_type_id).delete()
        return HttpResponseRedirect(reverse('labtech_dashboard'))


def view_template_details(request, lab_template_id):
    template = get_object_or_404(LabTemplate, id=lab_template_id)
    sections = template.sections.all()  # Fetch all related sections

    context = {
        'template': template,
        'sections': sections,
    }
    return render(request, 'users/template_details.html', context)


def delete_section(request, lab_template_id, section_id):
    section = get_object_or_404(
        TemplateSection, id=section_id, lab_template_id=lab_template_id)
    if request.method == "POST":
        section.delete()
        return redirect('view_template_details', lab_template_id=lab_template_id)
    else:
        # Confirm deletion page (optional)
        return render(request, 'your_app_name/confirm_delete.html', {'section': section})


@login_required
def submit_lab_report(request, lab_report_id):
    lab_report = get_object_or_404(LabReport, pk=lab_report_id)
    if request.method == 'POST' and request.FILES['submitted_file']:
        # Handle the file upload
        submitted_file = request.FILES['submitted_file']
        # Assume you have a model field in LabReport to store submitted files
        lab_report.submitted_file = submitted_file
        lab_report.save()
        messages.success(request, "Lab report submitted successfully.")
        return redirect('student_dashboard')

    # Redirect to the detail page if the conditions are not met
    return redirect('lab_report_detail', lab_report_id=lab_report_id)


# def lab_reports_for_grading(request):
#     if request.user.role == 'LT':  # Ensure this matches your role system
#         # Fetch lab reports related to the logged-in lab tech's laboratories
#         reports = LabReport.objects.filter(laboratory__creator=request.user)
#         print(reports)  # Debug: Print to console to see what's being fetched
#     else:
#         reports = LabReport.objects.none()

#     context = {
#         'reports': reports
#     }
#     return render(request, 'course/grading_list.html', context)

@login_required
def lab_reports_for_grading(request):
    # Assuming lab technicians have broader access, adjust the filter as needed.
    if request.user.role == User.Role.LAB_TECH:
        reports = LabReport.objects.filter(
            status='Pending').order_by('submitted_at')
    else:
        reports = LabReport.objects.none()  # No access for other roles

    return render(request, 'course/grading_list.html', {'reports': reports})


@login_required
def view_grades(request):
    if request.user.role == User.Role.LAB_TECH:
        reports = LabReport.objects.filter(grade__isnull=False).select_related(
            'student').order_by('-submitted_at')
    else:
        reports = LabReport.objects.none()  # No access for other roles

    return render(request, 'course/view_grades.html', {'reports': reports})


# @login_required
# def lab_report_detail(request, report_id):
#     if request.user.role != 'LT':
#         return HttpResponse("You do not have permission to view this page.", status=403)

#     lab_report = get_object_or_404(LabReport, pk=report_id)
#     responses = lab_report.studentresponse_set.all()  # Default related name usage

#     return render(request, 'lab_technician/lab_report_detail.html', {
#         'lab_report': lab_report,
#         'responses': responses
#     })


# @login_required
# def view_student_lab_reports(request):
#     if request.user.role != 'Student':  # Assuming there's a role attribute to differentiate users
#         return HttpResponse("You are not authorized to view this page.", status=403)

#     # Assuming LabReport has a direct relationship or you can adjust based on your model
#     lab_reports = LabReport.objects.filter(students=request.user)
#     responses = StudentResponse.objects.filter(student=request.user)

#     context = {
#         'lab_reports': lab_reports,
#         'responses': responses
#     }
#     return render(request, 'student/lab_reports.html', context)


# @login_required
# def student_response_detail(request, response_id):
#     # Fetch the response; ensure it belongs to the logged-in student
#     response = get_object_or_404(
#         StudentResponse, id=response_id, student=request.user)

#     return render(request, 'students/response_detail.html', {
#         'response': response
#     })


# @login_required
# def view_lab_reports(request):
#     # Ensure this view is only accessible to students
#     if not request.user.is_student:  # Adjust this check based on your user model
#         return HttpResponse("You do not have permission to view this page.", status=403)

#     # Fetch all lab reports for the logged-in student
#     student_responses = StudentResponse.objects.filter(
#         student=request.user).select_related('lab_report')

#     return render(request, 'course/view_lab_reports.html', {
# #         'student_responses': student_responses
#     })

# the new views


# def view_response(request, response_id):
#     response = get_object_or_404(
#         StudentResponse, id=response_id, student=request.user)
#     return render(request, 'course/view_response.html', {'response': response})


def student_lab_report_responses(request, lab_report_id):
    lab_report = get_object_or_404(LabReport, id=lab_report_id)
    # Ensure responses are filtered for both lab report and the logged-in student
    responses = lab_report.responses.filter(student=request.user)
    return render(request, 'course/students_response.html', {
        'lab_report': lab_report,
        'responses': responses
    })

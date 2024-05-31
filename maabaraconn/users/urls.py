from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),

    #     login url
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),

    #     #     bashboard
    #     path('', views.dashboard, name='dashboard'),


    path('register/', views.register, name='register'),
    path('add_course/', views.CourseCreateView.as_view(),
         name='add_course'),
    path('submit_report/', views.LabReportSubmitView.as_view(),
         name='submit_report'),
    path('grade_report/<int:pk>/',
         views.GradeReportView.as_view(), name='grade_report'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/student/', views.dashboard, name='student_dashboard'),
    path('dashboard/lecturer/', views.dashboard,
         name='lecturer_dashboard'),
    path('dashboard/labtech/', views.dashboard, name='labtech_dashboard'),
    path('add_course/', views.CourseCreateView.as_view(), name='add_course'),
    path('delete_course/<int:course_id>/',
         views.delete_course, name='delete_course'),
    path('enroll_course/', views.enroll_course, name='enroll_course'),
    path('unenroll_course/', views.unenroll_course, name='unenroll_course'),
    path('lab_reports/upload/<int:course_id>/',
         views.upload_lab_report, name='upload_lab_report'),
    path('add_laboratory/', views.add_laboratory, name='add_laboratory'),
    path('lab_content/', views.my_creations, name='view_lab_content'),
    path('course/<int:course_id>/', views.course_detail, name='course_detail'),
    path('ajax/get_laboratories/',
         views.get_laboratories_for_course, name='get_laboratories'),
    path('laboratory/delete/<int:lab_id>/',
         views.delete_laboratory, name='delete_laboratory'),
    path('upload_lab_report/<int:course_id>/',
         views.upload_lab_report, name='upload_lab_report'),
    path('student/dashboard/', views.student_dashboard, name='student_dashboard'),

    # for the student to go to the response page vf
    path('lab-reports/<int:lab_report_id>/',
         views.lab_report_detail, name='lab_report_detail'),



    #     path('upload_template/', views.upload_lab_template,
    #          name='upload_lab_template'),
    #     path('list_templates/', views.list_lab_templates, name='list_lab_templates'),
    path('lab/<int:lab_id>/upload_template/',
         views.lab_template_upload, name='lab_template_upload'),
    path('lab/template/delete/<int:template_id>/',
         views.LabTemplateDelete, name='lab_template_delete'),
    path('laboratories/', views.laboratories_list, name='laboratories_list'),
    #     path('lab_template/create/', views.create_lab_template, name='create_lab_template'),
    path('lab_template/<int:lab_template_id>/add_section/',
         views.add_sections_to_template, name='add_sections_to_template'),
    path('add_section_type/', views.add_section_type, name='add_section_type'),
    path('delete_section_type/<int:section_type_id>/',
         views.delete_section_type, name='delete_section_type'),

    #     the tech is viewing the template and it s sections vf
    path('lab_template/<int:lab_template_id>/',
         views.view_template_details, name='view_template_details'),


    path('lab_template/<int:lab_template_id>/delete_section/<int:section_id>/',
         views.delete_section, name='delete_section'),
    path('submit_lab_report/<int:lab_report_id>/',
         views.submit_lab_report, name='submit_lab_report'),
    #     tech to view the reports by diffrent students
    path('lab-reports/grading/', views.lab_reports_for_grading,
         name='lab_reports_for_grading'),

    #     when tech clickes on view grades vf 
    path('lab-reports/grades/', views.view_grades, name='view_grades'),
    # urls.py

    path('lab-report/<int:lab_report_id>/responses/',
         views.student_lab_report_responses, name='student_lab_report_responses'),
    path('responses/<int:lab_report_id>/', views.student_lab_report_responses,
         name='student_lab_report_responses'),



    # for viewing all pending lab reports
    path('lab-reports/', views.lab_reports_for_grading,
         name='lab_reports_for_grading'),

    #     now the upper has been clicked to view labreports by students
    path('lab-report/<int:lab_report_id>/',
         views.lab_report_detail_for_tech, name='lab_report_detail_for_tech'),

    # to direct lec to section response by indiv std
    path('lab-report/<int:report_id>/student/<int:student_id>/responses/',
         views.detailed_responses, name='detailed_responses'),


    path('lab-report/<int:report_id>/grade/',
         views.grade_lab_report, name='grade_lab_report'),

    #     handling the detailed view of student responses page 1
    path('lab-reports/<int:lab_report_id>/responses/<int:student_id>/',
         views.student_lab_response, name='student_lab_response'),

    # other URL patterns
    path('', views.landing_page, name='landing_page'),

    # delete report
    path('delete_lab_report/<int:report_id>/',
         views.delete_lab_report, name='delete_lab_report'),

    #     view results
    path('student_lab_reports/', views.student_lab_reports,
         name='student_lab_reports'),


    # the first page when student views grades vf
    path('student/<int:student_id>/lab_reports/',
         views.student_lab_reports, name='student_lab_reports'),
    # for student to view there delated grades vf
    path('lab_report/<int:report_id>/student/<int:student_id>/marks/',
         views.student_marks_detail, name='student_marks_detail'),





]

from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('', views.landing_page, name='landing_page'),
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

]

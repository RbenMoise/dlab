from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Course, User, Laboratory, LabTemplate, LabReport, Grade

admin.site.register(Course)
admin.site.register(User)
admin.site.register(Laboratory)
admin.site.register(LabTemplate)
admin.site.register(LabReport)
admin.site.register(Grade)

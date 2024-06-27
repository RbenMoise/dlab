from .models import Grade
from .models import StudentResponse, Grade
from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Course, TemplateSection, User, Laboratory, LabTemplate, LabReport, Grade, StudentResponse

admin.site.register(Course)
admin.site.register(User)
admin.site.register(Laboratory)
admin.site.register(LabTemplate)
admin.site.register(LabReport)
# admin.site.register(Grade)
admin.site.register(TemplateSection)
# admin.site.register(StudentResponse)


@admin.register(StudentResponse)
class StudentResponseAdmin(admin.ModelAdmin):
    list_display = ('id', 'student', 'lab_report',
                    'section', 'marks_awarded', 'tech_feedback')
    list_filter = ('lab_report', 'student')
    search_fields = ('student__username',
                     'lab_report__title', 'section__title')


# admin.py


class GradeAdmin(admin.ModelAdmin):
    list_display = ('lab_report', 'score', 'graded_by',
                    'graded_at', 'get_student_name')

    def get_student_name(self, obj):
        student_response = obj.lab_report.responses.first()
        if student_response:
            return student_response.student.username
        return "N/A"

    get_student_name.short_description = 'Student Name'


admin.site.register(Grade, GradeAdmin)

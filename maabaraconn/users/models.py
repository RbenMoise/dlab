from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
# cls
from django.contrib.auth.models import AbstractUser, Group, Permission


class User(AbstractUser):

    class Role(models.TextChoices):
        STUDENT = 'ST', _('Student')
        LAB_TECH = 'LT', _('Lab Technician')
        LECTURER = 'LE', _('Lecturer')

    # Extend the User model with a role field
    role = models.CharField(
        max_length=2,
        choices=Role.choices,
        default=Role.STUDENT,
    )

    # Override the groups and user_permissions fields to set a custom related_name
    groups = models.ManyToManyField(Group, verbose_name=_('groups'), blank=True, help_text=_(
        'The groups this user belongs to. A user will get all permissions granted to each of their groups.'),
        related_name="user_set_custom",
        related_query_name="user",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('user permissions'),
        blank=True,
        help_text=_('Specific permissions for this user.'),
        related_name="user_set_custom",
        related_query_name="user",
    )


class Course(models.Model):
    name = models.CharField(max_length=255, unique=True)
    code = models.CharField(max_length=10, unique=True)
    lecturer = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='courses')

    def __str__(self):
        return f"{self.code} - {self.name}"

    student = models.ManyToManyField(
        User, related_name='enrolled_courses', blank=False)


class Laboratory(models.Model):
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name='laboratories')
    name = models.CharField(max_length=255)
    # description = models.TextField(blank=True)
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='laboratories')

    def __str__(self):
        return self.name


class LabTemplate(models.Model):
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name='lab_templates')
    name = models.CharField(max_length=255)
    # template_file = models.FileField(upload_to='lab_templates/')
    laboratory = models.ForeignKey(
        Laboratory, on_delete=models.CASCADE, related_name='lab_templates')

    def __str__(self):
        return f"{self.name} Template for {self.course.name}"


class SectionType(models.Model):
    name = models.CharField(max_length=100)
    default_content = models.TextField(blank=True)

    def __str__(self):
        return self.name


class TemplateSection(models.Model):
    lab_template = models.ForeignKey(
        LabTemplate, on_delete=models.CASCADE, related_name='sections')
    title = models.CharField(max_length=255)
    # order = models.IntegerField(
    # help_text="The order in which the section appears in the template")
    content = models.TextField()
    visible_to_students = models.BooleanField(default=True)
    section_type = models.ForeignKey(SectionType, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.title} for this {self.lab_template}'


class LabReport(models.Model):
    REPORT_TYPE_CHOICES = [
        ('IND', 'Individual'),
        ('GRP', 'Group'),]
    report_type = models.CharField(
        max_length=3, choices=REPORT_TYPE_CHOICES, default='IND')
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='lab_reports')
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name='lab_reports')
    title = models.CharField(max_length=255)
    description = models.TextField()
    # student = models.ForeignKey(
    # User, on_delete=models.CASCADE, related_name='lab_reports')
    laboratory = models.ForeignKey(
        Laboratory, on_delete=models.CASCADE, related_name='lab_reports', null=True)
    document = models.FileField(upload_to='lab_reports/')
    submitted_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=100, default='Pending')
    template = models.ForeignKey(
        LabTemplate, on_delete=models.SET_NULL, null=True, blank=True, related_name='lab_reports')

    def __str__(self):
        return f"Report by {self.creator} for {self.laboratory.name}"


class StudentResponse(models.Model):
    section = models.ForeignKey(
        TemplateSection, on_delete=models.CASCADE, related_name='responses')
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='responses')
    response_text = models.TextField()
    lab_report = models.ForeignKey(
        LabReport, on_delete=models.CASCADE, related_name='responses')

    def __str__(self):
        return f"Response by {self.student} for {self.section}"


class Grade(models.Model):
    lab_report = models.OneToOneField(
        LabReport, on_delete=models.CASCADE, related_name='grade')
    score = models.DecimalField(max_digits=5, decimal_places=2)
    feedback = models.TextField(blank=True)
    graded_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='graded_reports')
    graded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Grade for {self.lab_report.student.username} - {self.score}/100"


class LabReportSubmission(models.Model):
    lab_report_template = models.ForeignKey(
        LabReport, related_name='submissions', on_delete=models.CASCADE)
    student = models.ForeignKey(
        User, related_name='lab_submissions', on_delete=models.CASCADE)
    submitted_at = models.DateTimeField(auto_now_add=True)
    document = models.FileField(upload_to='lab_submissions/')

    def __str__(self):
        return f"{self.lab_report_template.title} by {self.student.username}"

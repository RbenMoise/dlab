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
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=10)
    lecturer = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='courses')

    def __str__(self):
        return f"{self.code} - {self.name}"

    enrolled_students = models.ManyToManyField(
        User, related_name='enrolled_courses')


class Laboratory(models.Model):
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name='laboratories')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.title


class LabTemplate(models.Model):
    laboratory = models.OneToOneField(
        Laboratory, on_delete=models.CASCADE, related_name='template')
    template_file = models.FileField(upload_to='lab_templates/')

    def __str__(self):
        return f"Template for {self.laboratory.title}"


class LabReport(models.Model):
    student = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='lab_reports')
    laboratory = models.ForeignKey(
        Laboratory, on_delete=models.CASCADE, related_name='lab_reports')
    submittion_file = models.FileField(upload_to='lab_reports/')
    submitted_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=100, default='Pending')

    def __str__(self):
        return f"Report by {self.student.username} for {self.laboratory.title}"


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

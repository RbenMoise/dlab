from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Grade, User, Course, LabReport


from .models import User


class UserRegistrationForm(UserCreationForm):
    # Add a role field
    role = forms.ChoiceField(choices=User.Role.choices, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'role']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = self.cleaned_data['role']
        if commit:
            user.save()
        return user


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['name', 'code']


class LabReportForm(forms.ModelForm):
    class Meta:
        model = LabReport
        fields = ['submittion_file', ]

# If you have a Grade model and form


class GradeForm(forms.ModelForm):
    class Meta:
        model = Grade
        fields = ['score', 'feedback']

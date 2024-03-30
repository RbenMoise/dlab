from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Grade, Laboratory, User, Course, LabReport


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
    # def __init__(self, *args, **kwargs):
    #     super(LabReportForm, self).__init__(*args, **kwargs)
    #     # Assuming you have a relationship to Course in your LabReport model
    #     # Adjust this queryset as needed
    #     self.fields['course'].queryset = Course.objects.all()

    def __init__(self, *args, **kwargs):
        course_id = kwargs.pop('course_id', None)
        super(LabReportForm, self).__init__(*args, **kwargs)
        if course_id:
            self.fields['laboratory'].queryset = Laboratory.objects.filter(
                course_id=course_id)

    class Meta:
        model = LabReport
        fields = ['document', 'title', 'description', 'laboratory']

# If you have a Grade model and form


class LaboratoryForm(forms.ModelForm):
    class Meta:
        model = Laboratory
        fields = ['name', 'course']


class GradeForm(forms.ModelForm):
    class Meta:
        model = Grade
        fields = ['score', 'feedback']

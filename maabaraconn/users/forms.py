from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Grade, LabTemplate, Laboratory, SectionType, TemplateSection, User, Course, LabReport


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
    def __init__(self, *args, **kwargs):
        course_id = kwargs.pop('course_id', None)
        super(LabReportForm, self).__init__(*args, **kwargs)
        if course_id:
            self.fields['laboratory'].queryset = Laboratory.objects.filter(
                course_id=course_id)
            self.fields['template'].queryset = LabTemplate.objects.filter(
                course_id=course_id)

    class Meta:
        model = LabReport
        fields = ['title', 'description', 'laboratory', 'template', 'document']
# If you have a Grade model and form


class LaboratoryForm(forms.ModelForm):
    class Meta:
        model = Laboratory
        fields = ['name', 'course']


class GradeForm(forms.ModelForm):
    class Meta:
        model = Grade
        fields = ['score', 'feedback']


class LabTemplateForm(forms.ModelForm):
    class Meta:
        model = LabTemplate
        fields = ['course', 'name', ]


class TemplateSectionForm(forms.ModelForm):
    class Meta:
        model = TemplateSection
        fields = ['section_type', 'content', 'visible_to_students']


SectionFormset = forms.inlineformset_factory(
    LabTemplate, TemplateSection, form=TemplateSectionForm, extra=1, can_delete=True)


class SectionTypeForm(forms.ModelForm):
    class Meta:
        model = SectionType
        fields = ['name', 'default_content']

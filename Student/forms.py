from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Student, Assignment, Exam, Course, Program
from multiselectfield import MultiSelectField


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField(max_length=254)

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

        for fieldnames in ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']:
            self.fields[fieldnames].help_text = None
            self.fields[fieldnames].widget.attrs.update({'class': 'form-control autofocus'})

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Student
        course = forms.SelectMultiple()
        fields = ('first_name', 'last_name', 'email', 'picture', 'program', 'semester', 'course')

        def __init__(self, *args, **kwargs):
            super(ProfileForm, self).__init__(*args, **kwargs)

            for fieldnames in ['first_name', 'last_name', 'email', 'picture', 'program', 'semester', 'course']:
                self.fields[fieldnames].help_text = None
                self.fields[fieldnames].widget.attrs.update({'class': 'form-control autofocus'})


class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ('name', 'course', 'file', 'due_date')


class ExamForm(forms.ModelForm):
    class Meta:
        model = Exam
        fields = ('name', 'date', 'time', 'course')


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ('name', 'summary', 'program', 'credits', 'semester', 'level')


class ProgramForm(forms.ModelForm):
    class Meta:
        model = Program
        fields = ('name', 'summary')

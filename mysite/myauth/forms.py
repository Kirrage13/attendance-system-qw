from datetime import date

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

from attendance.models import StudentProfile, Group, TeacherProfile

User = get_user_model()

class StudentRegistrationForm(forms.ModelForm):
    group = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'password', 'university_id']

    def clean_password(self):
        password = self.cleaned_data.get("password")
        try:
            validate_password(password, self.instance)
        except ValidationError as e:
            self.add_error("password", e)
        return password

    def clean_group(self):
        group = self.cleaned_data['group']
        if not Group.objects.filter(name=group).exists():
            raise forms.ValidationError("This group does not exist.")
        return group

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_student = True
        if commit:
            user.set_password(self.cleaned_data['password'])
            user.save()
            group = Group.objects.get(name=self.cleaned_data['group'])
            StudentProfile.objects.create(user=user, group=group)
        return user


class TeacherRegistrationForm(forms.ModelForm):
    department = forms.CharField(max_length=100)

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'password', 'university_id']
        widgets = {
            'password': forms.PasswordInput(),
        }

    def clean_department(self):
        department = self.cleaned_data['department']
        if not department:
            raise forms.ValidationError("Department cannot be empty.")
        return department

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_teacher = True
        if commit:
            user.set_password(self.cleaned_data['password'])
            user.save()
            TeacherProfile.objects.create(user=user, department=self.cleaned_data['department'])
        return user

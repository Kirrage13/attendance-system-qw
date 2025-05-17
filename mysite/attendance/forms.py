from django import forms
from .models import Attendance, Lecture, Announcement, Group
from datetime import datetime
from django.utils import timezone

class MarkAttendanceForm(forms.Form):
    access_key = forms.CharField(label="Access Key", max_length=20)

    def clean_access_key(self):
        key = self.cleaned_data["access_key"]
        try:
            lecture = Lecture.objects.get(access_key=key)
        except Lecture.DoesNotExist:
            raise forms.ValidationError("Invalid access key.")

        if lecture.key_expires_at and lecture.key_expires_at < timezone.now():
            raise forms.ValidationError("Access key has expired.")

        self.cleaned_data["lecture"] = lecture
        return key

class CreateAnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = ["title", "message", "group"]
        widgets = {
            "title": forms.TextInput(attrs={"placeholder": "Title"}),
            "message": forms.Textarea(attrs={"placeholder": "Message", "rows": 4}),
        }

class CreateLectureForm(forms.ModelForm):
    class Meta:
        model = Lecture
        fields = ["subject", "start_time", "end_time", "group", "room_number"]
        widgets = {
            "start_time": forms.TimeInput(format="%H:%M", attrs={"type": "time"}),
            "end_time": forms.TimeInput(format="%H:%M", attrs={"type": "time"}),
        }

    def __init__(self, *args, **kwargs):
        teacher = kwargs.pop("teacher", None)
        super().__init__(*args, **kwargs)

        if teacher and teacher.department_fk:
            self.fields["group"].queryset = Group.objects.filter(department=teacher.department_fk)
        else:
            self.fields["group"].queryset = Group.objects.none()

    def save(self, commit=True, teacher=None):
        lecture = super().save(commit=False)
        lecture.date = datetime.today().date()
        if teacher:
            lecture.teacher = teacher
        if commit:
            lecture.save()
        return lecture

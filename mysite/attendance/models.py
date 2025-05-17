from django.contrib.auth.models import AbstractUser
from django.db import models
import secrets
from datetime import timedelta, datetime
from django.utils.timezone import now

class User(AbstractUser):
    username = None

    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)

    email = models.EmailField(unique=True)
    university_id = models.CharField(max_length=8, unique=True)
    birth_date = models.DateField(null=True, blank=True)
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Group(models.Model):
    name = models.CharField(max_length=100)
    department = models.ForeignKey("Department", null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"{self.name} ({self.department.name})"

class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.user.get_full_name()} (Student)"

class TeacherProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department_fk = models.ForeignKey("Department", null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"{self.user.get_full_name()} (Teacher)"

class Lecture(models.Model):
    subject = models.CharField(max_length=100)
    start_time = models.TimeField()
    end_time = models.TimeField()
    date = models.DateField()
    teacher = models.ForeignKey(TeacherProfile, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    room_number = models.CharField(max_length=20)
    students = models.ManyToManyField('StudentProfile', through='Attendance')
    access_key = models.CharField(max_length=20, blank=True, null=True)
    key_expires_at = models.DateTimeField(blank=True, null=True)

    def generate_access_key(self):
        self.access_key = secrets.token_urlsafe(8)
        self.key_expires_at = now() + timedelta(minutes=15)
        self.save()

    def __str__(self):
        start = datetime.combine(self.date, self.start_time)
        return f"{self.subject} ({start.strftime('%d.%m.%Y %H:%M')})"

class Attendance(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE)
    is_present = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.student.user.get_full_name()} - {self.lecture.subject} - {'Present' if self.is_present else 'Absent'}"

class Announcement(models.Model):
    teacher = models.ForeignKey(TeacherProfile, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Announcement: {self.title} — {self.teacher.user.get_full_name()} ({self.group.name})"




from django.urls import path
from .views import (
    att_index,
    student_page,
    teacher_page,
    teacher_attendance_summary,
    delete_lecture_from_summary,
)

app_name = 'attendance'

urlpatterns = [
    path("", att_index, name='index'),
    path("student/", student_page, name="student_page"),
    path("teacher/", teacher_page, name="teacher_page"),
    path("teacher/attendance/", teacher_attendance_summary, name="teacher_attendance_summary"),
    path("teacher/lecture/<int:pk>/delete_summary/", delete_lecture_from_summary, name="delete_lecture_summary"),

]
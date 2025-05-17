from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages


from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import UpdateView, DeleteView

from .models import Lecture, Announcement, Attendance, StudentProfile
from .forms import MarkAttendanceForm, CreateLectureForm, CreateAnnouncementForm


def att_index(request: HttpRequest):
    print(request)
    return HttpResponse("Hello, world. You're at the attendance index.")

def handle_attendance_submission(request, student):
    form = MarkAttendanceForm(request.POST)
    if form.is_valid():
        lecture = form.cleaned_data["lecture"]
        Attendance.objects.get_or_create(
            student=student, lecture=lecture, defaults={"is_present": True}
        )
        messages.success(request, f"Marked present for {lecture.subject}.")
        return True
    return False

@login_required
def student_page(request):
    if not hasattr(request.user, "studentprofile"):
        return redirect("attendance:index")

    student = request.user.studentprofile
    group = student.group
    now = timezone.now()

    if request.method == "POST":
        if handle_attendance_submission(request, student):
            return redirect("attendance:student_page")
        form = MarkAttendanceForm(request.POST)
    else:
        form = MarkAttendanceForm()

    lectures = Lecture.objects.filter(group=group, start_time__gte=now).order_by("start_time")
    announcements = Announcement.objects.filter(group=group).order_by("-created_at")[:10]

    today_lectures = lectures.filter(date=timezone.now().date()).exclude(attendance__student=student)

    context = {
        "user": request.user,
        "lectures": lectures,
        "announcements": announcements,
        "form": form,
        "today_lectures": today_lectures,
    }

    return render(request, "attendance/student-page.html", context)



@login_required
def teacher_page(request):
    if not hasattr(request.user, "teacherprofile"):
        return redirect("attendance:index")

    teacher = request.user.teacherprofile
    now = timezone.now()

    if request.method == "POST":
        if "create_lecture" in request.POST:
            if handle_lecture_creation(request, teacher):
                return redirect("attendance:teacher_page")
        elif "create_announcement" in request.POST:
            if handle_announcement_creation(request, teacher):
                return redirect("attendance:teacher_page")

    lecture_form = CreateLectureForm(teacher=teacher)
    announcement_form = CreateAnnouncementForm()

    upcoming_lectures = Lecture.objects.filter(teacher=teacher, start_time__gte=now).order_by("start_time")
    announcements = Announcement.objects.filter(teacher=teacher).order_by("-created_at")[:10]

    access_key = request.session.pop("last_lecture_key", None)
    last_lecture_id = request.session.pop("last_lecture_id", None)
    last_lecture = Lecture.objects.filter(id=last_lecture_id).first() if last_lecture_id else None

    context = {
        "user": request.user,
        "lectures": upcoming_lectures,
        "announcements": announcements,
        "lecture_form": lecture_form,
        "announcement_form": announcement_form,
        "now": now,
        "last_lecture_key": access_key,
        "last_lecture": last_lecture,
    }

    return render(request, "attendance/teacher-page.html", context)

def handle_lecture_creation(request, teacher):
    lecture_form = CreateLectureForm(request.POST, teacher=teacher)
    if lecture_form.is_valid():
        lecture = lecture_form.save(commit=False)
        lecture.teacher = teacher
        lecture.generate_access_key()
        lecture.save()
        request.session["last_lecture_key"] = lecture.access_key
        request.session["last_lecture_id"] = lecture.id
        messages.success(request, "Lecture created successfully.")
        return True
    return False

def handle_announcement_creation(request, teacher):
    announcement_form = CreateAnnouncementForm(request.POST)
    if announcement_form.is_valid():
        announcement = announcement_form.save(commit=False)
        announcement.teacher = teacher
        announcement.save()
        messages.success(request, "Announcement created successfully.")
        return True
    return False

@login_required
def teacher_attendance_summary(request):
    if not hasattr(request.user, "teacherprofile"):
        return redirect("attendance:index")

    teacher = request.user.teacherprofile

    lectures = Lecture.objects.filter(teacher=teacher).order_by("-date", "-start_time").prefetch_related("attendance_set__student")

    summary = []
    for lecture in lectures:
        attendance_records = Attendance.objects.filter(lecture=lecture).select_related("student__user")
        summary.append({
            "lecture": lecture,
            "records": attendance_records,
        })

    context = {
        "summary": summary,
    }
    return render(request, "attendance/teacher_attendance_summary.html", context)

@login_required
def delete_lecture_from_summary(request, pk):
    if not hasattr(request.user, "teacherprofile"):
        return redirect("attendance:index")

    lecture = get_object_or_404(Lecture, pk=pk, teacher=request.user.teacherprofile)
    lecture.delete()
    messages.success(request, "Lecture deleted successfully.")
    return redirect("attendance:teacher_attendance_summary")




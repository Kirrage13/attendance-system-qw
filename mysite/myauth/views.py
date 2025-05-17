from http.client import responses

from django.contrib.auth.views import LogoutView, LoginView
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView, CreateView

from myauth.forms import StudentRegistrationForm, TeacherRegistrationForm

def register(request):
    if request.method == 'POST':
        role = request.POST.get('role')
        if role == 'student':
            return redirect('myauth:student')
        elif role == 'teacher':
            return redirect('myauth:teacher')
        else:
            return HttpResponse("Invalid role", status=400)

    return render(request, "myauth/register.html")

def register_student(request):
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('myauth:login')
    else:
        form = StudentRegistrationForm()
    return render(request, 'myauth/student.html', {'form': form})

def register_teacher(request):
    if request.method == 'POST':
        form = TeacherRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('myauth:login')
    else:
        form = TeacherRegistrationForm()
    return render(request, 'myauth/teacher.html', {'form': form})

class MyLoginView(LoginView):
    template_name = "myauth/login.html"
    #redirect_authenticated_user = True

    def get_success_url(self):
        user = self.request.user
        if hasattr(user, "studentprofile"):
            return reverse_lazy("attendance:student_page")
        elif hasattr(user, "teacherprofile"):
            return reverse_lazy("attendance:teacher_page")
        return reverse_lazy("attendance:index")


def logout_view(request: HttpRequest) -> HttpResponse:
    logout(request)
    return redirect(reverse("myauth:login"))

class MyLogoutView(LogoutView):
    next_page = reverse_lazy("myauth:login")


def set_cookie_view(request: HttpRequest) -> HttpResponse:
    response = HttpResponse("Cookie set")
    response.set_cookie("username", request.user.username, max_age=3600)
    return response

def get_cookie_view(request: HttpRequest) -> HttpResponse:
    value = request.COOKIES.get("username", "default")
    return HttpResponse(f"Cookie value: {value!r}")

def set_session_view(request: HttpRequest) -> HttpResponse:
    request.session["foobar"] = "spameggs"
    return HttpResponse("Session set")

def get_session_view(request: HttpRequest) -> HttpResponse:
    value = request.session.get("foobar", "default")
    return HttpResponse(f"Session value: {value!r}")

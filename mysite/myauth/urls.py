from django.contrib.auth.views import LoginView
from django.urls import path
from django.views.generic import TemplateView

from .views import (
    get_cookie_view,
    set_cookie_view,
    set_session_view,
    get_session_view,
    MyLogoutView,
    MyLoginView,
    register_student,
    register_teacher,
    register,
)

app_name="myauth"

urlpatterns = [
   path("login/", MyLoginView.as_view(), name="login"),

    path('logout/', MyLogoutView.as_view(), name='logout'),
    path('register/', register, name='register'),
    path('student/', register_student, name='student'),
    path('teacher/', register_teacher, name='teacher'),

    path('cookie/get', get_cookie_view, name='cookie-get'),
    path('cookie/set', set_cookie_view, name='cookie-set'),

    path('session/set', set_session_view, name='session-set'),
    path('session/get', get_session_view, name='session-get'),


]
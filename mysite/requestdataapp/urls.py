from attendance.urls import path

from .views import process_get_view, user_form

app_name = "requestdataapp"

urlpatterns = [
    path("get/", process_get_view, name="get-view"),
    path("bio/", user_form, name="user-form"),
]
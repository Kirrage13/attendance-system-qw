from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Group, StudentProfile, TeacherProfile, Lecture, Attendance, Announcement, Department


class UserAdmin(BaseUserAdmin):
    model = User
    list_display = ("first_name", "last_name", "email", "university_id", "is_student", "is_teacher")
    list_filter = ("is_student", "is_teacher")
    ordering = ("email",)
    search_fields = ("email", "university_id")

    fieldsets = (
        (None, {"fields": ("first_name", "last_name","email", "password")}),
        (("Personal info"), {"fields": ("university_id", "birth_date")}),
        (("Roles"), {"fields": ("is_student", "is_teacher")}),
        (("Permissions"), {
            "fields": (
                "is_active",
                "is_staff",
                "is_superuser",
                "groups",
                "user_permissions",
            )
        }),
        (("Important dates"), {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (None, {
                "classes": ("wide",),
            "fields": ("first_name", "last_name", "email", "password1", "password2", "university_id", "birth_date", "is_student", "is_teacher"),
        }),
    )

class AttendanceInline(admin.TabularInline):
    model = Attendance
    extra = 0
    autocomplete_fields = ["student"]

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ["name"]

@admin.register(Lecture)
class LectureAdmin(admin.ModelAdmin):
    list_display = ["subject", "teacher", "group", "date", "start_time", "end_time"]
    inlines = [AttendanceInline]

@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ["get_first_name", "get_last_name","user", "group"]
    search_fields = ["user__username", "user__group"]

    @admin.display(description="First Name")
    def get_first_name(self, obj):
        return obj.user.first_name

    @admin.display(description="Last Name")
    def get_last_name(self, obj):
        return obj.user.last_name

@admin.register(TeacherProfile)
class TeacherProfileAdmin(admin.ModelAdmin):
    list_display = ["get_first_name", "get_last_name", "user", "get_department"]
    list_filter = ("department_fk",)
    search_fields = ("user__first_name", "user__last_name", "department_fk__name")

    def get_department(self, obj):
        return obj.department_fk.name if obj.department_fk else "-"
    get_department.short_description = "Department"

    @admin.display(description="First Name")
    def get_first_name(self, obj):
        return obj.user.first_name

    @admin.display(description="Last Name")
    def get_last_name(self, obj):
        return obj.user.last_name

@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ["name", "get_department"]

    def get_department(self, obj):
        if obj.department:
            return obj.department.name
        return "—"
    get_department.short_description = "Department"

@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ["title", "teacher", "group", "created_at"]

admin.site.register(User, UserAdmin)
admin.site.register(Attendance)
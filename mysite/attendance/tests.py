from django.test import TestCase
from django.urls import reverse

from attendance.models import User, StudentProfile, Group
from attendance.utils import generate_access_key

class UtilityFunctionTests(TestCase):
    def test_generate_access_key_length(self):
        key = generate_access_key()
        self.assertEqual(len(key), 6)

    def test_generate_access_key_unique(self):
        keys = {generate_access_key() for _ in range(1000)}
        self.assertEqual(len(keys), 1000)

class StudentRegistrationTests(TestCase):
    def test_valid_student_registration(self):
        Group.objects.create(name="KCA2D2")
        response = self.client.post(reverse("myauth:student"), {
            "email": "user@example.com",
            "first_name": "Kirill",
            "last_name": "Vatlin",
            "password": "TestPass123",
            "university_id": "ST-0001",
            "group": "KCA2D2"
        })

        HTTP_USER_AGENT = "TestAgent/1.0"
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(email="user@example.com").exists())
        self.assertTrue(StudentProfile.objects.filter(user__email="user@example.com").exists())


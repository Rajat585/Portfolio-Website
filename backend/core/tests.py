from django.test import TestCase
from django.urls import reverse
from .models import Project


class HomePageTests(TestCase):
    def test_home_page_loads(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)


class ContactApiTests(TestCase):
    def test_rejects_incomplete_payload(self):
        response = self.client.post(
            "/api/contact/",
            data={"name": "Test"},
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)


class ProjectModelTests(TestCase):
    def test_tech_stack_list_parses_csv(self):
        p = Project(title="X", description="d", tech_stack="Django, MySQL, Bootstrap")
        self.assertEqual(p.tech_stack_list, ["Django", "MySQL", "Bootstrap"])

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r"projects", views.ProjectViewSet, basename="project")
router.register(r"certifications", views.CertificationViewSet, basename="certification")
router.register(r"internships", views.InternshipViewSet, basename="internship")
router.register(r"testimonials", views.TestimonialViewSet, basename="testimonial")
router.register(r"blog", views.BlogPostViewSet, basename="blogpost")

urlpatterns = [
    path("contact/", views.contact_view, name="contact"),
    path("", include(router.urls)),
]

from rest_framework import serializers
from .models import (
    Project, Certification, Internship, Testimonial, BlogPost, ContactMessage
)


class ProjectSerializer(serializers.ModelSerializer):
    tech_stack_list = serializers.ReadOnlyField()

    class Meta:
        model = Project
        fields = [
            "id", "title", "description", "tech_stack", "tech_stack_list",
            "github_link", "live_demo_link", "icon", "is_featured", "order",
        ]


class CertificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certification
        fields = [
            "id", "title", "issuing_authority", "logo", "description",
            "is_verified", "date_issued", "order",
        ]


class InternshipSerializer(serializers.ModelSerializer):
    responsibilities_list = serializers.ReadOnlyField()

    class Meta:
        model = Internship
        fields = [
            "id", "company_name", "logo", "role", "location",
            "start_date", "end_date", "responsibilities_list", "order",
        ]


class TestimonialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Testimonial
        fields = ["id", "author_name", "author_role", "feedback", "rating", "order"]


class BlogPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogPost
        fields = [
            "id", "title", "slug", "excerpt", "content", "tag",
            "author", "published_at",
        ]


class ContactMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactMessage
        fields = ["name", "email", "message"]

    def validate_message(self, value):
        if len(value.strip()) < 10:
            raise serializers.ValidationError("Message is too short.")
        return value

from django.contrib import admin
from .models import (
    Project, Certification, Internship, Testimonial, BlogPost, ContactMessage
)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("title", "tech_stack", "is_featured", "order")
    list_editable = ("order", "is_featured")
    search_fields = ("title", "tech_stack")


@admin.register(Certification)
class CertificationAdmin(admin.ModelAdmin):
    list_display = ("title", "issuing_authority", "is_verified", "date_issued", "order")
    list_editable = ("order",)
    search_fields = ("title", "issuing_authority")


@admin.register(Internship)
class InternshipAdmin(admin.ModelAdmin):
    list_display = ("role", "company_name", "start_date", "end_date", "order")
    list_editable = ("order",)


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ("author_name", "author_role", "rating", "is_published", "order")
    list_editable = ("order", "is_published")


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ("title", "tag", "author", "is_published", "published_at")
    prepopulated_fields = {"slug": ("title",)}
    list_editable = ("is_published",)
    search_fields = ("title", "content")


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "email_sent", "whatsapp_sent", "created_at")
    readonly_fields = ("name", "email", "message", "ip_address", "created_at")
    list_filter = ("email_sent", "whatsapp_sent")

    def has_add_permission(self, request):
        # messages only ever come in through the public form
        return False

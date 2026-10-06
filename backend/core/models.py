"""
Core models for the portfolio.

Kept deliberately simple and well-documented so the recruiter (or anyone
reading the code) can see the data shape at a glance.
"""

from django.db import models
from django.utils.text import slugify


class TimeStampedModel(models.Model):
    """Abstract base adding created/updated timestamps to every model."""
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Project(TimeStampedModel):
    """A portfolio project shown in the Projects section."""
    title = models.CharField(max_length=120)
    description = models.TextField(help_text="2-3 line recruiter-friendly summary.")
    tech_stack = models.CharField(
        max_length=255, help_text="Comma-separated, e.g. 'Django, MySQL, Bootstrap'"
    )
    github_link = models.URLField(blank=True)
    live_demo_link = models.URLField(blank=True)
    icon = models.CharField(
        max_length=50, default="bi-code-slash",
        help_text="Bootstrap Icons class name shown on the project card."
    )
    is_featured = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "-created_at"]

    def __str__(self):
        return self.title

    @property
    def tech_stack_list(self):
        return [t.strip() for t in self.tech_stack.split(",") if t.strip()]


class Certification(TimeStampedModel):
    """A verified certification/credential."""
    title = models.CharField(max_length=150)
    issuing_authority = models.CharField(max_length=150)
    logo = models.ImageField(upload_to="certifications/", blank=True, null=True)
    description = models.CharField(max_length=255, blank=True)
    is_verified = models.BooleanField(default=True)
    date_issued = models.DateField(blank=True, null=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "-date_issued"]

    def __str__(self):
        return f"{self.title} — {self.issuing_authority}"


class Internship(TimeStampedModel):
    """Internship / professional experience entry."""
    company_name = models.CharField(max_length=150)
    logo = models.ImageField(upload_to="internships/", blank=True, null=True)
    role = models.CharField(max_length=150)
    location = models.CharField(max_length=120, blank=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    responsibilities = models.TextField(
        help_text="One responsibility per line — rendered as bullet points."
    )
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "-start_date"]

    def __str__(self):
        return f"{self.role} @ {self.company_name}"

    @property
    def responsibilities_list(self):
        return [line.strip() for line in self.responsibilities.splitlines() if line.strip()]


class Testimonial(TimeStampedModel):
    """Recruiter/client/mentor feedback shown in the carousel."""
    author_name = models.CharField(max_length=120)
    author_role = models.CharField(max_length=120, blank=True)
    feedback = models.TextField()
    rating = models.PositiveSmallIntegerField(default=5, help_text="Out of 5")
    is_published = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "-created_at"]

    def __str__(self):
        return f"{self.author_name} ({self.rating}★)"


class BlogPost(TimeStampedModel):
    """A short article/tutorial post."""
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    excerpt = models.CharField(max_length=280)
    content = models.TextField()
    tag = models.CharField(max_length=50, default="Django")
    author = models.CharField(max_length=100, default="Rajat Verma")
    is_published = models.BooleanField(default=True)
    published_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-published_at"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)[:220]
        super().save(*args, **kwargs)


class ContactMessage(TimeStampedModel):
    """A message submitted through the Contact section form."""
    name = models.CharField(max_length=120)
    email = models.EmailField()
    message = models.TextField()
    whatsapp_sent = models.BooleanField(default=False)
    email_sent = models.BooleanField(default=False)
    ip_address = models.GenericIPAddressField(blank=True, null=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} <{self.email}>"

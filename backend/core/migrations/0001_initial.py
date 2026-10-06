import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Project",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("title", models.CharField(max_length=120)),
                ("description", models.TextField(help_text="2-3 line recruiter-friendly summary.")),
                ("tech_stack", models.CharField(help_text="Comma-separated, e.g. 'Django, MySQL, Bootstrap'", max_length=255)),
                ("github_link", models.URLField(blank=True)),
                ("live_demo_link", models.URLField(blank=True)),
                ("icon", models.CharField(default="bi-code-slash", help_text="Bootstrap Icons class name shown on the project card.", max_length=50)),
                ("is_featured", models.BooleanField(default=True)),
                ("order", models.PositiveIntegerField(default=0)),
            ],
            options={"ordering": ["order", "-created_at"]},
        ),
        migrations.CreateModel(
            name="Certification",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("title", models.CharField(max_length=150)),
                ("issuing_authority", models.CharField(max_length=150)),
                ("logo", models.ImageField(blank=True, null=True, upload_to="certifications/")),
                ("description", models.CharField(blank=True, max_length=255)),
                ("is_verified", models.BooleanField(default=True)),
                ("date_issued", models.DateField(blank=True, null=True)),
                ("order", models.PositiveIntegerField(default=0)),
            ],
            options={"ordering": ["order", "-date_issued"]},
        ),
        migrations.CreateModel(
            name="Internship",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("company_name", models.CharField(max_length=150)),
                ("logo", models.ImageField(blank=True, null=True, upload_to="internships/")),
                ("role", models.CharField(max_length=150)),
                ("location", models.CharField(blank=True, max_length=120)),
                ("start_date", models.DateField(blank=True, null=True)),
                ("end_date", models.DateField(blank=True, null=True)),
                ("responsibilities", models.TextField(help_text="One responsibility per line — rendered as bullet points.")),
                ("order", models.PositiveIntegerField(default=0)),
            ],
            options={"ordering": ["order", "-start_date"]},
        ),
        migrations.CreateModel(
            name="Testimonial",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("author_name", models.CharField(max_length=120)),
                ("author_role", models.CharField(blank=True, max_length=120)),
                ("feedback", models.TextField()),
                ("rating", models.PositiveSmallIntegerField(default=5, help_text="Out of 5")),
                ("is_published", models.BooleanField(default=True)),
                ("order", models.PositiveIntegerField(default=0)),
            ],
            options={"ordering": ["order", "-created_at"]},
        ),
        migrations.CreateModel(
            name="BlogPost",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("title", models.CharField(max_length=200)),
                ("slug", models.SlugField(blank=True, max_length=220, unique=True)),
                ("excerpt", models.CharField(max_length=280)),
                ("content", models.TextField()),
                ("tag", models.CharField(default="Django", max_length=50)),
                ("author", models.CharField(default="Rajat Verma", max_length=100)),
                ("is_published", models.BooleanField(default=True)),
                ("published_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={"ordering": ["-published_at"]},
        ),
        migrations.CreateModel(
            name="ContactMessage",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("name", models.CharField(max_length=120)),
                ("email", models.EmailField(max_length=254)),
                ("message", models.TextField()),
                ("whatsapp_sent", models.BooleanField(default=False)),
                ("email_sent", models.BooleanField(default=False)),
                ("ip_address", models.GenericIPAddressField(blank=True, null=True)),
            ],
            options={"ordering": ["-created_at"]},
        ),
    ]

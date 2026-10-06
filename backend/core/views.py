import logging

import requests
from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render
from django_ratelimit.decorators import ratelimit
from rest_framework import viewsets, status
from rest_framework.decorators import api_view, throttle_classes
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle

from .models import Project, Certification, Internship, Testimonial, BlogPost, ContactMessage
from .serializers import (
    ProjectSerializer, CertificationSerializer, InternshipSerializer,
    TestimonialSerializer, BlogPostSerializer, ContactMessageSerializer,
)

logger = logging.getLogger(__name__)


def home_view(request):
    """Render the single-page portfolio (templates/index.html)."""
    return render(request, "index.html")


# ---------------------------------------------------------------------------
# Read-only API viewsets — power the frontend sections dynamically once
# connected (currently the frontend ships with static/demo content, but can
# be switched to fetch from these endpoints).
# ---------------------------------------------------------------------------
class ProjectViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Project.objects.filter(is_featured=True)
    serializer_class = ProjectSerializer


class CertificationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Certification.objects.all()
    serializer_class = CertificationSerializer


class InternshipViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Internship.objects.all()
    serializer_class = InternshipSerializer


class TestimonialViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Testimonial.objects.filter(is_published=True)
    serializer_class = TestimonialSerializer


class BlogPostViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = BlogPost.objects.filter(is_published=True)
    serializer_class = BlogPostSerializer
    lookup_field = "slug"


# ---------------------------------------------------------------------------
# Contact endpoint — validates + captcha-checks + rate-limits + stores +
# sends an email notification + (optionally) pings a WhatsApp API.
# ---------------------------------------------------------------------------
def _verify_recaptcha(token: str) -> bool:
    """Verify a Google reCAPTCHA token server-side. Returns True if no
    secret key is configured (so local/dev setups without captcha still
    work) — set RECAPTCHA_SECRET_KEY in production to enforce it."""
    if not settings.RECAPTCHA_SECRET_KEY:
        return True
    if not token:
        return False
    try:
        resp = requests.post(
            "https://www.google.com/recaptcha/api/siteverify",
            data={"secret": settings.RECAPTCHA_SECRET_KEY, "response": token},
            timeout=5,
        )
        return resp.json().get("success", False)
    except requests.RequestException:
        logger.exception("reCAPTCHA verification failed")
        return False


def _send_via_brevo(to_email, to_name, subject, text_content):
    """Send email via Brevo's HTTP API (works even where SMTP ports are blocked,
    e.g. Render's free tier)."""
    try:
        resp = requests.post(
            "https://api.brevo.com/v3/smtp/email",
            headers={
                "api-key": settings.BREVO_API_KEY,
                "Content-Type": "application/json",
                "Accept": "application/json",
            },
            json={
                "sender": {"name": "Rajat Verma Portfolio", "email": settings.CONTACT_RECEIVER_EMAIL},
                "to": [{"email": to_email, "name": to_name}],
                "subject": subject,
                "textContent": text_content,
            },
            timeout=10,
        )
        print("BREVO STATUS:", resp.status_code)
        print("BREVO RESPONSE:", resp.text)
        print("BREVO API KEY SET:", bool(settings.BREVO_API_KEY))
        return resp.status_code in (200, 201)
    except requests.RequestException as e:
        print("BREVO EXCEPTION:", e)
        return False


def _send_contact_email(contact: ContactMessage) -> bool:
    subject = f"Portfolio contact — {contact.name}"
    message = f"Name: {contact.name}\nEmail: {contact.email}\n\n{contact.message}"

    if settings.BREVO_API_KEY:
        return _send_via_brevo(settings.CONTACT_RECEIVER_EMAIL, "Rajat", subject, message)

    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.CONTACT_RECEIVER_EMAIL],
            fail_silently=False,
        )
        return True
    except Exception:
        logger.exception("Failed to send contact email")
        return False


def _send_whatsapp_notification(contact: ContactMessage) -> bool:
    if not settings.TWILIO_ACCOUNT_SID or not settings.TWILIO_AUTH_TOKEN or not settings.TWILIO_WHATSAPP_FROM:
        print("WHATSAPP SKIPPED: Twilio env vars not set")
        return False
    try:
        url = f"https://api.twilio.com/2010-04-01/Accounts/{settings.TWILIO_ACCOUNT_SID}/Messages.json"
        resp = requests.post(
            url,
            auth=(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN),
            data={
                "From": f"whatsapp:{settings.TWILIO_WHATSAPP_FROM}",
                "To": f"whatsapp:{settings.WHATSAPP_TO_NUMBER}",
                "Body": f"New portfolio lead: {contact.name} ({contact.email})\n\n{contact.message[:200]}",
            },
            timeout=8,
        )
        print("WHATSAPP STATUS:", resp.status_code)
        print("WHATSAPP RESPONSE:", resp.text)
        return resp.status_code in (200, 201)
    except requests.RequestException as e:
        print("WHATSAPP EXCEPTION:", e)
        return False

def _send_visitor_confirmation_email(contact: ContactMessage) -> bool:
    subject = "Thanks for reaching out — Rajat Verma"
    message = (
        f"Hi {contact.name},\n\n"
        "Thanks for getting in touch through my portfolio! I've received "
        "your message and will get back to you soon.\n\n"
        f"Your message:\n{contact.message}\n\n"
        "— Rajat Verma"
    )

    if settings.BREVO_API_KEY:
        return _send_via_brevo(contact.email, contact.name, subject, message)

    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[contact.email],
            fail_silently=True,
        )
        return True
    except Exception:
        logger.exception("Failed to send visitor confirmation email")
        return False
@api_view(["POST"])
@throttle_classes([AnonRateThrottle])
@ratelimit(key="ip", rate="5/m", block=True)
def contact_view(request):
    """POST /api/contact/  { name, email, message, recaptcha_token? }"""
    serializer = ContactMessageSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    if not _verify_recaptcha(request.data.get("recaptcha_token", "")):
        return Response(
            {"detail": "Captcha verification failed."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    contact = serializer.save(
        ip_address=request.META.get("REMOTE_ADDR"),
    )

    contact.email_sent = _send_contact_email(contact)
    contact.whatsapp_sent = _send_whatsapp_notification(contact)
    _send_visitor_confirmation_email(contact)
    contact.save(update_fields=["email_sent", "whatsapp_sent"])
    
    return Response(
        {"detail": "Message received. Thank you for reaching out!"},
        status=status.HTTP_201_CREATED,
    )

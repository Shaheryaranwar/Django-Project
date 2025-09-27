from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.utils.text import slugify

import uuid
def send_email_to_client(recipient_email, student_name="Student"):
    subject = 'Welcome to Our Student Portal'
    html_message = f'<p>Hello <b>{student_name}</b>, this is a test email from Django.</p>'
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [recipient_email]

    send_mail(subject, "", from_email, recipient_list, html_message=html_message)

def genrate_slug(title: str) -> str:
    from .models import Recipe
    """
    Generate a unique slug for a given title.
    """
    title = slugify(title)
    while(Recipe.objects.filter(slug=title).exists()):
        title = f"{title}-{str(uuid.uuid4())[:8]}"
    return title
import logging

from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail, BadHeaderError
from django.db.models import Q
from django.template import loader
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from website.celery import app


@app.task
def send_verification_email(user_id, v_id):
    user_model = get_user_model()
    logging.info(user_model)
    try:
        user = user_model.objects.get(pk=user_id)
        subject = 'Verify your Market account'
        message = 'Follow this link to verify your account:'
        from_ = 'zinnatullin@mail.com'

        html = loader.render_to_string('account/registration/email_verification.html',
                                       {'code': str(v_id)})
        send_mail(subject, message, from_, [user.email], fail_silently=False, html_message=html)
    except user_model.DoesNotExist:
        logging.warning(f"Tried to send verification email to non-existing user {user_id}")


@app.task
def send_password_reset_email(user_email):
    try:
        associated_users = User.objects.filter(Q(email=user_email))
        if associated_users.exists():
            for user in associated_users:
                subject = "Password Reset Requested"
                email_template_name = "account/registration/password_reset_email.html"
                message = 'Follow this link to reset your password'
                c = {
                    "email": user.email,
                    'domain': '127.0.0.1:8000',
                    'site_name': 'Website',
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "user": user,
                    'token': default_token_generator.make_token(user),
                    'protocol': 'http',
                }
                email = loader.render_to_string(email_template_name, c)
                send_mail(subject, message, 'admin@example.com', [user.email], fail_silently=False, html_message=email)
        else:
            raise User.DoesNotExist("No such user")
    except BadHeaderError:
        logging.warning(f"Tried to send password reset email, take some errors {user_email}")
    except User.DoesNotExist:
        logging.warning(f"Tried to send verification email to non-existing user {user_email}")

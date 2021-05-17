import logging

from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.template import loader

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
        logging.warning("Tried to send verification email to non-existing user '%s'" % user_id)

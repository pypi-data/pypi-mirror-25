from celery import task
from django.utils.module_loading import import_string
from django.conf import settings


@task
def send_email(obj_id):
    from .models import EmailMessage
    message = EmailMessage.objects.get(id=obj_id)
    backend_class = import_string(settings.PCART_EMAIL_BACKEND)
    backend = backend_class(message)
    backend.send()

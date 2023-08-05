from __future__ import absolute_import  # for python 2.7

from django.conf import settings
from django.core.mail import send_mail as django_send_mail

try:
    from celery.task import task

except ImportError:
    def func_add_delay(func):
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        wrapper.delay = func
        return wrapper
    task = func_add_delay


@task
def send_mail(subject, message, to_emails):
    django_send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, to_emails)

from django.core.urlresolvers import reverse
from django.template import Context, Template
from django.template.loader import render_to_string
from django.utils.http import *

from . import tasks
from .tokens import account_activation_token, password_reset_token_generator


def send_reset_password_mail(request, user):
    print(user.pk)
    uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
    token = password_reset_token_generator.make_token(user)
    host = request.get_host()
    reset_url = reverse('password_reset_confirm', args=[uidb64, token])

    if request.is_secure():
        scheme = 'https://'
    else:
        scheme = 'http://'

    url = '{scheme}{host}{path}'.format(scheme=scheme, host=host, path=reset_url)

    context = {'url': url}
    message = render_to_string('django_auth2/mail/send_reset_password_mail.html', context)
    subject = 'Смена пароля'

    tasks.send_mail.delay(subject, message, [user.email])


def send_activation_mail(request, user):
    uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
    token = account_activation_token.make_token(user)
    host = request.get_host()
    activation_url = reverse('activate', args=[uidb64, token])

    if request.is_secure():
        scheme = 'https://'
    else:
        scheme = 'http://'

    url = '{scheme}{host}{path}'.format(scheme=scheme, host=host, path=activation_url)
    context = {'url': url}
    message = render_to_string('django_auth2/mail/send_activation_mail.html',
                               context)
    subject = 'Подтверждение аккаунта'

    tasks.send_mail.delay(subject, message, [user.email])

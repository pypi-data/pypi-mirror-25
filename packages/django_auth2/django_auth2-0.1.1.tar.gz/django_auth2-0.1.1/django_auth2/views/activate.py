from django.contrib import auth
from django.db.transaction import atomic
from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.views import View
from django.views.generic import FormView, TemplateView

from .. import forms, mails, utils
from ..tokens import account_activation_token
from ..utils import get_user_model


class ReSend(FormView):
    form_class = forms.RetrySendEmailForActivateForm
    template_name = 'django_auth2/activate/re_send.html'

    @atomic
    def form_valid(self, form):
        email = form.cleaned_data['email']
        user = utils.get_user(email=email)

        mails.send_activation_mail(self.request, user)

        return render(self.request, template_name='django_auth2/register/email_sended.html')

re_send = ReSend.as_view()


class Activate(View):

    @atomic
    def get(self, request, uidb64, token):

        user = self.get_user(uidb64)
        if not user or user.is_active or not self.token_valid(user, token):
            raise Http404

        user.is_active = True
        user.save()

        auth.login(request, user)
        return redirect(reverse('activation_success'))

    def get_user(self, uidb64):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            return utils.get_user(pk=uid)
        except get_user_model().DoesNotExist:
            return

    def token_valid(self, user, token):
        return account_activation_token.check_token(user, token)

activate = Activate.as_view()


class Success(TemplateView):
    template_name = 'django_auth2/activate/success.html'

success = Success.as_view()

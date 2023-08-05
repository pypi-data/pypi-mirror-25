from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from django.views.generic import FormView

from .. import forms, mails, utils
from ..tokens import password_reset_token_generator


class PasswordReset(FormView):
    form_class = forms.PasswordResetForm
    template_name = 'django_auth2/reset_password/form.html'
    success_url = reverse_lazy('password_reset_done')

    def form_valid(self, form):
        response = super().form_valid(form)

        user = form.get_user_from_email()
        mails.send_reset_password_mail(self.request, user)
        return response

password_reset = PasswordReset.as_view()


def password_reset_done(request, **kwargs):
    return auth_views.password_reset_done(
        request, template_name='django_auth2/reset_password/done.html',
        **kwargs
    )


def password_reset_confirm(request, **kwargs):
    return auth_views.password_reset_confirm(
        request,
        set_password_form=forms.SetPasswordForm,
        token_generator=password_reset_token_generator,
        template_name='django_auth2/reset_password/confirm.html',
        **kwargs
    )


def password_reset_complete(request, **kwargs):
    return auth_views.password_reset_done(
        request,
        template_name='django_auth2/reset_password/complete.html',
        **kwargs)

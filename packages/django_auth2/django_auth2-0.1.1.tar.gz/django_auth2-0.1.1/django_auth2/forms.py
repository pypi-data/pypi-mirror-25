# -*- coding:utf-8 -*-
from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import SetPasswordForm as DjangoSetPasswordForm
from django.contrib.auth.forms import AuthenticationForm

from . import utils


class LoginForm(AuthenticationForm):
    error_messages = {
        'invalid_login': 'Пожалуйста введите корректный логин или пароль',
        'inactive': 'Аккаунт не активен',
    }

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            user_kwargs = {utils.get_user_model().USERNAME_FIELD: username}
            try:
                user = utils.get_user(**user_kwargs)

                if not user.is_active:
                    raise forms.ValidationError(
                        'Аккаунт не активен, хотите выслать подтверждение еще раз?',
                        code='invalid_account',
                        # params={'username': self.username_field.verbose_name},
                    )
            except utils.get_user_model().DoesNotExist:
                raise forms.ValidationError(
                    self.error_messages['invalid_login'],
                    code='invalid_login',
                    # params={'username': self.username_field.verbose_name},
                )

            self.user_cache = authenticate(password=password, **user_kwargs)
            if self.user_cache is None:
                raise forms.ValidationError(
                    self.error_messages['invalid_login'],
                    code='invalid_login',
                )

        return self.cleaned_data


class RegisterForm(forms.ModelForm):
    password1 = forms.CharField(label='Пароль', strip=False, widget=forms.PasswordInput)
    password2 = forms.CharField(label='Повторите пароль',
                                widget=forms.PasswordInput,
                                strip=False,
                                help_text='Пароли должны совподать')

    class Meta:
        model = utils.get_user_model()
        fields = utils.get_user_model().REQUIRED_FIELDS + [utils.get_user_model().USERNAME_FIELD]

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                u'Пароли не совпадают',
                code='password_mismatch',
            )
        return password2

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        for field, value in self.cleaned_data.items():
            setattr(user, field, value)

        user.set_password(self.cleaned_data['password1'])

        if commit:
            user.save()
        return user


class RetrySendEmailForActivateForm(forms.Form):
    email = forms.EmailField(required=True, label='Email')

    def clean_email(self):
        email = self.cleaned_data['email']

        try:
            user = utils.get_user(email=email)

            if user.is_active:
                raise forms.ValidationError(
                    'Аккаунт активен',
                    code='account_is_active',
                )

        except utils.get_user_model().DoesNotExist:
            raise forms.ValidationError(
                'Пользователя не найдено',
            )
        except utils.get_user_model().MultipleObjectsReturned:
            raise forms.ValidationError(
                'Большое количество пользователей на один email: {}'.format(email),
            )
        return email


class PasswordResetForm(forms.Form):
    email = forms.EmailField(required=True, label='Email')

    def clean(self):
        email = self.cleaned_data['email']

        try:
            self._user = utils.get_user(email=email)

            if not self._user.is_active:
                raise forms.ValidationError(
                    'Аккаунт не активен, хотите выслать подтверждение еще раз?',
                    code='account_not_active',
                )

        except utils.get_user_model().DoesNotExist:
            raise forms.ValidationError(
                'Пользователя не найдено',
            )
        except utils.get_user_model().MultipleObjectsReturned:
            raise forms.ValidationError(
                'Большое количество пользователей на один email: {}'.format(email),
            )

    def get_user_from_email(self):
        return getattr(self, '_user', None)


class SetPasswordForm(DjangoSetPasswordForm):

    def __init__(self, *args, **kwargs):
        super(SetPasswordForm, self).__init__(*args, **kwargs)
        self.fields['new_password1'].label = 'Новый пароль'
        self.fields['new_password2'].label = 'Повторите пароль'

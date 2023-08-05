from django.conf import settings
from django.contrib.auth.tokens import \
    PasswordResetTokenGenerator as DjangoPasswordResetTokenGenerator


default_key = 'fEqUvMDIIY1Yh70GbH9u7e8Fyv716xSs'


class SetKeySaltMixin:
    def __init__(self):
        self.key_salt = getattr(settings, 'ACTIVATION_ACCOUNT_PASSWORD_RESET', default_key)


class PasswordResetTokenGenerator(SetKeySaltMixin, DjangoPasswordResetTokenGenerator):
    pass


class AccountActivationTokenGenerator(SetKeySaltMixin, DjangoPasswordResetTokenGenerator):
    pass

password_reset_token_generator = PasswordResetTokenGenerator()
account_activation_token = AccountActivationTokenGenerator()

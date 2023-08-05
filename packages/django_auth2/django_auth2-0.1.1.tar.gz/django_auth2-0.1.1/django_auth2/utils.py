from django.conf import settings
from django.shortcuts import redirect


def get_user(**kwargs):
    return get_user_model().objects.get(**kwargs)


def get_user_model():
    if hasattr(settings, 'AUTH_USER_MODEL'):
        from django.contrib.auth import get_user_model
        return get_user_model()
    else:
        from django.contrib.auth.models import User as DjangoUser
        return DjangoUser


class RedirectActiveUser(object):

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('/')

        return super(RedirectActiveUser, self).dispatch(request, *args, **kwargs)

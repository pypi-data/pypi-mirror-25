from django.contrib import auth
from django.shortcuts import redirect
from django.urls import reverse


def logout(request):
    redirect_to = reverse('login')
    if request.user.is_authenticated():
        auth.logout(request)

    return redirect(redirect_to)

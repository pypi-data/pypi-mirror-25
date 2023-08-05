from re import compile

from django.conf import settings
from django.http import HttpResponseRedirect
from django.utils.deprecation import MiddlewareMixin
from django.urls import reverse


EXCEPT_URLS = [
    compile('login(\.*)'),
    compile('register(\.*)'),
    compile('logout(\.*)'),
    compile('activate_profile(\.*)'),
    compile('password_reset(\.*)'),
]  # urls for django_auth2_urls

EXCEPT_URLS += [compile(expr.lstrip('/'))
                for expr in getattr(settings, 'DJANGO_AUTH2_LOGIN_EXCEPT_URLS', [])]


class LoginRequiredMiddleware(MiddlewareMixin):

    def process_request(self, request):
        path = request.path_info.lstrip('/')

        can_show_urls_user = request.user.is_authenticated() and request.user.is_active
        if not any([m.match(path) for m in EXCEPT_URLS]) and path and not can_show_urls_user:
            login_url = reverse('login').rstrip('/') + '/?next_url={}'.format(path)
            return HttpResponseRedirect(login_url)

        return self.get_response(request)

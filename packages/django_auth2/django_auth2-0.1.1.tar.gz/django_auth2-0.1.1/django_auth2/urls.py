# coding: utf-8
from django.conf.urls import url

from .views import activate, login, logout, register, reset_password

urlpatterns = [
    url(r'^login/$', login.login, name='login'),
    url(r'^register/$', register.register, name='register'),
    url(r'^logout/$', logout.logout, name='logout'),

    url(r'^activate_profile/(?P<uidb64>[0-9A-Za-z_\-]+)/'
        r'(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        activate.activate, name='activate'),
    url(r'^activate_profile/re_send/$', activate.re_send, name='activate_re_send'),
    url(r'^activate_profile/success/$', activate.success, name='activation_success'),

    url(r'^password_reset/$', reset_password.password_reset, name='password_reset'),
    url(r'^password_reset/done/$', reset_password.password_reset_done,
        name='password_reset_done'),
    url(r'^password_reset/(?P<uidb64>[0-9A-Za-z_\-]+)/'
        r'(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        reset_password.password_reset_confirm, name='password_reset_confirm'),
    url(r'^password_reset/complete/$', reset_password.password_reset_complete,
        name='password_reset_complete'),
]

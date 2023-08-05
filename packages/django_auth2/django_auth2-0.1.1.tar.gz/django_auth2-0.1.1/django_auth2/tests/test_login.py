from django.test import TestCase

from rest_framework.reverse import reverse_lazy

from .base import BaseWithoutLoginMixin


class LoginTest(BaseWithoutLoginMixin, TestCase):
    url = reverse_lazy('login')

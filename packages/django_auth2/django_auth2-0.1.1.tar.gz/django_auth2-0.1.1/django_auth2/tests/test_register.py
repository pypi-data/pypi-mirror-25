from django.test import TestCase
from django.urls import reverse

from django_auth2.tests.base import BaseWithoutLoginMixin


class RegisterTest(BaseWithoutLoginMixin, TestCase):
    url = reverse('register')

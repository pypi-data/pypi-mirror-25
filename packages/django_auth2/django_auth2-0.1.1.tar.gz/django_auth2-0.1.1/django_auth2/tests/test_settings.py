INSTALLED_APPS = (
    'django_auth2',
)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

SECRET_KEY = "secret_key_for_django_auth2"

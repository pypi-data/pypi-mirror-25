# Django AUTH

### install from pypi

    pip install django-auth2

### local installing

    git clone git@github.com:Nick1994209/django-auth2.git

    python setup.pu install

else if need refactore code

    pip install -e django-auth2


### in project.settings

    INSTALLED_APPS = [
        ...
        'django.contrib.auth',
        'django_auth2',
    ]

### in project.urls

    ...
    url(r'', include('django_auth2.urls')),
    ...


## Additional

### for User model (optional)

    email = models.EmailField(unique=True, blank=False)
    is_active = models.BooleanField()


#### if want send activation email for activate user

###### then set project.settings

    DJANGO_AUTH2_SEND_ACTIVATION_EMAIL = True
    # password reset days
    PASSWORD_RESET_TIMEOUT_DAYS = 1

    # for sedning email
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
    EMAIL_USE_TLS = True
    EMAIL_HOST = 'smtp.gmail.com'
    EMAIL_HOST_USER = 'my_mail@gmail.com'
    EMAIL_HOST_PASSWORD = 'my_pass'
    EMAIL_PORT = 587

in yor project.settings user.is_active = False


`you can use celery for send mails
if you virtualenv installed celery and project work with her;
  mails be sent from celery
else if installed celery but not project now work with her;
  mails message is not sent`
[first state with celery. django]: http://docs.celeryproject.org/en/latest/django/first-steps-with-django.html

if not celery then mail will be sent (default django)


###### else

user.is_active = True (by default) and mail not sent

For send mail (example):

#### can use middleware

in settings

    MIDDLEWARE = [
        ...
        'django_auth2.middleware.LoginRequiredMiddleware',
    ]

    DJANGO_AUTH2_LOGIN_EXCEPT_URLS = [
        '/info/(.*)',
        '/index/',
    ]

from django.conf import settings


def pytest_configure(config):
    if not settings.configured:
        settings.configure(
            DATABASE_ENGINE='sqlite3',
            DATABASES={
                'default': {
                    'NAME': ':memory:',
                    'ENGINE': 'django.db.backends.sqlite3',
                    'TEST_NAME': ':memory:',
                },
            },
            INSTALLED_APPS=[
                'django.contrib.auth',
                'django.contrib.admin',
                'django.contrib.sessions',
                'django.contrib.sites',
                'django.contrib.contenttypes',

                'sentry',
            ],
            SENTRY_QUOTAS={
                'redis': {
                    'hosts': {0: {}},
                },
                'default_events_per_minute': 100,
            },
            ROOT_URLCONF='',
            DEBUG=False,
            SITE_ID=1,
            SENTRY_ALLOW_ORIGIN='*',
            TEMPLATE_DEBUG=True,
        )

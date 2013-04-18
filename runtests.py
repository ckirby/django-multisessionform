import os, sys

from django.conf import settings

DIRNAME = os.path.dirname(__file__)
settings.configure(DEBUG=True,
               DATABASES={
                    'default': {
                        'ENGINE': 'django.db.backends.sqlite3',
                    }
                },
               ROOT_URLCONF='multisessionform.urls',
               INSTALLED_APPS=('django.contrib.auth',
                              'django.contrib.contenttypes',
                              'django.contrib.sessions',
                              'django.contrib.admin',
                              'multisessionform',
                              'multisessionform.tests',))

test_args = ['tests']

from django.test.simple import DjangoTestSuiteRunner
test_runner = DjangoTestSuiteRunner(verbosity=1)
failures = test_runner.run_tests(test_args)
if failures:
    sys.exit(failures)
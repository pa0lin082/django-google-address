#!/usr/bin/env python3
import glob
import os
import sys
import copy

import django
from django.conf import settings
from django.core.management import execute_from_command_line
from django.test.utils import get_runner

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(BASE_DIR, '../..')))

# Unfortunately, apps can not be installed via ``modify_settings``
# decorator, because it would miss the database setup.
CUSTOM_INSTALLED_APPS = (
    'google_address',
    'demo',
    # 'modeltranslation',
    'django.contrib.admin',
)

ALWAYS_INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
)

ALWAYS_MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

gettext = lambda s: s

settings.configure(
    SECRET_KEY="django_tests_secret_key",
    DEBUG=False,
    TEMPLATE_DEBUG=False,
    ALLOWED_HOSTS=[],
    INSTALLED_APPS=ALWAYS_INSTALLED_APPS + CUSTOM_INSTALLED_APPS,
    MIDDLEWARE_CLASSES=ALWAYS_MIDDLEWARE_CLASSES,
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3'
        }
    },
    LANGUAGES = (
      ('en-us', gettext('English')),
    ),
    LANGUAGE_CODE='en-us',
    TIME_ZONE='UTC',
    USE_I18N=True,
    USE_L10N=True,
    USE_TZ=True,
    STATIC_URL='/static/',
    # Use a fast hasher to speed up tests.
    PASSWORD_HASHERS=(
        'django.contrib.auth.hashers.MD5PasswordHasher',
    ),
    FIXTURE_DIRS=glob.glob(BASE_DIR + '/' + '*/fixtures/'),
    EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend',
    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [os.path.abspath(os.path.join(BASE_DIR, '../../templates'))],
            'APP_DIRS': True,
            'OPTIONS': {
                'context_processors': [
                    'django.template.context_processors.debug',
                    'django.template.context_processors.request',
                    'django.contrib.auth.context_processors.auth',
                    'django.contrib.messages.context_processors.messages',
                ],
            },
        },
    ],
    GOOGLE_ADDRESS = {'API_LANGUAGE': 'en_US'}
)

if __name__ == '__main__':
    django.setup()
    args = [sys.argv[0], 'test']
    # Current module (``tests``) and its submodules.
    test_cases = '.'

    # Allow accessing test options from the command line.
    offset = 1
    try:
        sys.argv[1]
    except IndexError:
        pass
    else: #pragma: no cover
        option = sys.argv[1].startswith('-')
        if not option:
            test_cases = sys.argv[1]
            offset = 2

    args.append(test_cases)
    # ``verbosity`` can be overwritten from command line.
    args.append('--verbosity=2')
    args.extend(sys.argv[offset:])

    test_labels = []
    TestRunner = get_runner(settings)
    test_runner = TestRunner(verbosity=2)
    test_runner.setup_test_environment()
    suite = test_runner.build_suite(test_labels, None)
    old_config = test_runner.setup_databases()
    test_runner.run_checks()

    print('suite:',suite)
    for a in range(10):
        copy_suite = suite = test_runner.build_suite(test_labels, None)
        result = test_runner.run_suite(copy_suite)
        print('suite:', suite)
        # print(result)



    test_runner.teardown_databases(old_config)
    test_runner.teardown_test_environment()
    test_runner.suite_result(suite, result)


    # test_runner.run_tests([])
    # test_runner.run_tests([])
    # execute_from_command_line(args)

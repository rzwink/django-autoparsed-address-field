import django
from django.conf import settings
from django.test.utils import setup_test_environment
from django.core.management import call_command

if not settings.configured:
    settings.configure(
        INSTALLED_APPS=[
            "django.contrib.contenttypes",
            "django.contrib.auth",
            "autoparsed_address_field",
        ],
        DATABASES={
            "default": {
                "ENGINE": "django.db.backends.sqlite3",
                "NAME": ":memory:",  # Use an in-memory database
            }
        },
        SECRET_KEY="test_secret_key",
    )
    django.setup()

# Set up the test environment and run migrations
setup_test_environment()
call_command("migrate")

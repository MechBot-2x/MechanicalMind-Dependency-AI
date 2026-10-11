from django.conf import settings

if not settings.configured:
    settings.configure(
        INSTALLED_APPS=[
            "mechanicalmind_ai.core",
        ],
        DATABASES={
            "default": {
                "ENGINE": "django.db.backends.sqlite3",
                "NAME": ":memory:",
            }
        },
    )

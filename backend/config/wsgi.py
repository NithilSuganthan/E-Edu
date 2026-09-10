"""
WSGI config for config project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

# Load .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

application = get_wsgi_application()

# When SQLite is active (e.g. Render demo without managed PostgreSQL),
# automatically create tables and seed courses on first boot.
try:
    from django.db import connection
    tables = connection.introspection.table_names()
    if 'core_course' not in tables:
        from django.core.management import call_command
        call_command('migrate', interactive=False)
        try:
            call_command('seed_courses')
            call_command('seed_hero_courses')
            call_command('seed_demo_accounts')
        except Exception:
            pass
    elif 'auth_user' in tables:
        from django.contrib.auth.models import User
        if not User.objects.filter(is_superuser=True).exists():
            from django.core.management import call_command
            try:
                call_command('seed_demo_accounts')
            except Exception:
                pass
except Exception as e:
    import logging
    logging.getLogger('django').error(f"Startup database initialization error: {e}", exc_info=True)



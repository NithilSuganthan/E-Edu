
import os
import django
import sys

sys.path.append(os.getcwd())

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.db import connection

print(f"Vendor: {connection.vendor}")

with connection.cursor() as cursor:
    if 'sqlite' in connection.vendor:
        cursor.execute("PRAGMA table_info(core_course);")
        # cid, name, type, notnull, dflt_value, pk
        columns = cursor.fetchall()
        for col in columns:
            # col[1] is name, col[3] is notnull (1=True, 0=False)
            is_nullable = "NO" if col[3] else "YES"
            print(f"Col: {col[1]}, Nullable: {is_nullable}")
    else:
        cursor.execute("SELECT column_name, data_type, is_nullable FROM information_schema.columns WHERE table_name = 'core_course' AND column_name LIKE 'd%' ORDER BY column_name;")
        columns = cursor.fetchall()
        for col in columns:
            print(f"Col: {col[0]}, Type: {col[1]}, Nullable: {col[2]}")

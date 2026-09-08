import os
import django
import sys

sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.db import connection

sql_statements = [
    "ALTER TABLE core_course ADD COLUMN syllabus text;",
    "ALTER TABLE core_course ADD COLUMN mode varchar(20) DEFAULT 'ONLINE' NOT NULL;",
    "ALTER TABLE core_course ADD COLUMN start_date date;",
    "ALTER TABLE core_course ADD COLUMN certification_details text;",
    "ALTER TABLE core_course ADD COLUMN notes text;",
]

with connection.cursor() as cursor:
    for sql in sql_statements:
        try:
            print(f"Executing: {sql}")
            cursor.execute(sql)
            print("Success")
        except Exception as e:
            print(f"Error executing {sql}: {e}")

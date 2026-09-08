
import os
import django
import sys

# Setup Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from core.models import Course

try:
    print("Attempting to create debug course...")
    c = Course.objects.create(
        title="Debug Course 123",
        description="Test Description",
        category="CODING",
        price=10.00
    )
    print("Success!")
except Exception as e:
    import traceback
    with open("debug_error.txt", "w") as f:
        f.write(str(e))
        f.write("\n")
        traceback.print_exc(file=f)
    print("Failed! Check debug_error.txt")

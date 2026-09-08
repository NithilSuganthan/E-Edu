import os
import django
from django.contrib.auth import authenticate

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User
from parents.models import Student

def verify_student_login():
    print("Verifying student login...")
    
    username = "teststudent"
    password = "password123"
    
    # 1. Check User exists
    try:
        user = User.objects.get(username=username)
        print(f"User '{username}' exists. ID: {user.id}")
        print(f"Is active: {user.is_active}")
        print(f"Has usable password: {user.has_usable_password()}")
    except User.DoesNotExist:
        print(f"User '{username}' DOES NOT EXIST!")
        return

    # 2. Check Authentication
    auth_user = authenticate(username=username, password=password)
    print(f"\nAUTHENTICATION RESULT: {auth_user}\n")
    if auth_user:
        print(">>> Authentication SUCCESSFUL. <<<")
    else:
        print(">>> Authentication FAILED. Password mismatch? <<<")

    # 3. Check Student Profile Link
    try:
        student = Student.objects.get(user=user)
        print(f"Student profile found for user: {student.full_name} (ID: {student.id})")
    except Student.DoesNotExist:
        print("Student profile NOT found for this user!")
        # Check if student exists but unlinked?
        try:
            s_unlinked = Student.objects.get(full_name="Junior Doe")
            print(f"Found 'Junior Doe' student (ID: {s_unlinked.id}), but verified User is: {s_unlinked.user}")
            
            # Fix it
            print("Fixing link...")
            s_unlinked.user = user
            s_unlinked.save()
            print("Link fixed.")
        except Student.DoesNotExist:
            print("No 'Junior Doe' student found at all.")

if __name__ == "__main__":
    import sys
    with open("verify_output.txt", "w") as f:
        sys.stdout = f
        verify_student_login()

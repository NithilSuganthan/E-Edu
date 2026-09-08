import os
import django
import sys
from django.utils import timezone

sys.path.append('v:\\Inventobots\\backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User
from parents.models import Student, Parent, CourseEnrollment
from certifications.models import CertificationCourse
from django.test import RequestFactory
from parents.admin import CourseEnrollmentAdmin
from django.contrib.admin.sites import AdminSite

def verify_flow():
    print("--- STARTING ENROLLMENT VERIFICATION ---")
    
    # 1. Setup
    # 1. Setup
    username = f"verify_user_{timezone.now().timestamp()}"
    try:
        user = User.objects.create_user(username=username, password="password123")
        # Signals should auto-create Parent and Student
        student = Student.objects.get(user=user)
        print(f"Refreshed Student from Signals: {student.full_name}")
    except Exception as e:
        print(f"Setup Error: {e}")
        return
    
    course = CertificationCourse.objects.first()
    if not course:
        print("FAILURE: No certification courses available.")
        return

    print(f"Created Student: {student.full_name}")
    print(f"Target Course: {course.name}")

    # 2. Simulate Enrollment (Call View Logic directly or just create object mimicking view)
    # Mimicking view logic:
    enrollment = CourseEnrollment.objects.create(
        student=student,
        course=course,
        status='Pending Payment',
        payment_status='Pending',
        enrollment_date=timezone.now().date()
    )
    
    print(f"Enrollment Created. Status: {enrollment.status}, Payment: {enrollment.payment_status}")
    if enrollment.status != 'Pending Payment':
        print("FAILURE: Initial status should be Pending Payment")
        return

    # 3. Simulate Admin Activation
    print("\n[Simulating Admin Activation]")
    admin_instance = CourseEnrollmentAdmin(CourseEnrollment, AdminSite())
    queryset = CourseEnrollment.objects.filter(id=enrollment.id)
    
    # Mock Request
    factory = RequestFactory()
    request = factory.get('/admin/')
    request.user = user # Attach the user
    # Add message storage support
    from django.contrib.messages.storage.fallback import FallbackStorage
    setattr(request, 'session', 'session')
    messages = FallbackStorage(request)
    setattr(request, '_messages', messages)
    
    # Call the action
    admin_instance.activate_enrollment(request, queryset)
    
    enrollment.refresh_from_db()
    print(f"Post-Activation Status: {enrollment.status}")
    print(f"Post-Activation Payment: {enrollment.payment_status}")
    print(f"Payment Date: {enrollment.payment_date}")
    
    if enrollment.status == 'Active' and enrollment.payment_status == 'Completed' and enrollment.payment_date:
        print("SUCCESS: Enrollment is Active and Paid.")
    else:
        print("FAILURE: Admin activation did not work as expected.")

    print("\n--- VERIFICATION COMPLETE ---")

if __name__ == "__main__":
    verify_flow()

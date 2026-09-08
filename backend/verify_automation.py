import os
import django
import sys

# Setup Django environment
sys.path.append('v:\\Inventobots\\backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User
from parents.models import Student, Parent, CourseEnrollment, StudentCertificate
from core.models import Course, Topic, TopicProgress
from certifications.models import CertificationCourse, Certificate
from django.utils import timezone
import datetime

def run_verification():
    print("--- STARTING VERIFICATION ---")

    # 1. Test User -> Student Creation
    print("\n[Test 1] User Creation -> Auto Student")
    username = f"testUser_{timezone.now().timestamp()}"
    try:
        user = User.objects.create_user(username=username, password="password123")
        print(f"Created User: {user.username}")
        
        student = Student.objects.get(user=user)
        print(f"SUCCESS: Student found: {student.full_name}, Parent: {student.parent}")
    except Student.DoesNotExist:
        print("FAILURE: Student was NOT created.")
        return

    # 2. Setup Courses for Progress Test
    print("\n[Test 2] Setup Courses")
    core_course = Course.objects.first()
    if core_course:
        print(f"Using existing Core Course: {core_course.title}")
    else:
        try:
            core_course = Course.objects.create(
                title=f"Core Course {username}", 
                description="Test Description",
                highlights=[],
                syllabus="Syllabus content",
                notes="Notes content",
                category="CODING"
            )
        except Exception as e:
            print(f"ERROR Creating Course: {e}")
            return
    
    try:
        cert_course = CertificationCourse.objects.create(
            name=f"Cert Course {username}", 
            description="Cert Description", 
            core_course=core_course,
            duration="8 Weeks",
            level="Beginner"
        )
    except Exception as e:
        print(f"ERROR Creating Cert Course: {e}")
        return
    
    topic1 = Topic.objects.create(course=core_course, title="Topic 1", order=1)
    topic2 = Topic.objects.create(course=core_course, title="Topic 2", order=2)
    
    # Enroll Student (Simulate click)
    enrollment = CourseEnrollment.objects.create(
        student=student, 
        course=cert_course, 
        enrollment_date=timezone.now().date()
    )
    print(f"Enrolled in: {cert_course.name}")

    # 3. Test Progress Automation
    print("\n[Test 3] Progress Automation")
    # Complete Topic 1
    TopicProgress.objects.create(student=student, topic=topic1, is_completed=True)
    
    enrollment.refresh_from_db()
    print(f"Progress after Topic 1 (Total 2): {enrollment.completion_percentage}%")
    
    if enrollment.completion_percentage == 50:
        print("SUCCESS: Progress updated to 50%")
    else:
        print(f"FAILURE: Expected 50%, got {enrollment.completion_percentage}%")

    # 4. Test Manual Override
    print("\n[Test 4] Manual Override")
    enrollment.is_manually_modified = True
    enrollment.completion_percentage = 80 # Manually set to 80
    enrollment.save()
    print("Set Manual Override = True, Progress = 80%")
    
    # Complete Topic 2
    TopicProgress.objects.create(student=student, topic=topic2, is_completed=True)
    
    enrollment.refresh_from_db()
    print(f"Progress after Topic 2 (Total 2): {enrollment.completion_percentage}%")
    
    if enrollment.completion_percentage == 80:
        print("SUCCESS: Progress stayed at 80% (Override respected)")
    else:
        print(f"FAILURE: Expected 80%, got {enrollment.completion_percentage}% (Override IGNORED)")
        
    # 5. Test Certificate Generation
    print("\n[Test 5] Certificate Generation")
    # Turn off override to allow completion
    enrollment.is_manually_modified = False
    enrollment.save()
    
    # Trigger update again (hacky way: just save the topic progress again or call signal logic)
    # Since topic is already saved, signal won't fire for 'create'. 
    # Let's save the topic progress again to trigger 'post_save'
    tp2 = TopicProgress.objects.get(student=student, topic=topic2)
    tp2.save() 
    
    enrollment.refresh_from_db()
    print(f"Progress after re-enabling automation: {enrollment.completion_percentage}%")
    
    if enrollment.completion_percentage == 100:
        print("SUCCESS: Progress reached 100%")
        
        # Check Certificate
        if StudentCertificate.objects.filter(student=student, certificate__course=cert_course).exists():
            print("SUCCESS: Certificate Generated!")
        else:
            print("FAILURE: No Certificate found.")
    else:
        print("FAILURE: Progress did not reach 100%")

    print("\n--- VERIFICATION COMPLETE ---")

if __name__ == "__main__":
    run_verification()

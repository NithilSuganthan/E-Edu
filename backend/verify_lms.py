
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User
from core.models import Course, Subject, Module, Lesson
from parents.models import Student, Parent, CourseEnrollment, LessonProgress
from certifications.models import Certificate
from django.utils import timezone
import datetime

def verify_lms():
    print("--- Verifying LMS Structure and Workflow ---")

    # 1. Create Data Structure
    print("\n1. Creating Course Hierarchy...")
    
    # 1. Create Data Structure
    print("\n1. Creating Course Hierarchy...")
    
    # print("Existing Courses:")
    # for c in Course.objects.all():
    #     print(f" - {c.title} (ID: {c.id}, Mode: {getattr(c, 'mode', 'N/A')})")

    course, created = Course.objects.get_or_create(title="New Robotics Course 2026", defaults={
        "description": "A comprehensive robotics course.",
        "price": 199.99,
        "mode": "ONLINE",
        "duration": 12,
        "syllabus": "Test Syllabus",
        "certification_details": "Test Cert",
        "notes": "Test Notes",
        "display_order": 1,
        "badge": "New",
        "subtitle": "Subtitle",
        "tagline": "Tagline",
        "color_gradient": "from-blue-500 to-cyan-400",
        "is_hero_featured": False,
        "cta_primary_url": "/courses/",
        "cta_primary_text": "Explore",
        "start_date": timezone.now().date(),
        "image_url": "https://example.com/image.jpg"
    })
    print(f"   Course ID: {course.id}, Created: {created}")

    try:
        subject, created = Subject.objects.get_or_create(course=course, title="Electronics Basics", defaults={"order": 1})
        print(f"   Subject ID: {subject.id}, Created: {created}")
    except Exception as e:
        print(f"   ERROR Creating Subject: {e}")
        return
    
    try:
        module, created = Module.objects.get_or_create(subject=subject, title="Circuit Components", defaults={"order": 1})
        print(f"   Module ID: {module.id}, Created: {created}")
    except Exception as e:
        print(f"   ERROR Creating Module: {e}")
        return
    
    lesson_video, _ = Lesson.objects.get_or_create(
        module=module, 
        title="Understanding Resistors", 
        defaults={
            "lesson_type": "VIDEO",
            "video_url": "https://youtube.com/example",
            "order": 1,
            "duration_minutes": 10
        }
    )
    
    lesson_quiz, _ = Lesson.objects.get_or_create(
        module=module,
        title="Resistors Quiz",
        defaults={
             "lesson_type": "QUIZ",
             "order": 2
        }
    )

    print(f"   Created Course: {course}")
    print(f"   Created Subject: {subject}")
    print(f"   Created Module: {module}")
    print(f"   Created Lessons: {lesson_video}, {lesson_quiz}")

    # 2. Student Enrollment
    print("\n2. Enrolling Student...")
    # Ensure user exists
    user, _ = User.objects.get_or_create(username="test_student_lms", defaults={"email": "test@example.com"})
    parent_user, _ = User.objects.get_or_create(username="test_parent_lms", defaults={"email": "parent@example.com"})
    
    parent, _ = Parent.objects.get_or_create(user=parent_user)
    student, _ = Student.objects.get_or_create(
        user=user, 
        defaults={
            "parent": parent,
            "full_name": "Test Student LMS",
            "date_of_birth": "2015-01-01",
            "enrollment_date": timezone.now().date()
        }
    )
    
    enrollment, created = CourseEnrollment.objects.get_or_create(
        student=student, 
        course=course,
        defaults={
            "status": "Active",
            "enrollment_date": timezone.now().date()
        }
    )
    print(f"   Student '{student}' enrolled in '{course}'? {created or 'Already Enrolled'}")

    # 3. Progress Tracking
    print("\n3. Tracking Progress...")
    # Mark video as completed
    progress, _ = LessonProgress.objects.get_or_create(
        student=student,
        lesson=lesson_video,
        defaults={
            "status": "COMPLETED",
            "watched_percentage": 100,
            "completed_at": timezone.now()
        }
    )
    print(f"   Lesson '{lesson_video}' status: {progress.status}")

    # 4. Certificate Generation (Simulated)
    print("\n4. Simulating Certificate Generation...")
    # Assume course is completed
    cert = Certificate.objects.create(
        student_name=student.full_name,
        course=course,
        issue_date=timezone.now().date(),
        status="Valid"
    )
    print(f"   Certificate Generated: {cert.certificate_id} for {cert.student_name}")
    
    print("\n--- Verification Complete ---")

if __name__ == "__main__":
    try:
        verify_lms()
    except Exception as e:
        print(f"\nERROR: {e}")

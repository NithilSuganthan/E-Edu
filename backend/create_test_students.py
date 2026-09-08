import os
import django
from datetime import date, timedelta

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User
from parents.models import Parent, Student, CourseEnrollment
from certifications.models import CertificationCourse

def create_test_data():
    print("Creating test data...")

    # 1. Create Parent User
    parent_username = "testparent"
    parent_email = "parent@example.com"
    parent_password = "password123"
    
    parent_user, created = User.objects.get_or_create(username=parent_username, email=parent_email)
    if created:
        parent_user.set_password(parent_password)
        parent_user.first_name = "John"
        parent_user.last_name = "Doe"
        parent_user.save()
        print(f"Created Parent User: {parent_username}")
    else:
        print(f"Parent User {parent_username} already exists.")

    # 2. Create Parent Profile
    parent_profile, created = Parent.objects.get_or_create(user=parent_user)
    if created:
        parent_profile.phone_number = "1234567890"
        parent_profile.save()
        print("Created Parent Profile.")

    # 3. Create Student User
    student_username = "teststudent"
    student_password = "password123"
    
    student_user, created = User.objects.get_or_create(username=student_username)
    # Always set password to ensure it matches what we tell the user
    student_user.set_password(student_password)
    student_user.first_name = "Junior"
    student_user.last_name = "Doe"
    student_user.save()
    
    if created:
        print(f"Created Student User: {student_username}")
    else:
        print(f"Student User {student_username} updated with new password.")

    # 4. Create Student Profile
    student_profile, created = Student.objects.get_or_create(
        parent=parent_profile,
        full_name="Junior Doe",
        defaults={
            'date_of_birth': date(2015, 1, 1),
            'grade_level': "Grade 5",
            'enrollment_date': date.today(),
            'user': student_user,
            'level': 15,
            'xp': 4200
        }
    )
    if created:
        print("Created Student Profile.")
    else:
        print("Student Profile already exists.")

    # 5. Create Sample Courses and Enrollments
    courses_data = [
        {"name": "Python for Kids", "level": "Module 3"},
        {"name": "Robotics Basics", "level": "Module 1"}
    ]

    for c_data in courses_data:
        course, _ = CertificationCourse.objects.get_or_create(
            name=c_data["name"],
            defaults={
                'description': "Sample course",
                'duration': "10 Weeks",
                'level': "Beginner",
                'price': 0
            }
        )
        
        enrollment, created = CourseEnrollment.objects.get_or_create(
            student=student_profile,
            course=course,
            defaults={
                'enrollment_date': date.today(),
                'status': 'Active',
                'completion_percentage': 45 if "Python" in c_data["name"] else 15,
                'current_level': c_data["level"]
            }
        )
        if created:
            print(f"Enrolled student in {c_data['name']}")

    print("\n--- TEST DATA READY ---")
    print(f"Student Login: {student_username} / {student_password}")
    print(f"Parent Login: {parent_username} / {parent_password}")

if __name__ == "__main__":
    create_test_data()

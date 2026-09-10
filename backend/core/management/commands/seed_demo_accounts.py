from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import date, timedelta
from parents.models import (
    Parent, Student, CourseEnrollment, Attendance,
    ProgressTracker, TrainerFeedback, StudentCertificate, Alert
)
from core.models import Course, Topic, Quiz, QuizSubmission, Badge, StudentBadge


class Command(BaseCommand):
    help = 'Seeds standard demo accounts (Admin, Parent, Student) with complete profiles and enrollments'

    def handle(self, *args, **kwargs):
        self.stdout.write("Seeding demo accounts...")

        # 1. Superuser / Admin
        admin_username = "admin"
        admin_email = "admin@inventobots.com"
        admin_password = "AdminPassword123!"

        admin_user, admin_created = User.objects.get_or_create(username=admin_username)
        admin_user.email = admin_email
        admin_user.set_password(admin_password)
        admin_user.is_staff = True
        admin_user.is_superuser = True
        admin_user.first_name = "Admin"
        admin_user.last_name = "Master"
        admin_user.save()
        status_str = "Created" if admin_created else "Updated"
        self.stdout.write(self.style.SUCCESS(f"[{status_str}] Superuser: {admin_username} (password: {admin_password})"))

        # 2. Parent Account
        parent_username = "testparent"
        parent_email = "parent@example.com"
        parent_password = "password123"

        parent_user, parent_user_created = User.objects.get_or_create(username=parent_username)
        parent_user.email = parent_email
        parent_user.set_password(parent_password)
        parent_user.first_name = "Sarah"
        parent_user.last_name = "Doe"
        parent_user.save()

        parent_profile, _ = Parent.objects.get_or_create(user=parent_user)
        parent_profile.phone_number = "+91 98765 43210"
        parent_profile.address = "42 Silicon Avenue, Chennai, India"
        parent_profile.emergency_contact = "+91 98765 43211"
        parent_profile.save()
        self.stdout.write(self.style.SUCCESS(f"[OK] Parent Account: {parent_username} (password: {parent_password})"))

        # 3. Student Account
        student_username = "teststudent"
        student_email = "student@example.com"
        student_password = "password123"

        student_user, student_user_created = User.objects.get_or_create(username=student_username)
        student_user.email = student_email
        student_user.set_password(student_password)
        student_user.first_name = "Alex"
        student_user.last_name = "Doe"
        student_user.save()

        student_profile, student_created = Student.objects.get_or_create(
            user=student_user,
            defaults={
                'parent': parent_profile,
                'full_name': "Alex Doe",
                'grade_level': "Grade 6",
                'date_of_birth': date(2013, 5, 15),
                'enrollment_date': date(2024, 1, 10),
                'level': 5,
                'xp': 1450,
                'is_active': True,
            }
        )
        student_profile.parent = parent_profile
        student_profile.full_name = "Alex Doe"
        student_profile.grade_level = "Grade 6"
        student_profile.level = 5
        student_profile.xp = 1450
        student_profile.save()
        self.stdout.write(self.style.SUCCESS(f"[OK] Student Account: {student_username} (password: {student_password})"))

        # 4. Enrollments & Course Data
        courses = list(Course.objects.all()[:3])
        if not courses:
            c1 = Course.objects.create(
                title="Python for Beginners",
                description="Master fundamentals of Python.",
                category="CODING",
                price=49.99,
                badge="Popular"
            )
            c2 = Course.objects.create(
                title="Robotics 101",
                description="Hands-on robotics and circuits.",
                category="ROBOTICS",
                price=79.99,
                badge="Hands-on"
            )
            courses = [c1, c2]

        active_course = courses[0]
        enrollment_active, _ = CourseEnrollment.objects.get_or_create(
            student=student_profile,
            course=active_course,
            defaults={
                'enrollment_date': date(2024, 1, 15),
                'status': 'Active',
                'mode': 'Online',
                'completion_percentage': 68,
                'current_level': 'Module 3: Functions & Logic',
                'payment_status': 'Completed',
                'payment_reference': 'PAY-INV-2024-001',
                'payment_date': timezone.now() - timedelta(days=60)
            }
        )
        enrollment_active.status = 'Active'
        enrollment_active.completion_percentage = 68
        enrollment_active.current_level = 'Module 3: Functions & Logic'
        enrollment_active.payment_status = 'Completed'
        enrollment_active.save()

        if len(courses) > 1:
            second_course = courses[1]
            enrollment_2, _ = CourseEnrollment.objects.get_or_create(
                student=student_profile,
                course=second_course,
                defaults={
                    'enrollment_date': date.today() - timedelta(days=14),
                    'status': 'Active',
                    'mode': 'Offline',
                    'completion_percentage': 30,
                    'current_level': 'Module 1: Circuit Basics',
                    'payment_status': 'Completed',
                    'payment_reference': 'PAY-INV-2024-002',
                    'payment_date': timezone.now() - timedelta(days=14)
                }
            )

        # 5. Attendance & Alerts
        for i in range(1, 8):
            att_date = date.today() - timedelta(days=i * 2)
            Attendance.objects.get_or_create(
                student=student_profile,
                date=att_date,
                defaults={
                    'course': active_course,
                    'status': 'Present' if i != 3 else 'Late',
                    'notes': 'Active participation' if i != 3 else 'Joined 5 mins late'
                }
            )

        Alert.objects.get_or_create(
            student=student_profile,
            alert_type='Achievement',
            defaults={
                'message': "Alex's progress report for Python Module 3 is now available for review.",
                'severity': 'Info',
                'is_read': False
            }
        )
        Alert.objects.get_or_create(
            student=student_profile,
            alert_type='General',
            defaults={
                'message': "Upcoming hands-on robotics session scheduled for Saturday 10:00 AM.",
                'severity': 'Info',
                'is_read': False
            }
        )

        self.stdout.write(self.style.SUCCESS("All demo accounts and dashboard data seeded successfully!"))

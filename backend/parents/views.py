from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Avg, Q
from django.utils import timezone
from datetime import timedelta
import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest, HttpResponse
from .models import (
    Parent, Student, CourseEnrollment, Attendance,
    ProgressTracker, TrainerFeedback, StudentCertificate, Report, Alert,
    LessonProgress
)
from core.models import Topic, TopicProgress, Quiz, QuizSubmission, Badge, StudentBadge


def parent_login_view(request):
    """Handle parent login"""
    if request.user.is_authenticated and hasattr(request.user, 'parent_profile'):
        return redirect('parents:dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            # Check if user has a parent profile
            if hasattr(user, 'parent_profile'):
                login(request, user)
                return redirect('parents:dashboard')
            else:
                messages.error(request, 'This account is not registered as a parent account.')
        else:
            messages.error(request, 'Invalid email or password.')
    
    return render(request, 'parents/login.html')


def student_login_view(request):
    """Handle student login"""
    if request.user.is_authenticated and hasattr(request.user, 'student_profile'):
        return redirect('parents:student_dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            # Check if user has a student profile
            if hasattr(user, 'student_profile'):
                login(request, user)
                return redirect('parents:student_dashboard')
            else:
                # Valid credentials, but this account is not a student
                # (e.g. a parent or admin account).
                messages.error(request, 'This account is not registered as a student account.')
        else:
            # Generic message: do not reveal whether the username exists.
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'parents/student_login.html')


@login_required
def parent_dashboard_view(request):
    """Display personalized parent dashboard"""
    # Ensure user is a parent
    if not hasattr(request.user, 'parent_profile'):
        messages.error(request, 'Access denied. Parent account required.')
        return redirect('parents:login')
    
    parent = request.user.parent_profile
    students = parent.students.filter(is_active=True)
    
    # Prepare dashboard data for each student
    student_data = []
    total_alerts = 0
    
    for student in students:
        # Get active enrollments
        enrollments = student.enrollments.filter(status='Active')
        
        # Calculate attendance percentage
        total_attendance = student.attendance_records.count()
        present_count = student.attendance_records.filter(
            Q(status='Present') | Q(status='Late')
        ).count()
        attendance_percentage = (present_count / total_attendance * 100) if total_attendance > 0 else 0
        
        # Get recent feedback
        recent_feedback = student.feedback_records.order_by('-feedback_date')[:3]
        
        # Get certificates
        certificates = student.certificates.filter(status='Issued')
        
        # Get unread alerts
        unread_alerts = student.alerts.filter(is_read=False)
        total_alerts += unread_alerts.count()
        
        # Get recent progress
        recent_progress = student.progress_records.order_by('-last_updated')[:5]
        
        # Get latest report
        latest_report = student.reports.order_by('-generated_date').first()
        
        student_data.append({
            'student': student,
            'enrollments': enrollments,
            'attendance_percentage': round(attendance_percentage, 1),
            'total_classes': total_attendance,
            'days_present': present_count,
            'days_absent': total_attendance - present_count,
            'recent_feedback': recent_feedback,
            'certificates_count': certificates.count(),
            'unread_alerts': unread_alerts,
            'recent_progress': recent_progress,
            'latest_report': latest_report,
        })
    
    # Get all alerts for the parent's students
    all_alerts = Alert.objects.filter(
        student__in=students
    ).order_by('-created_at')[:10]
    
    context = {
        'parent': parent,
        'student_data': student_data,
        'total_students': students.count(),
        'total_alerts': total_alerts,
        'all_alerts': all_alerts,
    }
    
    return render(request, 'parents/dashboard.html', context)


@login_required
def student_detail_view(request, student_id):
    """Display detailed information for a specific student"""
    if not hasattr(request.user, 'parent_profile'):
        messages.error(request, 'Access denied.')
        return redirect('parents:login')
    
    parent = request.user.parent_profile
    student = get_object_or_404(Student, id=student_id, parent=parent)
    
    # Get all data for this student
    enrollments = student.enrollments.all()
    attendance_records = student.attendance_records.order_by('-date')[:20]
    progress_records = student.progress_records.order_by('-last_updated')
    feedback_records = student.feedback_records.order_by('-feedback_date')
    certificates = student.certificates.all()
    reports = student.reports.order_by('-generated_date')
    alerts = student.alerts.order_by('-created_at')
    
    context = {
        'student': student,
        'enrollments': enrollments,
        'attendance_records': attendance_records,
        'progress_records': progress_records,
        'feedback_records': feedback_records,
        'certificates': certificates,
        'reports': reports,
        'alerts': alerts,
    }
    
    return render(request, 'parents/student_detail.html', context)


@login_required
def mark_alert_read(request, alert_id):
    """Mark an alert as read"""
    if not hasattr(request.user, 'parent_profile'):
        return redirect('parents:login')
    
    parent = request.user.parent_profile
    alert = get_object_or_404(Alert, id=alert_id, student__parent=parent)
    alert.is_read = True
    alert.save()
    
    messages.success(request, 'Alert marked as read.')
    return redirect('parents:dashboard')


@login_required
def download_report(request, report_id):
    """Allow parent to download a report"""
    if not hasattr(request.user, 'parent_profile'):
        return redirect('parents:login')
    
    parent = request.user.parent_profile
    report = get_object_or_404(Report, id=report_id, student__parent=parent)
    
    # In a production environment, you would serve the file securely
    # For now, we'll redirect to the file URL
    if report.report_file:
        return redirect(report.report_file.url)
    else:
        messages.error(request, 'Report file not found.')
        return redirect('parents:dashboard')


def parent_logout_view(request):
    """Handle parent logout"""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('parents:login')


def student_logout_view(request):
    """Handle student logout"""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('parents:student_login')

@login_required(login_url='/parents/student/login/')
def student_dashboard_view(request):
    """Display personalized student dashboard"""
    # Ensure user is a student
    if not hasattr(request.user, 'student_profile'):
        messages.error(request, 'Access denied. Student account required.')
        # Redirect to parent login or home if not a student
        return redirect('home') 

    student = request.user.student_profile
    
    # 1. Overview & Streak
    # Calculate streak based on TopicProgress last_accessed or Attendance
    # Simple logic: check distinct dates in last 7 days from TopicProgress
    recent_activity = TopicProgress.objects.filter(
        student=student, 
        last_accessed__gte=timezone.now() - timedelta(days=7)
    ).dates('last_accessed', 'day')
    streak_count = recent_activity.count() # This is a simple approximation
    
    # 2. Progress Tracker & Enrollment List
    # Fetch ALL enrollments to show pending ones too
    enrollments = student.enrollments.all().order_by('-last_activity_date')
    courses_progress = []
    
    for enrollment in enrollments:
        course = enrollment.course
        
        # CourseEnrollment now links directly to core.Course
        core_course = course
        
        progress_percent = 0
        if enrollment.status == 'Active':
            if core_course:
                # Fallback to TopicProgress for now, or update to LessonProgress
                # Check if we should use LessonProgress (new system)
                total_lessons = 0
                completed_lessons = 0
                
                # Check for new hierarchy
                if course.subjects.exists():
                     # Calculate using LessonProgress
                     
                     # Get total lessons count efficiently
                     for subject in course.subjects.all():
                         for module in subject.modules.all():
                             total_lessons += module.lessons.count()
                     
                     if total_lessons > 0:
                         completed_lessons = LessonProgress.objects.filter(
                             student=student,
                             lesson__module__subject__course=course,
                             status='COMPLETED'
                         ).count()
                         progress_percent = int((completed_lessons / total_lessons) * 100)
                else:
                    # Fallback to TopicProgress (Old system)
                    total_topics = core_course.topics.count()
                    completed_topics = TopicProgress.objects.filter(
                        student=student, 
                        topic__course=core_course, 
                        is_completed=True
                    ).count()
                    if total_topics > 0:
                        progress_percent = int((completed_topics / total_topics) * 100)
            else:
                progress_percent = enrollment.completion_percentage
        
        courses_progress.append({
            'name': course.title,
            'status': enrollment.status,
            'payment_status': enrollment.payment_status,
            'percent': progress_percent,
            'enrollment': enrollment,
            'core_course': core_course,
            'whatsapp_link': None, # Whatsapp link not currently on Course model
            'image_url': course.image.url if course.image else None,
            'price': course.price
        })

    # 3. Personalized Recommendations
    recommendations = []
    # logic: Low quiz scores (< 50%)
    low_scores = QuizSubmission.objects.filter(student=student, score__lt=50).order_by('-submitted_at')[:3]
    for sub in low_scores:
        if sub.quiz.topic:
            recommendations.append({
                'type': 'Review',
                'text': f"Revise {sub.quiz.topic.title}",
                'link': '#', # To be implemented (topic detail)
                'reason': f"Low score in {sub.quiz.title}"
            })
    
    # logic: Next topic in active course
    if not recommendations and courses_progress:
        # Find first incomplete topic
        cp = courses_progress[0]
        if cp['core_course']:
            next_topic = Topic.objects.filter(
                course=cp['core_course']
            ).exclude(
                topicprogress__student=student, 
                topicprogress__is_completed=True
            ).first()
            if next_topic:
                 recommendations.append({
                    'type': 'Next Step',
                    'text': f"Start {next_topic.title}",
                    'link': '#',
                    'reason': "Continue your progress"
                })

    # 4. Assessments (Chart Data)
    recent_quizzes = QuizSubmission.objects.filter(student=student).order_by('submitted_at')[:10]
    quiz_labels = [q.quiz.title for q in recent_quizzes]
    quiz_scores = [q.score for q in recent_quizzes]
    
    # 5. Certificates & Badges
    badges = student.badges_earned.all()
    certificates = student.certificates.all()

    # Real Data from Model
    # level = student.level
    # xp = student.xp
    active_courses_count = enrollments.count()

    context = {
        'student': student,
        'streak_count': streak_count,
        'courses_progress': courses_progress,
        'recommendations': recommendations,
        'quiz_labels': quiz_labels,
        'quiz_scores': quiz_scores,
        'badges': badges,
        'certificates': certificates,
        'level': student.level,
        'xp': student.xp,
        'active_courses_count': active_courses_count,
    }
    return render(request, 'student_dashboard.html', context)


@login_required(login_url='/parents/student/login/')
def student_courses_view(request):
    if not hasattr(request.user, 'student_profile'):
        messages.error(request, 'Access denied.')
        return redirect('parents:login')
    
    student = request.user.student_profile
    enrollments = CourseEnrollment.objects.filter(student=student)
    
    # Statistics
    total_enrolled = enrollments.count()
    completed_courses = enrollments.filter(status='Completed').count()
    certificates_count = student.certificates.count()
    
    context = {
        'student': student,
        'enrollments': enrollments,
        'total_enrolled': total_enrolled,
        'completed_courses': completed_courses,
        'certificates_count': certificates_count,
    }
    return render(request, 'student_courses.html', context)


@login_required(login_url='/parents/student/login/')
def student_settings_view(request):
    if not hasattr(request.user, 'student_profile'):
        messages.error(request, 'Access denied.')
        return redirect('parents:login')
    
    student = request.user.student_profile
    
    if request.method == 'POST':
        student.full_name = request.POST.get('full_name', student.full_name)
        student.grade_level = request.POST.get('grade_level', student.grade_level)
        
        # Handle Date of Birth if provided
        dob = request.POST.get('date_of_birth')
        if dob:
            student.date_of_birth = dob

        # Handle Username Change
        new_username = request.POST.get('username')
        if new_username and new_username != request.user.username:
            from django.contrib.auth.models import User
            if User.objects.filter(username=new_username).exists():
                messages.error(request, 'Username already taken. Please choose another.')
                return redirect('parents:student_settings')
            else:
                request.user.username = new_username
                request.user.save()
            
        # Handle Profile Image (validate content: only real images are accepted)
        if 'profile_image' in request.FILES:
            uploaded = request.FILES['profile_image']
            from django.core.files.images import get_image_dimensions
            max_bytes = 5 * 1024 * 1024  # 5 MB
            if uploaded.size > max_bytes:
                messages.error(request, 'Profile image is too large (max 5 MB).')
                return redirect('parents:student_settings')
            try:
                uploaded.seek(0)
                dims = get_image_dimensions(uploaded)
                uploaded.seek(0)
            except Exception:
                dims = None
            if not dims or not dims[0]:
                messages.error(request, 'Please upload a valid image file (JPG/PNG).')
                return redirect('parents:student_settings')
            student.profile_image = uploaded
            
        student.save()
        messages.success(request, 'Profile updated successfully!')
        return redirect('parents:student_settings')
    
    context = {
        'student': student,
    }
    return render(request, 'student_settings.html', context)

from django.contrib.auth import update_session_auth_hash

@login_required(login_url='/parents/student/login/')
def student_change_password(request):
    if not hasattr(request.user, 'student_profile'):
        messages.error(request, 'Access denied.')
        return redirect('parents:login')
        
    if request.method == 'POST':
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        
        # Validation
        if not request.user.check_password(current_password):
            messages.error(request, 'Incorrect current password.')
        elif new_password != confirm_password:
            messages.error(request, 'New passwords do not match.')
        elif len(new_password) < 6:
             messages.error(request, 'Password must be at least 6 characters long.')
        else:
            # Success
            request.user.set_password(new_password)
            request.user.save()
            update_session_auth_hash(request, request.user) # Keep user logged in
            messages.success(request, 'Password changed successfully!')
            
    return redirect('parents:student_settings')


@login_required(login_url='/parents/student/login/')
def student_lab_view(request):
    if not hasattr(request.user, 'student_profile'):
        messages.error(request, 'Access denied. Please log in as a student to access the Coding Lab.')
        return redirect('parents:student_login')
    
    student = request.user.student_profile
    
    # Lab is unlocked for all authenticated students in the student portal
    unlocked_features = {'code': True, 'circuit': True, 'abacus': True, 'memory': True}

    context = {
        'student': student,
        'unlocked_features': unlocked_features,
        'is_locked': False,  # Unlocked upon logging into student portal
    }
    return render(request, 'student_lab.html', context)


@login_required(login_url='/parents/student/login/')
def student_certificates_view(request):
    """Display dedicated page for student certificates"""
    if not hasattr(request.user, 'student_profile'):
        messages.error(request, 'Access denied.')
        return redirect('parents:login')
    
    student = request.user.student_profile
    certificates = student.certificates.all()
    
    context = {
        'student': student,
        'certificates': certificates,
    }
    return render(request, 'student_certificates.html', context)



# @login_required  <-- Removed to handle custom redirect
def enroll_student(request, course_id):
    """
    Allow students to enroll in a course directly.
    Production Flow:
    1. Create Enrollment (Pending Payment)
    2. Redirect to Dashboard (where they see 'Pay Now')
    """
    # Custom Authentication Check
    if not request.user.is_authenticated:
        messages.info(request, "Please log in as a student to enroll.")
        return redirect(f'/parents/student/login/?next=/parents/student/enroll-now/{course_id}/')

    if not hasattr(request.user, 'student_profile'):
        messages.error(request, 'You are logged in as a Parent/Admin. Please log in as a Student to enroll.')
        return redirect('parents:student_login')
    
    student = request.user.student_profile
    from certifications.models import CertificationCourse
    cert_course = get_object_or_404(CertificationCourse, id=course_id)
    
    if not cert_course.core_course:
        messages.error(request, "Error: This certification course is not linked to any course content.")
        return redirect('parents:student_dashboard')
    
    # Check if already enrolled
    enrollment, created = CourseEnrollment.objects.get_or_create(
        student=student,
        course=cert_course.core_course,
        defaults={
            'status': 'Pending Payment',
            'payment_status': 'Pending',
            'enrollment_date': timezone.now().date()
        }
    )
    
    if created:
        messages.success(request, f'Enrollment initiated for {cert_course.name}. Redirecting to payment...')
        return redirect('parents:enroll_student_core_payment', course_id=cert_course.core_course.id)
    else:
        if enrollment.status == 'Pending Payment':
            messages.info(request, f'You have a pending enrollment for {cert_course.name}. Redirecting to payment...')
            return redirect('parents:enroll_student_core_payment', course_id=cert_course.core_course.id)
        elif enrollment.status == 'Active':
            messages.info(request, f'You are already actively enrolled in {cert_course.name}.')
        
    return redirect('parents:student_dashboard')


def parent_register_view(request):
    """Handle new parent registration"""
    if request.user.is_authenticated:
        return redirect('parents:dashboard')

    if request.method == 'POST':
        # 1. Account Details
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        
        # 2. Parent Details
        full_name = request.POST.get('full_name') # Used for Parent Name
        parent_phone = request.POST.get('parent_phone')
        address = request.POST.get('address')
        emergency_contact = request.POST.get('emergency_contact')

        # Validation
        from django.contrib.auth.models import User
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken.')
            return redirect('parents:register')
        
        try:
            # Create User
            user = User.objects.create_user(username=username, email=email, password=password)
            user.first_name = full_name # Store parent name in built-in field or profile
            user.save()
            
            # Create Parent Profile
            parent = Parent.objects.create(
                user=user,
                phone_number=parent_phone,
                address=address,
                emergency_contact=emergency_contact
            )
            
            # Login immediately
            login(request, user)
            
            messages.success(request, 'Registration successful! Welcome to Inventobots. Please add your student details.')
            return redirect('parents:dashboard')
                
        except Exception as e:
            messages.error(request, f'Registration error: {str(e)}')
            return redirect('parents:register')

    return render(request, 'parents/parent_register.html')


def student_register_view(request):
    """Handle new student self-registration"""
    if request.user.is_authenticated and hasattr(request.user, 'student_profile'):
        return redirect('parents:student_dashboard')

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        email = request.POST.get('email', '').strip()
        full_name = request.POST.get('full_name', '').strip()
        grade_level = request.POST.get('grade_level', 'Grade 5').strip()
        date_of_birth = request.POST.get('date_of_birth')
        parent_phone = request.POST.get('parent_phone', '').strip()
        emergency_contact = request.POST.get('emergency_contact', '').strip()
        address = request.POST.get('address', '').strip()

        from django.contrib.auth.models import User
        if User.objects.filter(username=username).exists():
            messages.error(request, f'Username "{username}" is already taken. Please choose another.')
            return render(request, 'parents/student_register.html')

        try:
            # 1. Create Student User
            student_user = User.objects.create_user(username=username, email=email, password=password)
            student_user.first_name = full_name
            student_user.save()

            # 2. Ensure linked Parent Profile
            parent_username = f"parent_{username}"
            if User.objects.filter(username=parent_username).exists():
                parent_user = User.objects.get(username=parent_username)
            else:
                parent_user = User.objects.create_user(
                    username=parent_username,
                    email=email,
                    password=password
                )
                parent_user.first_name = f"{full_name}'s Guardian"
                parent_user.save()

            parent_profile, _ = Parent.objects.get_or_create(
                user=parent_user,
                defaults={
                    'phone_number': parent_phone,
                    'address': address,
                    'emergency_contact': emergency_contact
                }
            )

            # 3. Create Student Profile
            from datetime import date
            dob = date.fromisoformat(date_of_birth) if date_of_birth else timezone.now().date()
            student = Student.objects.create(
                user=student_user,
                parent=parent_profile,
                full_name=full_name,
                grade_level=grade_level or 'Grade 5',
                date_of_birth=dob,
                enrollment_date=timezone.now().date(),
                level=1,
                xp=100
            )

            # 4. Log in immediately
            login(request, student_user)
            messages.success(request, f'Welcome to Inventobots Academy, {full_name}! Your student account is active.')
            return redirect('parents:student_dashboard')

        except Exception as e:
            messages.error(request, f'Registration error: {str(e)}')
            return render(request, 'parents/student_register.html')

    return render(request, 'parents/student_register.html')



@login_required
def add_student_view(request):
    """Allow logged-in parent to add a student sub-account"""
    if not hasattr(request.user, 'parent_profile'):
        messages.error(request, 'Access denied. Parent account required.')
        return redirect('parents:dashboard')
    
    parent = request.user.parent_profile
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        full_name = request.POST.get('full_name')
        grade_level = request.POST.get('grade_level')
        dob = request.POST.get('date_of_birth')
        
        from django.contrib.auth.models import User
        if User.objects.filter(username=username).exists():
            messages.error(request, f'Username "{username}" is already taken.')
            return redirect('parents:dashboard')
        
        try:
            # Create Student User
            student_user = User.objects.create_user(username=username, password=password)
            # Tag as student directly? No field for that, but checks rely on student_profile existence.
            
            # Create Student Profile linked to this Parent
            student = Student.objects.create(
                user=student_user,
                parent=parent,
                full_name=full_name,
                grade_level=grade_level,
                date_of_birth=dob,
                enrollment_date=timezone.now().date()
            )
            
            messages.success(request, f'Student "{full_name}" added successfully! They can now login with username "{username}".')
            return redirect('parents:dashboard')
            
        except Exception as e:
            messages.error(request, f'Error adding student: {str(e)}')
            return redirect('parents:dashboard')
    
    return redirect('parents:dashboard') # GET not supported, use modal in dashboard


@login_required(login_url='/parents/student/login/')
def student_browse_courses_view(request):
    if not hasattr(request.user, 'student_profile'):
        messages.error(request, 'Access denied.')
        return redirect('parents:login')
    
    student = request.user.student_profile
    from core.models import Course
    courses = Course.objects.all().order_by('-created_at')
    
    # Get list of enrolled course IDs to show "Already Enrolled"
    enrolled_course_ids = CourseEnrollment.objects.filter(student=student).values_list('course_id', flat=True)
    
    context = {
        'student': student,
        'courses': courses,
        'enrolled_course_ids': enrolled_course_ids,
    }
    return render(request, 'student_browse_courses.html', context)


@login_required(login_url='/parents/student/login/') # Login required for direct enrollment
def enroll_student_core(request, course_id):
    """
    Step 1: Show Enrollment Preference (Online/Offline)
    """
    if not hasattr(request.user, 'student_profile'):
        messages.error(request, 'Access denied. Student account required.')
        return redirect('parents:student_login')
        
    student = request.user.student_profile
    from core.models import Course
    course = get_object_or_404(Course, id=course_id)

    # Check if already enrolled
    if CourseEnrollment.objects.filter(student=student, course=course).exists():
        messages.info(request, f'You are already enrolled in {course.title}.')
        return redirect('parents:student_dashboard')
    
    context = {
        'student': student,
        'course': course
    }
    return render(request, 'student_enrollment_preference.html', context)


@login_required(login_url='/parents/student/login/')
def enroll_student_core_confirm(request, course_id):
    """
    Step 2: Process Enrollment with Preference
    """
    if request.method != 'POST':
        return redirect('parents:enroll_student_core', course_id=course_id)

    if not hasattr(request.user, 'student_profile'):
        messages.error(request, 'Access denied.')
        return redirect('parents:student_login')
        
    student = request.user.student_profile
    from core.models import Course
    course = get_object_or_404(Course, id=course_id)
    
    mode = request.POST.get('mode', 'Online') # Default to Online

    # Create/Get Enrollment
    enrollment, created = CourseEnrollment.objects.get_or_create(
        student=student,
        course=course,
        defaults={
            'status': 'Pending Payment',
            'payment_status': 'Pending',
            'enrollment_date': timezone.now().date(),
            'mode': mode
        }
    )
    
    if created:
        messages.success(request, f'Enrollment initiated for {course.title} ({mode}). Redirecting to payment...')
    else:
        # Update mode if it was pending
        if enrollment.status == 'Pending Payment':
            enrollment.mode = mode
            enrollment.save()
            
    if enrollment.status == 'Pending Payment':
        return redirect('parents:enroll_student_core_payment', course_id=course.id)
    else:
        messages.info(request, f'You are already enrolled in {course.title}.')
        return redirect('parents:student_dashboard')


@login_required(login_url='/parents/student/login/')
def enroll_student_core_payment(request, course_id):
    """
    Step 3: Show Razorpay Checkout Page
    """
    if not hasattr(request.user, 'student_profile'):
        messages.error(request, 'Access denied.')
        return redirect('parents:student_login')
        
    student = request.user.student_profile
    from core.models import Course
    course = get_object_or_404(Course, id=course_id)
    
    enrollment = get_object_or_404(CourseEnrollment, student=student, course=course)
    
    if enrollment.status == 'Active':
        messages.info(request, "You are already enrolled.")
        return redirect('parents:student_dashboard')

    # Create Razorpay Order
    amount_in_paise = int(course.price * 100) if course.price else 0
    if amount_in_paise == 0:
        enrollment.status = 'Active'
        enrollment.payment_status = 'Completed'
        enrollment.save()
        messages.success(request, f"Successfully enrolled in {course.title} for free.")
        return redirect('parents:student_dashboard')
        
    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
    order_data = {
        'amount': amount_in_paise,
        'currency': 'INR',
        'receipt': f'order_rcptid_{enrollment.id}',
        'payment_capture': 1
    }
    
    try:
        razorpay_order = client.order.create(data=order_data)
        enrollment.payment_reference = razorpay_order['id']
        enrollment.save()
        
        context = {
            'course': course,
            'enrollment': enrollment,
            'order_id': razorpay_order['id'],
            'amount_in_paise': amount_in_paise,
            'razorpay_key_id': settings.RAZORPAY_KEY_ID,
            'student': student
        }
        return render(request, 'parents/razorpay_checkout.html', context)
    except Exception as e:
        messages.error(request, f"Payment gateway error: {str(e)}")
        return redirect('parents:student_dashboard')


@csrf_exempt
def razorpay_success_callback(request):
    if request.method == "POST":
        razorpay_payment_id = request.POST.get('razorpay_payment_id', '')
        razorpay_order_id = request.POST.get('razorpay_order_id', '')
        razorpay_signature = request.POST.get('razorpay_signature', '')
        
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        params_dict = {
            'razorpay_order_id': razorpay_order_id,
            'razorpay_payment_id': razorpay_payment_id,
            'razorpay_signature': razorpay_signature
        }
        
        try:
            client.utility.verify_payment_signature(params_dict)
            
            # Find the enrollment by order ID
            enrollment = CourseEnrollment.objects.get(payment_reference=razorpay_order_id)
            enrollment.status = 'Active'
            enrollment.payment_status = 'Completed'
            enrollment.payment_date = timezone.now()
            enrollment.payment_reference = f"{razorpay_order_id}|{razorpay_payment_id}"
            enrollment.save()
            
            if request.user.is_authenticated and hasattr(request.user, 'student_profile'):
                 messages.success(request, f"Payment successful! You are now fully active in {enrollment.course.title}.")
                 return redirect('parents:student_dashboard')
            else:
                 return HttpResponse("Payment success. You can close this window and login to your dashboard.")
            
        except razorpay.errors.SignatureVerificationError:
            return HttpResponseBadRequest("Invalid Signature")
        except CourseEnrollment.DoesNotExist:
            return HttpResponseBadRequest("Enrollment record not found")
        except Exception as e:
            return HttpResponseBadRequest(f"Error: {str(e)}")
        
    return HttpResponseBadRequest("Invalid Request Method")


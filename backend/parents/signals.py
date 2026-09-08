from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.utils import timezone
from .models import Student, CourseEnrollment, Parent
from core.models import TopicProgress, QuizSubmission, Course as CoreCourse
from certifications.models import CertificationCourse

# 1. User Registration -> Auto Student Creation
# 1. User Registration -> Auto Student Creation
# REMOVED: create_student_profile signal to allow for manual Student creation by Parents.
# Students are now created via the 'add_student' view in the Parent Dashboard.


# 3. Progress Tracking -> Auto Update
@receiver(post_save, sender=TopicProgress)
def update_course_progress_on_topic(sender, instance, **kwargs):
    update_enrollment_progress(instance.student, instance.topic.course)

@receiver(post_save, sender=QuizSubmission)
def update_course_progress_on_quiz(sender, instance, **kwargs):
    if instance.quiz.topic and instance.quiz.topic.course:
        update_enrollment_progress(instance.student, instance.quiz.topic.course)
    elif instance.quiz.course:
         update_enrollment_progress(instance.student, instance.quiz.course)

def update_enrollment_progress(student, core_course):
    # Find corresponding CertificationCourse enrollment
    # Link: CertificationCourse.core_course == core_course
    try:
        cert_course = CertificationCourse.objects.get(core_course=core_course)
        enrollment = CourseEnrollment.objects.get(student=student, course=core_course)
        
        if enrollment.is_manually_modified:
            return  # Skip auto-update
            
        # Calculate Progress
        total_topics = core_course.topics.count()
        completed_topics = TopicProgress.objects.filter(
            student=student, 
            topic__course=core_course, 
            is_completed=True
        ).count()
        
        if total_topics > 0:
            new_percentage = int((completed_topics / total_topics) * 100)
            enrollment.completion_percentage = new_percentage
            
            # Check for completion
            if new_percentage == 100 and enrollment.status != 'Completed':
                enrollment.status = 'Completed'
                # Trigger Certificate Generation (via signal or direct call)
                from certifications.signals import generate_certificate_signal
                generate_certificate_signal.send(sender=CourseEnrollment, enrollment=enrollment)
            
            enrollment.save()
            
    except CertificationCourse.DoesNotExist:
        pass # No linked certification course
    except CourseEnrollment.DoesNotExist:
        pass # Student not enrolled

from django.dispatch import Signal, receiver
from django.utils import timezone
from .models import Certificate


# Define a custom signal
generate_certificate_signal = Signal()


@receiver(generate_certificate_signal)
def handle_certificate_generation(sender, enrollment, **kwargs):
    """
    Auto-generate a certificate when a course is completed.
    enrollment: CourseEnrollment instance (from parents app)
    
    Flow:
    1. Check if certificate already exists for this student + course
    2. Create Certificate record (ID auto-generates via model.save())
    3. Generate certificate image using Pillow (if template configured)
    4. Link certificate to student via StudentCertificate
    """
    from parents.models import StudentCertificate  # Local import to avoid circular dependency
    from .certificate_generator import generate_certificate_image

    student = enrollment.student
    course = enrollment.course  # This is a CertificationCourse instance

    # Check if certificate already exists
    if StudentCertificate.objects.filter(student=student, certificate__course=course).exists():
        return

    # Create Certificate record — ID auto-generates (INV-YYYY-NNNN)
    certificate = Certificate(
        student_name=student.full_name,
        course=course,
        issue_date=timezone.now().date(),
        status='Valid'
    )
    certificate.save()  # Triggers auto-ID generation in Certificate.save()

    # Generate certificate image if template is configured for this course
    if course.certificate_template:
        try:
            generate_certificate_image(certificate, course)
            certificate.save()  # Save again to persist the generated image
        except Exception as e:
            print(f"[CertGen] Image generation failed for {certificate.certificate_id}: {e}")

    # Link to Student via StudentCertificate
    StudentCertificate.objects.create(
        student=student,
        certificate=certificate,
        awarded_date=timezone.now().date(),
        status='Issued'
    )

    print(f"[CertGen] Generated Certificate {certificate.certificate_id} for {student.full_name}")

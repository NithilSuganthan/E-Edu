from django.db import models
from django.contrib.auth.models import User
from certifications.models import Certificate

class Parent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='parent_profile')
    phone_number = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    emergency_contact = models.CharField(max_length=15, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} (Parent)"

    class Meta:
        verbose_name = "Parent"
        verbose_name_plural = "Parents"


class Student(models.Model):
    parent = models.ForeignKey(Parent, on_delete=models.CASCADE, related_name='students')
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile', null=True, blank=True)
    full_name = models.CharField(max_length=200)
    date_of_birth = models.DateField()
    grade_level = models.CharField(max_length=50, help_text="e.g., 'Grade 5', 'Class 8'")
    enrollment_date = models.DateField()
    profile_image = models.ImageField(upload_to='student_profiles/', blank=True, null=True)
    level = models.IntegerField(default=1, help_text="Current student level")
    xp = models.IntegerField(default=0, help_text="Experience points")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.full_name} ({self.parent.user.get_full_name()})"

    class Meta:
        verbose_name = "Student"
        verbose_name_plural = "Students"
        ordering = ['-enrollment_date']


class CourseEnrollment(models.Model):
    STATUS_CHOICES = [
        ('Pending Payment', 'Pending Payment'),
        ('Active', 'Active'),
        ('Completed', 'Completed'),
        ('Paused', 'Paused'),
        ('Cancelled', 'Cancelled'),
    ]

    MODE_CHOICES = [
        ('Online', 'Online'),
        ('Offline', 'Offline'),
    ]

    PAYMENT_STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Completed', 'Completed'),
        ('Failed', 'Failed'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey('core.Course', on_delete=models.CASCADE)
    enrollment_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending Payment')
    mode = models.CharField(max_length=10, choices=MODE_CHOICES, default='Online')
    completion_percentage = models.IntegerField(default=0, help_text="0-100")
    current_level = models.CharField(max_length=100, blank=True, help_text="e.g., 'Module 3'")
    is_manually_modified = models.BooleanField(default=False, help_text="If True, auto-updates for progress will be skipped.")
    last_activity_date = models.DateTimeField(auto_now=True)
    
    # Payment Details
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='Pending')
    payment_reference = models.CharField(max_length=100, blank=True, help_text="Transaction ID or Reference")
    payment_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.student.full_name} - {self.course.title} ({self.status})"

    class Meta:
        verbose_name = "Course Enrollment"
        verbose_name_plural = "Course Enrollments"
        unique_together = ['student', 'course']


class LessonProgress(models.Model):
    STATUS_CHOICES = [
        ('NOT_STARTED', 'Not Started'),
        ('IN_PROGRESS', 'In Progress'),
        ('COMPLETED', 'Completed'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='lesson_progress')
    lesson = models.ForeignKey('core.Lesson', on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='NOT_STARTED')
    watched_percentage = models.PositiveIntegerField(default=0, help_text="Video watched %")
    completed_at = models.DateTimeField(null=True, blank=True)
    last_accessed = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['student', 'lesson']
    
    def __str__(self):
        return f"{self.student.full_name} - {self.lesson.title} ({self.status})"


class Attendance(models.Model):
    STATUS_CHOICES = [
        ('Present', 'Present'),
        ('Absent', 'Absent'),
        ('Late', 'Late'),
        ('Excused', 'Excused'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='attendance_records')
    course = models.ForeignKey('core.Course', on_delete=models.CASCADE)
    lesson = models.ForeignKey('core.Lesson', on_delete=models.SET_NULL, null=True, blank=True, help_text="Optional: Link to specific live lesson")
    date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.student.full_name} - {self.course.title} - {self.date} ({self.status})"

    class Meta:
        verbose_name = "Attendance"
        verbose_name_plural = "Attendance Records"
        ordering = ['-date']
        unique_together = ['student', 'course', 'date']


class ProgressTracker(models.Model):
    PROFICIENCY_CHOICES = [
        ('Beginner', 'Beginner'),
        ('Intermediate', 'Intermediate'),
        ('Advanced', 'Advanced'),
        ('Expert', 'Expert'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='progress_records')
    course = models.ForeignKey('core.Course', on_delete=models.CASCADE)
    skill_name = models.CharField(max_length=200, help_text="e.g., 'Python Basics', 'Circuit Design'")
    proficiency_level = models.CharField(max_length=20, choices=PROFICIENCY_CHOICES)
    score = models.IntegerField(help_text="0-100")
    last_updated = models.DateTimeField(auto_now=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.student.full_name} - {self.skill_name} ({self.proficiency_level})"

    class Meta:
        verbose_name = "Progress Tracker"
        verbose_name_plural = "Progress Trackers"
        ordering = ['-last_updated']


class TrainerFeedback(models.Model):
    CATEGORY_CHOICES = [
        ('Behavior', 'Behavior'),
        ('Technical Skills', 'Technical Skills'),
        ('Creativity', 'Creativity'),
        ('Teamwork', 'Teamwork'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='feedback_records')
    course = models.ForeignKey('core.Course', on_delete=models.CASCADE)
    trainer_name = models.CharField(max_length=200)
    feedback_date = models.DateField()
    feedback_text = models.TextField()
    rating = models.IntegerField(help_text="1-5 stars")
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)

    def __str__(self):
        return f"{self.student.full_name} - {self.trainer_name} ({self.feedback_date})"

    class Meta:
        verbose_name = "Trainer Feedback"
        verbose_name_plural = "Trainer Feedback"
        ordering = ['-feedback_date']


class StudentCertificate(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Issued', 'Issued'),
        ('Revoked', 'Revoked'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='certificates')
    certificate = models.ForeignKey(Certificate, on_delete=models.CASCADE)
    awarded_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')

    def __str__(self):
        return f"{self.student.full_name} - {self.certificate.certificate_id}"

    class Meta:
        verbose_name = "Student Certificate"
        verbose_name_plural = "Student Certificates"
        ordering = ['-awarded_date']


class Report(models.Model):
    REPORT_TYPE_CHOICES = [
        ('Monthly', 'Monthly'),
        ('Term', 'Term'),
        ('Annual', 'Annual'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='reports')
    report_type = models.CharField(max_length=20, choices=REPORT_TYPE_CHOICES)
    period_start = models.DateField()
    period_end = models.DateField()
    report_file = models.FileField(upload_to='reports/')
    generated_date = models.DateField(auto_now_add=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.student.full_name} - {self.report_type} ({self.period_start} to {self.period_end})"

    class Meta:
        verbose_name = "Report"
        verbose_name_plural = "Reports"
        ordering = ['-generated_date']


class Alert(models.Model):
    ALERT_TYPE_CHOICES = [
        ('Low Attendance', 'Low Attendance'),
        ('Payment Due', 'Payment Due'),
        ('Achievement', 'Achievement'),
        ('General', 'General'),
    ]

    SEVERITY_CHOICES = [
        ('Info', 'Info'),
        ('Warning', 'Warning'),
        ('Critical', 'Critical'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='alerts')
    alert_type = models.CharField(max_length=50, choices=ALERT_TYPE_CHOICES)
    message = models.TextField()
    severity = models.CharField(max_length=20, choices=SEVERITY_CHOICES, default='Info')
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.full_name} - {self.alert_type} ({self.severity})"

    class Meta:
        verbose_name = "Alert"
        verbose_name_plural = "Alerts"
        ordering = ['-created_at']

from django.db import models
from django.utils import timezone


class CertificationCourse(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    duration = models.CharField(max_length=50, help_text="e.g. '8 Weeks'")
    level = models.CharField(max_length=50, help_text="e.g. 'Beginner to Advanced'")
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    image = models.ImageField(upload_to='course_images/', blank=True, null=True)
    core_course = models.ForeignKey('core.Course', on_delete=models.SET_NULL, null=True, blank=True, help_text="Link to the core course content for progress tracking")
    whatsapp_group_link = models.URLField(blank=True, help_text="Invite link for the WhatsApp group (e.g., chat.whatsapp.com/...)")
    created_at = models.DateTimeField(auto_now_add=True)

    # Certificate Template Configuration
    certificate_template = models.ImageField(
        upload_to='certificate_templates/', blank=True, null=True,
        help_text="Upload the certificate background template image (recommended: 1200×850px, landscape PNG/JPG)"
    )
    
    FONT_CHOICES = [
        ('Inter.ttf', 'Inter (Modern Sans)'),
        ('Roboto.ttf', 'Roboto (Clean Sans)'),
        ('PlayfairDisplay.ttf', 'Playfair Display (Elegant Serif)'),
        ('GreatVibes.ttf', 'Great Vibes (Cursive)'),
    ]
    
    # Global Style
    font_family = models.CharField(max_length=50, choices=FONT_CHOICES, default='Inter.ttf', help_text="Primary font family")
    
    # Student Name
    name_position_x = models.IntegerField(default=600)
    name_position_y = models.IntegerField(default=340)
    name_font_size = models.IntegerField(default=52)
    name_color = models.CharField(max_length=7, default='#1a1a2e', help_text="Hex color for student name")
    
    # Details (Course, Date, ID)
    detail_font_family = models.CharField(max_length=50, choices=FONT_CHOICES, default='Inter.ttf', help_text="Font for details (optional override)")
    detail_font_size = models.IntegerField(default=24)
    detail_color = models.CharField(max_length=7, default='#1a1a2e', help_text="Hex color for details")
    
    # Detail Positions
    course_position_x = models.IntegerField(default=600)
    course_position_y = models.IntegerField(default=430)
    
    date_position_x = models.IntegerField(default=350)
    date_position_y = models.IntegerField(default=570)
    
    certid_position_x = models.IntegerField(default=850)
    certid_position_y = models.IntegerField(default=570)

    # Legacy field - kept for backward compatibility but hidden from new UI
    text_color = models.CharField(max_length=7, default='#1a1a2e', blank=True)

    def __str__(self):
        return self.name

class Certificate(models.Model):
    STATUS_CHOICES = [
        ('Valid', 'Valid'),
        ('Revoked', 'Revoked'),
    ]

    certificate_id = models.CharField(max_length=50, unique=True, db_index=True, blank=True,
                                       help_text="Leave blank to auto-generate (e.g., INV-2026-0042)")
    student_name = models.CharField(max_length=200)
    course = models.ForeignKey('core.Course', on_delete=models.CASCADE)
    issue_date = models.DateField()
    issued_by = models.CharField(max_length=100, default="Inventobots Academy")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Valid')
    certificate_image = models.ImageField(upload_to='certificate_images/', blank=True, null=True, help_text="Upload the certificate image")
    created_at = models.DateTimeField(auto_now_add=True)

    @classmethod
    def generate_certificate_id(cls):
        """Generate the next certificate ID in format INV-YYYY-NNNN."""
        year = timezone.now().year
        prefix = f"INV-{year}-"

        # Find the highest existing number for this year
        last_cert = (
            cls.objects
            .filter(certificate_id__startswith=prefix)
            .order_by('-certificate_id')
            .first()
        )

        if last_cert:
            try:
                last_number = int(last_cert.certificate_id.split('-')[-1])
                next_number = last_number + 1
            except (ValueError, IndexError):
                next_number = 1
        else:
            next_number = 1

        return f"{prefix}{next_number:04d}"

    def save(self, *args, **kwargs):
        if not self.certificate_id:
            self.certificate_id = Certificate.generate_certificate_id()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.certificate_id} - {self.student_name}"


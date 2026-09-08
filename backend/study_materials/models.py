from django.db import models
from core.models import Course

class StudyMaterial(models.Model):
    MATERIAL_TYPE_CHOICES = [
        ('PDF', 'PDF Document'),
        ('VIDEO', 'Video File'),
        ('IMAGE', 'Image'),
        ('ZIP', 'Zip/Archive'),
        ('LINK', 'External Link/Video URL'),
        ('OTHER', 'Other'),
    ]

    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='study_materials', help_text="Select the course this material belongs to.")
    title = models.CharField(max_length=200, help_text="Title of the study material (e.g., 'Chapter 1 Notes')")
    description = models.TextField(blank=True, help_text="Optional description or instructions.")
    material_type = models.CharField(max_length=10, choices=MATERIAL_TYPE_CHOICES, default='PDF')
    
    file = models.FileField(upload_to='study_materials/', blank=True, null=True, help_text="Upload the file (PDF, Video, etc.)")
    video_url = models.URLField(blank=True, null=True, help_text="YouTube or external video link (if not uploading a file)")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} ({self.course.title})"

    class Meta:
        verbose_name = "Study Material"
        verbose_name_plural = "Study Materials"
        ordering = ['-created_at']

class StudyMaterialFile(models.Model):
    study_material = models.ForeignKey(StudyMaterial, on_delete=models.CASCADE, related_name='files')
    file = models.FileField(upload_to='study_materials/files/')
    description = models.CharField(max_length=255, blank=True, help_text="Configurable description for the file")
    
    def __str__(self):
        return f"File for {self.study_material.title}"

from django.db import models

class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='courses/', blank=True, null=True)
    image_url = models.URLField(max_length=500, blank=True, null=True, help_text="External URL for image (used if Image file is not set)")
    thumbnail = models.ImageField(upload_to='course_thumbnails/', blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    CATEGORY_CHOICES = [
        ('ROBOTICS', 'Robotics'),
        ('CODING', 'Coding'),
        ('ABACUS', 'Abacus'),
        ('ACADEMIC', 'Academic'),
        ('INVENTOWRITE', 'Inventowrite'),
        ('INVENTOSHASTRA', 'Inventoshastra'),
        ('INVENTOTHUNAI', 'Inventothunai'),
        ('INVENTOPHONICS', 'Inventophonics'),
        ('INVENTOBEADS', 'Inventobeads'),
        ('INVENTOHINDI', 'Inventohindi'),
        ('OTHER', 'Other'),
    ]
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='OTHER')
    
    # Hero Slider Fields
    badge = models.CharField(max_length=100, blank=True, null=True)
    subtitle = models.CharField(max_length=200, blank=True, null=True)
    tagline = models.CharField(max_length=200, blank=True, null=True)
    highlights = models.JSONField(default=list, blank=True)
    color_gradient = models.CharField(max_length=100, default='from-blue-500 to-cyan-400')
    is_hero_featured = models.BooleanField(default=False)
    display_order = models.IntegerField(default=0)
    
    # CTA Fields
    cta_primary_url = models.CharField(max_length=1000, default='/courses/')
    cta_primary_text = models.CharField(max_length=50, default='Explore')
    cta_secondary_url = models.CharField(max_length=1000, blank=True, null=True)
    cta_secondary_text = models.CharField(max_length=50, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    # New Fields for Detailed View & Admin Management
    duration = models.PositiveIntegerField(default=0, help_text="Duration of the course in weeks")
    total_offline_classes = models.PositiveIntegerField(default=0, help_text="Total number of scheduled offline classes for attendance calculation.")
    syllabus = models.TextField(blank=True, null=True, help_text="Detailed syllabus or topics covered")
    MODE_CHOICES = [
        ('ONLINE', 'Online'),
        ('OFFLINE', 'Offline'),
        ('HYBRID', 'Hybrid'),
    ]
    mode = models.CharField(max_length=20, choices=MODE_CHOICES, default='ONLINE', help_text="Mode of the course")
    start_date = models.DateField(blank=True, null=True, help_text="Course start date (if applicable)")
    certification_details = models.TextField(blank=True, null=True, help_text="Details about certification")
    notes = models.TextField(blank=True, null=True, help_text="Any additional notes")

    def __str__(self):
        return self.title

class HeroSlide(Course):
    class Meta:
        proxy = True
        verbose_name = "Hero Slider Item"
        verbose_name_plural = "Hero Slider Items"
        ordering = ['display_order']

    def save(self, *args, **kwargs):
        self.is_hero_featured = True
        super().save(*args, **kwargs)

# --- Student Learning Models ---
# Note: Using string references for 'parents.Student' to avoid potential circular imports if parents app imports core

class Subject(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='subjects')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.course.title} - {self.title}"

class Module(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='modules')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.subject.title} - {self.title}"

class Lesson(models.Model):
    LESSON_TYPE_CHOICES = [
        ('VIDEO', 'Video'),
        ('LIVE_CLASS', 'Live Class'),
        ('READING', 'Reading'),
        ('QUIZ', 'Quiz'),
        ('ASSIGNMENT', 'Assignment'),
        ('EXTERNAL_LINK', 'External Link'),
    ]

    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=200)
    lesson_type = models.CharField(max_length=20, choices=LESSON_TYPE_CHOICES, default='VIDEO')
    order = models.PositiveIntegerField(default=0)
    
    # Content Fields
    video_url = models.URLField(blank=True, null=True, help_text="YouTube/Zoom recording link")
    live_link = models.URLField(blank=True, null=True, help_text="Zoom/Meet live session link")
    whatsapp_link = models.URLField(blank=True, null=True, help_text="WhatsApp group link")
    file_upload = models.FileField(upload_to='lesson_materials/', blank=True, null=True)
    content_text = models.TextField(blank=True, help_text="Rich text content for reading/notes")
    external_link = models.URLField(blank=True, null=True)
    
    # Meta
    is_preview = models.BooleanField(default=False, help_text="Allow free preview")
    duration_minutes = models.PositiveIntegerField(default=0, help_text="Estimated duration in minutes")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.module.title} - {self.title}"

# --- Student Learning Models ---
# Note: Using string references for 'parents.Student' to avoid potential circular imports if parents app imports core

class Topic(models.Model):
    # Deprecated: Retaining for migration safety, but should use Subject/Module/Lesson hierarchy
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='topics')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)
    video_url = models.URLField(blank=True, null=True, help_text="Link to video lecture")
    resources = models.TextField(blank=True, help_text="Links to resources, comma separated or JSON")

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.course.title} - {self.title}"

class TopicProgress(models.Model):
    student = models.ForeignKey('parents.Student', on_delete=models.CASCADE, related_name='topic_progress')
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    is_completed = models.BooleanField(default=False)
    time_spent_minutes = models.PositiveIntegerField(default=0)
    last_accessed = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['student', 'topic']

    def __str__(self):
        return f"{self.student} - {self.topic.title}"

class Quiz(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='quizzes')
    # Link to Lesson instead of Topic for new structure, but keep Topic for now
    lesson = models.OneToOneField(Lesson, on_delete=models.SET_NULL, null=True, blank=True, related_name='quiz_data')
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True, blank=True, related_name='quizzes')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    time_limit_minutes = models.PositiveIntegerField(default=15)
    passing_score = models.PositiveIntegerField(default=50)

    def __str__(self):
        return self.title

class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField()
    choices = models.JSONField(help_text="List of choices: {'A': 'Opt1', 'B': 'Opt2'}")
    correct_answer = models.CharField(max_length=1, help_text="Key of correct answer (e.g., 'A')")
    explanation = models.TextField(blank=True)

    def __str__(self):
        return f"{self.quiz.title} - {self.text[:50]}"

class QuizSubmission(models.Model):
    student = models.ForeignKey('parents.Student', on_delete=models.CASCADE, related_name='quiz_submissions')
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    score = models.FloatField()
    answers = models.JSONField(help_text="User answers keys")
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student} - {self.quiz.title} - {self.score}"

class Badge(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='badges/', blank=True, null=True)
    criteria = models.CharField(max_length=200, help_text="Internal criteria code (e.g., 'STREAK_5')")
    
    def __str__(self):
        return self.name

class StudentBadge(models.Model):
    student = models.ForeignKey('parents.Student', on_delete=models.CASCADE, related_name='badges_earned')
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE)
    earned_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['student', 'badge']
    
    def __str__(self):
        return f"{self.student} - {self.badge.name}"

from django.contrib import admin
from .models import Course, HeroSlide

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'is_hero_featured', 'display_order', 'price', 'created_at')
    list_filter = ('category', 'is_hero_featured')
    search_fields = ('title', 'description', 'subtitle', 'tagline')
    list_editable = ('is_hero_featured', 'display_order')
    
    fieldsets = (
        ('Main Info', {
            'fields': ('title', 'category', 'description', 'image', 'price', 
                      'duration', 'mode', 'start_date', 'syllabus', 'certification_details', 'notes')
        }),
        ('Hero Slider Configuration', {
            'fields': ('is_hero_featured', 'display_order', 'badge', 'subtitle', 'tagline', 'highlights', 'color_gradient'),
            'classes': ('collapse',),
        }),
        ('Call to Action', {
            'fields': ('cta_primary_url', 'cta_primary_text', 'cta_secondary_url', 'cta_secondary_text'),
            'classes': ('collapse',),
        }),
    )

@admin.register(HeroSlide)
class HeroSlideAdmin(admin.ModelAdmin):
    list_display = ('title', 'badge', 'display_order', 'category')
    list_editable = ('display_order',)
    search_fields = ('title', 'subtitle')
    
    # Only show items that are featured in hero slider
    def get_queryset(self, request):
        return super().get_queryset(request).filter(is_hero_featured=True)

    fieldsets = (
        ('Slide Content', {
            'fields': ('title', 'badge', 'subtitle', 'image', 'image_url', 'description', 'color_gradient', 'display_order')
        }),
        ('Highlights & Features', {
            'fields': ('tagline', 'highlights')
        }),
        ('Call to Action', {
            'fields': ('cta_primary_url', 'cta_primary_text', 'cta_secondary_url', 'cta_secondary_text')
        }),
        ('Course Linking (Optional)', {
            'fields': ('category', 'price'),
            'classes': ('collapse',),
            'description': 'If this slide represents a course, set the category and price here.'
        }),
    )

    def save_model(self, request, obj, form, change):
        obj.is_hero_featured = True
        super().save_model(request, obj, form, change)

from .models import Topic, TopicProgress, Quiz, Question, QuizSubmission, Badge, StudentBadge

class QuestionInline(admin.StackedInline):
    model = Question
    extra = 1

@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'topic', 'time_limit_minutes')
    list_filter = ('course',)
    inlines = [QuestionInline]

class TopicInline(admin.TabularInline):
    model = Topic
    extra = 1

# Note: Ideally we attach TopicInline to CourseAdmin, but CourseAdmin is already defined.
# We can unregister and re-register or just register Topic separately for now.

@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'order')
    list_filter = ('course',)
    ordering = ('course', 'order')

@admin.register(Badge)
class BadgeAdmin(admin.ModelAdmin):
    list_display = ('name', 'criteria')

@admin.register(StudentBadge)
class StudentBadgeAdmin(admin.ModelAdmin):
    list_display = ('student', 'badge', 'earned_at')

@admin.register(QuizSubmission)
class QuizSubmissionAdmin(admin.ModelAdmin):
    list_display = ('student', 'quiz', 'score', 'submitted_at')
    list_filter = ('quiz', 'submitted_at')

@admin.register(TopicProgress)
class TopicProgressAdmin(admin.ModelAdmin):
    list_display = ('student', 'topic', 'is_completed', 'last_accessed')
    list_filter = ('is_completed',)

from .models import Subject, Module, Lesson

class LessonInline(admin.StackedInline):
    model = Lesson
    extra = 1

@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ('title', 'subject', 'order')
    list_filter = ('subject__course', 'subject')
    ordering = ('subject', 'order')
    inlines = [LessonInline]

class ModuleInline(admin.StackedInline):
    model = Module
    extra = 1

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'order')
    list_filter = ('course',)
    ordering = ('course', 'order')
    inlines = [ModuleInline]

class SubjectInline(admin.StackedInline):
    model = Subject
    extra = 1

from study_materials.models import StudyMaterial

class StudyMaterialInline(admin.TabularInline):
    model = StudyMaterial
    extra = 5
    fields = ('title', 'material_type', 'file', 'video_url')

# Re-register Course with SubjectInline
admin.site.unregister(Course)
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'is_hero_featured', 'display_order', 'price', 'created_at')
    list_filter = ('category', 'is_hero_featured')
    search_fields = ('title', 'description')
    list_editable = ('is_hero_featured', 'display_order')
    inlines = [SubjectInline, StudyMaterialInline]
    
    fieldsets = (
        ('Main Info', {
            'fields': ('title', 'category', 'description', 'image', 'price', 
                      'duration', 'mode', 'start_date', 'syllabus', 'certification_details', 'notes')
        }),
        ('Hero Slider Configuration', {
            'fields': ('is_hero_featured', 'display_order', 'badge', 'subtitle', 'tagline', 'highlights', 'color_gradient'),
            'classes': ('collapse',),
        }),
        ('Call to Action', {
            'fields': ('cta_primary_url', 'cta_primary_text', 'cta_secondary_url', 'cta_secondary_text'),
            'classes': ('collapse',),
        }),
    )

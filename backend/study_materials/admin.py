from django.contrib import admin
from .models import StudyMaterial, StudyMaterialFile

class StudyMaterialFileInline(admin.TabularInline):
    model = StudyMaterialFile
    extra = 1

@admin.register(StudyMaterial)
class StudyMaterialAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'material_type', 'created_at')
    list_filter = ('course', 'material_type', 'created_at')
    search_fields = ('title', 'course__title', 'description')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
    inlines = [StudyMaterialFileInline]
    
    fieldsets = (
        ('Course Association', {
            'fields': ('course',)
        }),
        ('Material Details', {
            'fields': ('title', 'description', 'material_type', 'file', 'video_url')
        }),
    )

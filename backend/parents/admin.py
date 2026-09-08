from django.contrib import admin
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django import forms
from .models import (
    Parent, Student, CourseEnrollment, Attendance, 
    ProgressTracker, TrainerFeedback, StudentCertificate, Report, Alert
)


# Custom forms with better date input
class StudentAdminForm(forms.ModelForm):
    date_of_birth = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        help_text="Select or type date in YYYY-MM-DD format"
    )
    enrollment_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        help_text="Select or type date in YYYY-MM-DD format"
    )
    
    class Meta:
        model = Student
        fields = '__all__'


class CourseEnrollmentAdminForm(forms.ModelForm):
    enrollment_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        help_text="Select or type date in YYYY-MM-DD format"
    )
    
    class Meta:
        model = CourseEnrollment
        fields = '__all__'


class AttendanceAdminForm(forms.ModelForm):
    date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        help_text="Select or type date in YYYY-MM-DD format"
    )
    
    class Meta:
        model = Attendance
        fields = '__all__'


class TrainerFeedbackAdminForm(forms.ModelForm):
    feedback_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        help_text="Select or type date in YYYY-MM-DD format"
    )
    
    class Meta:
        model = TrainerFeedback
        fields = '__all__'


class StudentCertificateAdminForm(forms.ModelForm):
    awarded_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        help_text="Select or type date in YYYY-MM-DD format"
    )
    
    class Meta:
        model = StudentCertificate
        fields = '__all__'


class ReportAdminForm(forms.ModelForm):
    period_start = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        help_text="Select or type date in YYYY-MM-DD format"
    )
    period_end = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        help_text="Select or type date in YYYY-MM-DD format"
    )
    
    class Meta:
        model = Report
        fields = '__all__'


# Inline admin for Parent profile
class ParentInline(admin.StackedInline):
    model = Parent
    can_delete = False
    verbose_name_plural = 'Parent Profile'
    fields = ('phone_number', 'address', 'emergency_contact')


# Extend User admin to include Parent profile
class UserAdmin(BaseUserAdmin):
    # inlines = (ParentInline,) # Removed static declaration
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_parent')
    
    @admin.display(boolean=True, description='Is Parent')
    def is_parent(self, obj):
        return hasattr(obj, 'parent_profile')

    def get_inlines(self, request, obj=None):
        if obj:
            return [ParentInline]
        return []


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)


@admin.register(Parent)
class ParentAdmin(admin.ModelAdmin):
    list_display = ('get_parent_name', 'get_email', 'phone_number', 'student_count', 'created_at')
    search_fields = ('user__username', 'user__email', 'user__first_name', 'user__last_name', 'phone_number')
    list_filter = ('created_at',)
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('User Account', {
            'fields': ('user',)
        }),
        ('Contact Information', {
            'fields': ('phone_number', 'address', 'emergency_contact')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    @admin.display(description='Parent Name')
    def get_parent_name(self, obj):
        return obj.user.get_full_name() or obj.user.username
    
    @admin.display(description='Email')
    def get_email(self, obj):
        return obj.user.email
    
    @admin.display(description='Students')
    def student_count(self, obj):
        return obj.students.count()


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    form = StudentAdminForm
    list_display = ('full_name', 'parent', 'grade_level', 'enrollment_date', 'has_user_account', 'is_active', 'course_count')
    list_filter = ('is_active', 'grade_level', 'enrollment_date')
    search_fields = ('full_name', 'parent__user__first_name', 'parent__user__last_name', 'user__username')
    date_hierarchy = 'enrollment_date'
    readonly_fields = ('created_at', 'updated_at', 'user')
    
    fieldsets = (
        ('Student Information', {
            'fields': ('parent', 'user', 'full_name', 'date_of_birth', 'grade_level', 'profile_image')
        }),
        ('Enrollment', {
            'fields': ('enrollment_date', 'is_active', 'level', 'xp')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def has_add_permission(self, request):
        # Disable manual creation of students to enforce automation workflow
        return False
        
    @admin.display(description='Active Courses')
    def course_count(self, obj):
        return obj.enrollments.filter(status='Active').count()

    @admin.display(boolean=True, description='User Linked')
    def has_user_account(self, obj):
        return obj.user is not None


@admin.register(CourseEnrollment)
class CourseEnrollmentAdmin(admin.ModelAdmin):
    form = CourseEnrollmentAdminForm
    list_display = ('student', 'course', 'enrollment_date', 'status', 'completion_percentage', 'current_level', 'is_manually_modified')
    list_filter = ('status', 'is_manually_modified', 'course', 'enrollment_date')
    search_fields = ('student__full_name', 'course__name')
    date_hierarchy = 'enrollment_date'
    readonly_fields = ('last_activity_date',)
    
    fieldsets = (
        ('Enrollment Details', {
            'fields': ('student', 'course', 'enrollment_date', 'status')
        }),
        ('Progress', {
            'fields': ('completion_percentage', 'current_level', 'is_manually_modified')
        }),
        ('Metadata', {
            'fields': ('last_activity_date',),
            'classes': ('collapse',)
        })
    )

    actions = ['activate_enrollment']

    @admin.action(description="Activate selected enrollments (Mark Paid)")
    def activate_enrollment(self, request, queryset):
        queryset.update(status='Active', payment_status='Completed', payment_date=timezone.now())
        self.message_user(request, "Selected enrollments have been activated.")


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    form = AttendanceAdminForm
    list_display = ('student', 'course', 'date', 'status', 'has_notes')
    list_filter = ('status', 'course', 'date')
    search_fields = ('student__full_name', 'course__name')
    date_hierarchy = 'date'
    
    fieldsets = (
        ('Attendance Record', {
            'fields': ('student', 'course', 'date', 'status')
        }),
        ('Additional Information', {
            'fields': ('notes',),
            'classes': ('collapse',)
        }),
    )
    
    @admin.display(boolean=True, description='Notes')
    def has_notes(self, obj):
        return bool(obj.notes)


@admin.register(ProgressTracker)
class ProgressTrackerAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'skill_name', 'proficiency_level', 'score', 'last_updated')
    list_filter = ('proficiency_level', 'course', 'last_updated')
    search_fields = ('student__full_name', 'skill_name', 'course__name')
    date_hierarchy = 'last_updated'
    
    fieldsets = (
        ('Progress Details', {
            'fields': ('student', 'course', 'skill_name')
        }),
        ('Performance', {
            'fields': ('proficiency_level', 'score', 'notes')
        }),
        ('Timestamp', {
            'fields': ('last_updated',),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('last_updated',)


@admin.register(TrainerFeedback)
class TrainerFeedbackAdmin(admin.ModelAdmin):
    form = TrainerFeedbackAdminForm
    list_display = ('student', 'course', 'trainer_name', 'feedback_date', 'rating', 'category')
    list_filter = ('category', 'rating', 'course', 'feedback_date')
    search_fields = ('student__full_name', 'trainer_name', 'course__name', 'feedback_text')
    date_hierarchy = 'feedback_date'
    
    fieldsets = (
        ('Feedback Details', {
            'fields': ('student', 'course', 'trainer_name', 'feedback_date')
        }),
        ('Feedback Content', {
            'fields': ('category', 'rating', 'feedback_text')
        }),
    )


@admin.register(StudentCertificate)
class StudentCertificateAdmin(admin.ModelAdmin):
    form = StudentCertificateAdminForm
    list_display = ('student', 'certificate', 'awarded_date', 'status')
    list_filter = ('status', 'awarded_date')
    search_fields = ('student__full_name', 'certificate__certificate_id', 'certificate__student_name')
    date_hierarchy = 'awarded_date'
    
    fieldsets = (
        ('Certificate Assignment', {
            'fields': ('student', 'certificate', 'awarded_date', 'status')
        }),
    )


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    form = ReportAdminForm
    list_display = ('student', 'report_type', 'period_start', 'period_end', 'generated_date', 'has_file')
    list_filter = ('report_type', 'generated_date')
    search_fields = ('student__full_name',)
    date_hierarchy = 'generated_date'
    readonly_fields = ('generated_date',)
    
    fieldsets = (
        ('Report Details', {
            'fields': ('student', 'report_type', 'period_start', 'period_end')
        }),
        ('Report File', {
            'fields': ('report_file', 'notes')
        }),
        ('Timestamp', {
            'fields': ('generated_date',),
            'classes': ('collapse',)
        }),
    )
    
    @admin.display(boolean=True, description='File Uploaded')
    def has_file(self, obj):
        return bool(obj.report_file)


@admin.register(Alert)
class AlertAdmin(admin.ModelAdmin):
    list_display = ('student', 'alert_type', 'severity', 'is_read', 'created_at', 'short_message')
    list_filter = ('alert_type', 'severity', 'is_read', 'created_at')
    search_fields = ('student__full_name', 'message')
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at',)
    actions = ['mark_as_read', 'mark_as_unread']
    
    fieldsets = (
        ('Alert Details', {
            'fields': ('student', 'alert_type', 'severity')
        }),
        ('Message', {
            'fields': ('message', 'is_read')
        }),
        ('Timestamp', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    @admin.display(description='Message Preview')
    def short_message(self, obj):
        return obj.message[:50] + '...' if len(obj.message) > 50 else obj.message
    
    @admin.action(description="Mark selected alerts as read")
    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)
    
    @admin.action(description="Mark selected alerts as unread")
    def mark_as_unread(self, request, queryset):
        queryset.update(is_read=False)

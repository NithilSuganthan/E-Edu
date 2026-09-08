from django.contrib import admin
from django import forms
from django.utils.html import format_html, mark_safe
from django.urls import reverse
from .models import CertificationCourse, Certificate


# Custom form for Certificate with better date input
class CertificateAdminForm(forms.ModelForm):
    issue_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        help_text="Select or type date in YYYY-MM-DD format"
    )
    
    class Meta:
        model = Certificate
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make certificate_id optional — auto-generated if left blank
        if 'certificate_id' in self.fields:
            self.fields['certificate_id'].required = False
            if not self.instance.pk:
                self.fields['certificate_id'].widget.attrs['placeholder'] = 'Auto-generated (e.g., INV-2026-0042)'


@admin.register(CertificationCourse)
class CertificationCourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'duration', 'level', 'has_template', 'open_editor_link', 'created_at')
    search_fields = ('name', 'level')
    
    fieldsets = (
        ('Course Details', {
            'fields': ('name', 'description', 'duration', 'level', 'price', 'image', 'core_course', 'whatsapp_group_link'),
        }),
        ('Certificate Template Settings', {
            'fields': (
                'certificate_template',
                ('font_family', 'detail_font_family'),
                ('name_position_x', 'name_position_y', 'name_font_size', 'name_color'),
                ('course_position_x', 'course_position_y'),
                ('date_position_x', 'date_position_y'),
                ('certid_position_x', 'certid_position_y'),
                ('detail_font_size', 'detail_color'),
            ),
            'classes': ('collapse',),
            'description': 'Upload a template image, save, then use the Visual Editor to drag-and-drop text positions. '
                          'Or manually enter X/Y coordinates below.',
        }),
    )
    
    @admin.display(boolean=True, description='Template')
    def has_template(self, obj):
        return bool(obj.certificate_template)
    
    @admin.display(description='Editor')
    def open_editor_link(self, obj):
        if obj.pk and obj.certificate_template:
            url = reverse('admin:certifications_template_editor', args=[obj.pk])
            return format_html(
                '<a href="{}" style="'
                'display:inline-block; padding:4px 12px; background:#8b5cf6; color:white; '
                'border-radius:6px; font-size:12px; font-weight:700; text-decoration:none;'
                '">🎨 Visual Editor</a>',
                url
            )
        elif obj.pk:
            return mark_safe('<span style="color:#999;">Upload template first</span>')
        return mark_safe('—')
    
    def get_urls(self):
        from django.urls import path
        custom_urls = [
            path(
                '<int:course_id>/template-editor/',
                self.admin_site.admin_view(self.template_editor_view),
                name='certifications_template_editor',
            ),
        ]
        return custom_urls + super().get_urls()
    
    def template_editor_view(self, request, course_id):
        from django.shortcuts import get_object_or_404, redirect
        from django.template.response import TemplateResponse
        from django.contrib import messages
        
        course = get_object_or_404(CertificationCourse, pk=course_id)
        
        if request.method == 'POST':
            # Save the dragged positions and styles
            position_fields = [
                'name_position_x', 'name_position_y', 'name_font_size', 'name_color',
                'course_position_x', 'course_position_y',
                'date_position_x', 'date_position_y',
                'certid_position_x', 'certid_position_y',
                'detail_font_size', 'detail_color',
                'font_family', 'detail_font_family',
            ]
            for field in position_fields:
                value = request.POST.get(field)
                if value is not None:
                    if 'color' in field or 'family' in field:
                        setattr(course, field, value)
                    else:
                        try:
                            setattr(course, field, int(value))
                        except (ValueError, TypeError):
                            pass
            course.save()
            messages.success(request, f'✅ Template positions & styles saved for "{course.name}"!')
            return redirect(request.path)
        
        context = {
            **self.admin_site.each_context(request),
            'course': course,
            'title': f'Template Editor — {course.name}',
            'opts': self.model._meta,
        }
        return TemplateResponse(
            request,
            'admin/certifications/template_editor_v2.html',
            context,
        )


@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    form = CertificateAdminForm
    list_display = ('certificate_id', 'student_name', 'course', 'issue_date', 'status', 'has_image')
    list_filter = ('status', 'course', 'issue_date')
    search_fields = ('certificate_id', 'student_name')
    ordering = ('-issue_date',)
    
    fieldsets = (
        ('Certificate Details', {
            'fields': ('certificate_id', 'student_name', 'course', 'issue_date', 'issued_by', 'status'),
        }),
        ('Certificate Image', {
            'fields': ('template_preview', 'edit_template_link', 'certificate_image', 'generated_image_preview'),
            'description': 'The certificate image is auto-generated from the course template when a student completes the course. '
                          'You can also upload a custom image to override the auto-generated one.',
        }),
    )
    
    def get_readonly_fields(self, request, obj=None):
        readonly = ['template_preview', 'edit_template_link', 'generated_image_preview']
        if obj and obj.certificate_id:
            readonly.append('certificate_id')
        return readonly
    
    @admin.display(boolean=True, description='Image')
    def has_image(self, obj):
        return bool(obj.certificate_image)
    
    @admin.display(description='Course Template Preview')
    def template_preview(self, obj):
        """Show the course's certificate template with simulated text overlay."""
        if not obj.pk or not obj.course:
            return mark_safe('<span style="color: #999;">Select a course first, then save to see the template preview.</span>')
        
        course = obj.course
        if course.certificate_template:
            # Calculate positions as percentages for responsive preview
            try:
                # Default to 1200x850 if image dimensions not available
                img_w = course.certificate_template.width if hasattr(course.certificate_template, 'width') else 1200
                img_h = course.certificate_template.height if hasattr(course.certificate_template, 'height') else 850
                
                # Helper to get style string
                def get_style(x, y, size, color, font_family, bold=False):
                    # Convert absolute pixels to percentage for responsive scaling
                    left_pct = (x / img_w) * 100
                    # Add 10px offset to match generator and editor
                    top_pct = ((y + 10) / img_h) * 100
                    # Scale font size roughly based on a 500px wide preview
                    font_name = font_family.replace('.ttf', '')
                    return (
                        f"position: absolute; left: {left_pct}%; top: {top_pct}%; "
                        f"transform: translate(-50%, 0); "
                        f"font-size: {size * 0.4}px; color: {color}; "
                        f"font-weight: {'bold' if bold else 'normal'}; white-space: nowrap;"
                        f"font-family: '{font_name}', sans-serif;"
                    )

                preview_html = f"""
                <link href="https://fonts.googleapis.com/css2?family=Great+Vibes&family=Inter:wght@400;700&family=Playfair+Display:wght@400;700&family=Roboto:wght@400;700&display=swap" rel="stylesheet">
                <div style="position: relative; display: inline-block; max-width: 500px; border: 2px solid #ddd; border-radius: 8px; overflow: hidden;">
                    <img src="{course.certificate_template.url}" style="display: block; width: 100%; height: auto;">
                    
                    <div style="{get_style(course.name_position_x, course.name_position_y, course.name_font_size, course.name_color, course.font_family, bold=True)}">
                        {obj.student_name if obj.student_name else 'Student Name'}
                    </div>
                    
                    <div style="{get_style(course.course_position_x, course.course_position_y, course.detail_font_size, course.detail_color, course.detail_font_family)}">
                        {course.name}
                    </div>
                    
                    <div style="{get_style(course.date_position_x, course.date_position_y, course.detail_font_size, course.detail_color, course.detail_font_family)}">
                        {obj.issue_date.strftime('%B %d, %Y') if obj.issue_date else 'Issue Date'}
                    </div>
                    
                    <div style="{get_style(course.certid_position_x, course.certid_position_y, course.detail_font_size, course.detail_color, course.detail_font_family)}">
                        {obj.certificate_id if obj.certificate_id else 'INV-2026-XXXX'}
                    </div>
                </div>
                """
                return mark_safe(preview_html)
            except Exception as e:
                return mark_safe(f"Error generating preview: {str(e)}")
        else:
            return format_html(
                '<span style="color: #e74c3c; font-weight: bold;">⚠ No template uploaded for "{}".</span>'
                '<br><small>Upload a template image in the course settings, or upload a custom certificate image below.</small>',
                course.name
            )
    
    @admin.display(description='Template Settings')
    def edit_template_link(self, obj):
        """Provide a direct link to the visual template editor."""
        if not obj.pk or not obj.course:
            return mark_safe('<span style="color: #999;">—</span>')
        
        if obj.course.certificate_template:
            url = reverse('admin:certifications_template_editor', args=[obj.course.pk])
            return format_html(
                '<a href="{}" target="_blank" style="'
                'display: inline-block; padding: 8px 16px; '
                'background: #8b5cf6; color: white; text-decoration: none; '
                'border-radius: 6px; font-weight: bold; font-size: 13px;'
                '">🎨 Open Visual Editor for "{}"</a>',
                url, obj.course.name
            )
        else:
            url = reverse('admin:certifications_certificationcourse_change', args=[obj.course.pk])
            return format_html(
                '<a href="{}" target="_blank" style="'
                'display: inline-block; padding: 8px 16px; '
                'background: #3498db; color: white; text-decoration: none; '
                'border-radius: 6px; font-weight: bold; font-size: 13px;'
                '">⬆️ Upload Template for "{}"</a>',
                url, obj.course.name
            )
    
    @admin.display(description='Current Certificate Image')
    def generated_image_preview(self, obj):
        """Show the generated/uploaded certificate image."""
        if obj.certificate_image:
            return format_html(
                '<div style="margin: 10px 0;">'
                '<img src="{}" style="max-width: 500px; max-height: 350px; border: 2px solid #28a745; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);" />'
                '<br><small style="color: #28a745; font-weight: bold;">✅ Certificate image ready for download</small>'
                '</div>',
                obj.certificate_image.url
            )
        return mark_safe('<span style="color: #999;">No certificate image generated yet.</span>')

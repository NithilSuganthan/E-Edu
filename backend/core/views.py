from django.shortcuts import render
from django.views.generic import TemplateView
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate, login
from .models import Course
from .models import Course, Lesson
import json
from parents.models import LessonProgress, CourseEnrollment, Student

# --- Template Views ---
class HomeView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Fetch hero courses
        hero_courses = Course.objects.filter(is_hero_featured=True).order_by('display_order')
        
        slides = []
        for c in hero_courses:
            slides.append({
                'badge': c.badge,
                'title': c.title,
                'subtitle': c.subtitle,
                'desc': c.description,
                'tagline': c.tagline,
                'highlights': c.highlights,
                'image': c.image.url if c.image else (c.image_url if c.image_url else ''), 
                'color': c.color_gradient,
                'cta_p': c.cta_primary_url,
                'cta_p_text': c.cta_primary_text,
                'cta_s': c.cta_secondary_url,
                'cta_s_text': c.cta_secondary_text,
            })
            
        # Append Founders Slide
        slides.append({
            'badge': 'LEADERSHIP',
            'title': 'Meet Our Founding Team',
            'subtitle': 'Visionaries with 15+ Years of Industry Experience',
            'desc': 'Led by experts from top tech giants like Visa, Shell, Juniper, and Opentext. Our founders bring decades of experience in Architecture, Cyber Security, FullStack Development, and Product Marketing to shape the next generation of inventors.',
            'tagline': 'Guided by Excellence',
            'highlights': [
                'Saivadurai Jeyaraman - Tech Architect',
                'Prakashkumar - Cyber Security & ML',
                'Harinarayanan N R - Cloud & FullStack',
                'Ramesh Ganesan - Business & Strategy'
            ],
            'image': '/media/founders.jpg',
            'color': 'from-purple-600 to-indigo-600',
            'cta_p': '/about/',
            'cta_p_text': 'Know More',
            'cta_s': None,
            'cta_s_text': None
        })

        context['hero_slides_json'] = json.dumps(slides)
        return context

# --- API Views ---
class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return Response({'status': 'success', 'user': user.username})
        return Response({'status': 'error', 'message': 'Invalid credentials'}, status=401)

class CourseListView(APIView):
    def get(self, request):
        category = request.query_params.get('category')
        if category:
            courses = Course.objects.filter(category=category)
        else:
            courses = Course.objects.all()

        data = []
        for c in courses:
            data.append({
                'id': c.id,
                'title': c.title,
                'description': c.description,
                'price': c.price if c.price else 'Free', # Handle None price
                'category': c.category,
                'image': c.image.url if c.image else (c.image_url if c.image_url else 'https://images.unsplash.com/photo-1516321318423-f06f85e504b3?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.0.3'),
                # New fields for detailed view
                'duration': c.duration,
                'syllabus': c.syllabus,
                'mode': c.mode,
                'start_date': c.start_date,
                'certification_details': c.certification_details,
                'notes': c.notes,
            })
        return Response(data)

from django.shortcuts import get_object_or_404
from django.db.models import Prefetch
from .models import Subject, Module, Lesson
from study_materials.models import StudyMaterial
from parents.models import LessonProgress, CourseEnrollment

class CoursePlayerView(TemplateView):
    template_name = 'course_player.html'

    def get_context_data(self, course_id, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # 1. Fetch Course with Hierarchy
        course = get_object_or_404(
            Course.objects.prefetch_related(
                Prefetch('subjects', queryset=Subject.objects.order_by('order').prefetch_related(
                    Prefetch('modules', queryset=Module.objects.order_by('order').prefetch_related(
                        Prefetch('lessons', queryset=Lesson.objects.order_by('order'))
                    ))
                )),
                Prefetch('study_materials', queryset=StudyMaterial.objects.prefetch_related('files'))
            ),
            id=course_id
        )
        context['course'] = course

        # 2. Check Enrollment & Progress
        if self.request.user.is_authenticated and hasattr(self.request.user, 'student_profile'):
            student = self.request.user.student_profile
            # Verify enrollment
            enrollment = CourseEnrollment.objects.filter(student=student, course=course).first()
            context['is_enrolled'] = bool(enrollment)
            
            if enrollment:
                # Fetch progress for all lessons in this course
                # We'll create a dictionary {lesson_id: progress_obj} for easy lookup in template
                progress_qs = LessonProgress.objects.filter(student=student, lesson__module__subject__course=course)
                progress_map = {p.lesson_id: p for p in progress_qs}
                context['progress_map'] = progress_map
                
                # Stats
                context['total_lessons'] = Lesson.objects.filter(module__subject__course=course).count()
                context['completed_lessons'] = progress_qs.filter(status='COMPLETED').count()
        else:
            context['is_enrolled'] = False
            
        # 3. Get First Lesson for Initial Load
        first_lesson = None
        # Use prefetched data to ensure matching order and avoid extra queries
        all_subjects = list(course.subjects.all())
        if all_subjects:
            first_subject = all_subjects[0]
            all_modules = list(first_subject.modules.all())
            if all_modules:
                first_module = all_modules[0]
                all_lessons = list(first_module.lessons.all())
                all_lessons = list(first_module.lessons.all())
                if all_lessons:
                    first_lesson = all_lessons[0]
        
        # Fallback: If hierarchy traversal failed (e.g. first subject has no modules), find ANY first lesson
        if not first_lesson:
            first_lesson = Lesson.objects.filter(module__subject__course=course).order_by('module__subject__order', 'module__order', 'order').first()

        context['first_lesson'] = first_lesson
        
        return context

class MarkLessonCompleteView(APIView):
    def post(self, request, lesson_id):
        if not request.user.is_authenticated or not hasattr(request.user, 'student_profile'):
            return Response({'status': 'error', 'message': 'Unauthorized'}, status=401)
        
        student = request.user.student_profile
        lesson = get_object_or_404(Lesson, id=lesson_id)
        
        # Verify enrollment in the course this lesson belongs to
        course = lesson.module.subject.course
        if not CourseEnrollment.objects.filter(student=student, course=course).exists():
            return Response({'status': 'error', 'message': 'Not enrolled'}, status=403)
            
        # Update or Create Progress
        progress, created = LessonProgress.objects.get_or_create(student=student, lesson=lesson)
        progress.status = 'COMPLETED'
        progress.watched_percentage = 100
        progress.completed_at = timezone.now()
        progress.save()
        
        return Response({'status': 'success', 'lesson_id': lesson_id})

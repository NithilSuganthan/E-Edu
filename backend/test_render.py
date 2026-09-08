import os
import django
from django.template.loader import render_to_string
from django.test import RequestFactory
from django.contrib.auth.models import User

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from core.models import Course, Subject, Module, Lesson
from core.views import CoursePlayerView

def test_render(course_id):
    factory = RequestFactory()
    user = User.objects.first() # Use any user
    request = factory.get(f'/api/course/{course_id}/learn/')
    request.user = user
    
    view = CoursePlayerView()
    view.request = request
    view.kwargs = {'course_id': course_id}
    
    context = view.get_context_data(course_id=course_id)
    html = render_to_string('course_player.html', context)
    
    with open('rendered_output.html', 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"Render component checks for Course {course_id}:")
    print(f"Course Title present: {context['course'].title in html}")
    print(f"Material 'Chapter 1 notes' present: {'Chapter 1 notes' in html}")
    print(f"PDF Link present: {'Session_-_24_or.pdf' in html}")
    print(f"Total HTML size: {len(html)} bytes")

if __name__ == "__main__":
    test_render(31)

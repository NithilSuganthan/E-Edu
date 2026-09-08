import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from core.models import Course, Subject, Module, Lesson
from study_materials.models import StudyMaterial, StudyMaterialFile

def debug_course(course_id):
    try:
        course = Course.objects.get(id=course_id)
        print(f"Course: {course.title} (ID: {course.id})")
        
        subjects = Subject.objects.filter(course=course)
        print(f"Subjects: {subjects.count()}")
        for s in subjects:
            print(f"  - {s.title}")
            modules = Module.objects.filter(subject=s)
            for m in modules:
                print(f"    - {m.title}")
                lessons = Lesson.objects.filter(module=m)
                for l in lessons:
                    print(f"      - {l.title}")
        
        materials = StudyMaterial.objects.filter(course=course)
        print(f"Study Materials: {materials.count()}")
        for m in materials:
            print(f"  - Material ID {m.id}: {m.title}")
            print(f"    Type: {m.material_type}")
            print(f"    Main File: {m.file}")
            print(f"    Video URL: {m.video_url}")
            
            files = StudyMaterialFile.objects.filter(study_material=m)
            print(f"    Inline Files: {files.count()}")
            for f in files:
                print(f"      - File ID {f.id}: {f.file}")
                
    except Course.DoesNotExist:
        print(f"Course ID {course_id} not found.")

if __name__ == "__main__":
    debug_course(31)

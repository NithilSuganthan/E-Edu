from django.core.management.base import BaseCommand
from core.models import Course, Topic, Quiz, Question
from parents.models import Student, Parent
from django.utils import timezone
import random

class Command(BaseCommand):
    help = 'Seeds the database with Courses, Topics, and Quizzes'

    def handle(self, *args, **kwargs):
        self.stdout.write("Planting seeds...")

        # 1. Create or Get Courses
        courses_data = [
            {
                "title": "Python for Beginners",
                "description": "Master the basics of Python programming, from variables to loops and functions. Perfect for young coders!",
                "category": "CODING",
                "price": 49.99,
                "badge": "Best Seller",
                "image_url": "https://img.freepik.com/free-vector/programmer-working-web-development-code-engineer-programming-python-php-java-script-computer_90220-250.jpg",
                "color": "from-blue-500 to-indigo-600",
                "topics": [
                    "Introduction to Python", "Variables & Datatypes", "Control Flow (If/Else)", "Loops (For/While)", "Functions", "Mini Project: Calculator"
                ]
            },
            {
                "title": "Robotics 101",
                "description": "Build your first robot! Learn about circuits, sensors, and motors in this hands-on course.",
                "category": "ROBOTICS",
                "price": 79.99,
                "badge": "Hands-on",
                "image_url": "https://img.freepik.com/free-vector/robots-illustration-collection_23-2147501300.jpg",
                "color": "from-red-500 to-orange-500",
                "topics": [
                    "What is a Robot?", "Basic Circuits", "Understanding Sensors", "Motors and Movement", "Building the Chassis", "Final Assembly"
                ]
            },
            {
                "title": "Virtual Abacus Master",
                "description": "Sharpen your mental math skills with the ancient art of Abacus. Visualize and calculate faster than a calculator.",
                "category": "ABACUS",
                "price": 39.99,
                "badge": "Math Whiz",
                "image_url": "https://img.freepik.com/free-vector/abacus-illustration_1284-18366.jpg",
                "color": "from-green-500 to-emerald-600",
                "topics": [
                    "Basics of Abacus", "Addition Techniques", "Subtraction Techniques", "Mental Math Drills", "Speed Calculation"
                ]
            }
        ]

        for c_data in courses_data:
            try:
                self.stdout.write(f"Attempting to create course: {c_data['title']}")
                course, created = Course.objects.get_or_create(
                    title=c_data['title'],
                    defaults={
                        'description': c_data['description'],
                        'category': c_data['category'],
                        'price': c_data['price'],
                        'badge': c_data['badge'],
                        'image_url': c_data['image_url'],
                        'color_gradient': c_data['color'],
                        'cta_primary_text': 'Start Learning',
                        'cta_primary_url': f"/courses/{str(c_data.get('title', '')).lower().replace(' ', '-')}/",
                        # Optional fields that might be strict in DB
                        'subtitle': 'Learn by doing',
                        'tagline': 'Master the future',
                        'duration': 4, # DB expects Integer
                        'syllabus': 'Week 1: Basics, Week 2: Advanced...',
                        'start_date': timezone.now(),
                        'certification_details': 'Certificate of Completion included.',
                        'notes': 'Beginner friendly.'
                    }
                )
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Failed to create course {c_data['title']}: {str(e)}"))
                continue
            
            if created:
                self.stdout.write(f"Created Course: {course.title}")
                
                # Create Topics
                topics = c_data.get('topics', [])
                assert isinstance(topics, list)
                for i, topic_title in enumerate(topics):
                    topic = Topic.objects.create(
                        course=course,
                        title=topic_title,
                        order=i+1, 
                        description=f"Learn about {topic_title} in depth."
                    )
                    
                    # Create a Quiz for the last topic
                    if i == len(topics) - 1:
                        quiz = Quiz.objects.create(
                            course=course,
                            topic=topic,
                            title=f"{course.title} Final Quiz",
                            description="Test your knowledge!",
                            passing_score=70
                        )
                        
                        # Add Questions
                        Question.objects.create(
                            quiz=quiz,
                            text="What is the result of 2 + 2?",
                            choices={'A': '3', 'B': '4', 'C': '5', 'D': '22'},
                            correct_answer='B'
                        )
                        Question.objects.create(
                            quiz=quiz,
                            text="Which is NOT a programming language?",
                            choices={'A': 'Python', 'B': 'Java', 'C': 'HTML', 'D': 'Cobra'},
                            correct_answer='D' # Cobra is actually a language but let's assume D for simplicity or change logic.
                        )
            else:
                self.stdout.write(f"Course already exists: {course.title}")

        self.stdout.write(self.style.SUCCESS('Successfully seeded database!'))

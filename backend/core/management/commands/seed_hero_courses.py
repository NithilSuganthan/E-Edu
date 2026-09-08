from django.core.management.base import BaseCommand
from core.models import Course
import json

class Command(BaseCommand):
    help = 'Seeds the database with hero slider courses'

    def handle(self, *args, **kwargs):
        courses_data = [
            {
                'badge': 'Ages 8+ Pioneers',
                'title': 'SPARK THE FUTURE',
                'subtitle': "MASTER TOMORROW'S SKILLS",
                'description': 'From Robotics and Coding to Maths and Abacus. We provide the tools for the next generation of inventors.',
                'image_url': 'https://images.unsplash.com/photo-1581092160562-40aa08e78837?auto=format&fit=crop&q=80&w=1000',
                'color': 'from-blue-500 to-cyan-400',
                'cta_p': '/courses/',
                'cta_p_text': 'Explore Courses',
                'cta_s': 'https://www.google.com/maps/place/Inventobots+Academy/@12.9760844,80.176346,15z/data=!4m6!3m5!1s0x3a525fed04cdf603:0x164058f0b4ca8c85!8m2!3d12.979803!4d80.1829627!16s%2Fg%2F11yrgl28hg?entry=ttu&g_ep=EgoyMDI1MTIwOS4wIKXMDSoKLDEwMDc5MjA2N0gBUAM%3D',
                'cta_s_text': 'Find Center',
                'category': 'OTHER',
                'is_featured': True,
                'order': 1
            },
            {
                'badge': 'Hands-on Learning',
                'title': 'BUILD. CODE. CREATE.',
                'subtitle': 'ROBOTICS MASTERCLASS',
                'description': 'Dive into the world of automation, sensors, and mechanical engineering. Turn complex concepts into exciting challenges.',
                'image_url': 'https://images.unsplash.com/photo-1531297484001-80022131f5a1?auto=format&fit=crop&w=1000&q=80',
                'color': 'from-fuchsia-500 to-purple-600',
                'cta_p': '/robotics/',
                'cta_p_text': 'Start Building',
                'cta_s': '/courses/',
                'cta_s_text': 'View Curriculum',
                'category': 'ROBOTICS',
                'is_featured': True,
                'order': 2
            },
            {
                'badge': 'Virtual Simulation',
                'title': 'LEARN ANYWHERE',
                'subtitle': 'INTERACTIVE ONLINE LAB',
                'description': 'Experience our cutting-edge virtual simulator. Experiment with circuits and code without needing physical hardware.',
                'image_url': 'https://images.unsplash.com/photo-1555949963-aa79dcee981c?auto=format&fit=crop&w=1000&q=80',
                'color': 'from-emerald-400 to-teal-500',
                'cta_p': '/lab/',
                'cta_p_text': 'Launch Lab',
                'cta_s': '/courses/',
                'cta_s_text': 'All Programs',
                'category': 'OTHER',
                'is_featured': True,
                'order': 3
            },
            {
                'badge': 'Grades 10 – 12',
                'title': 'INVENTOSHASTRA',
                'subtitle': 'PCM Mastery Program',
                'tagline': 'Excel in Physics, Chemistry & Maths',
                'highlights': [
                    'Concept clarity with problem-solving techniques',
                    'Past-year paper practice and test series',
                    '4–6 sessions per week (2 hours each)'
                ],
                'image_url': 'https://images.unsplash.com/photo-1635070041078-e363dbe005cb?auto=format&fit=crop&w=1000&q=80',
                'color': 'from-violet-500 to-purple-600',
                'cta_p': '/courses/',
                'cta_p_text': 'Explore PCM Program',
                'category': 'INVENTOSHASTRA',
                'is_featured': True,
                'order': 4
            },
            {
                'badge': 'Grades 1 – 9',
                'title': 'INVENTOTHUNAI',
                'subtitle': 'All-Subject Tuition',
                'tagline': 'Learn Better. Score Higher.',
                'highlights': [
                    'Daily guided study sessions (2 hours)',
                    'Homework completion and doubt clearing',
                    'Weekly tests with parent reporting'
                ],
                'image_url': 'https://images.unsplash.com/photo-1503676260728-1c00da094a0b?auto=format&fit=crop&w=1000&q=80',
                'color': 'from-orange-500 to-amber-500',
                'cta_p': '/courses/',
                'cta_p_text': 'View Tuition Details',
                'category': 'INVENTOTHUNAI',
                'is_featured': True,
                'order': 5
            },
            {
                'badge': 'LKG – Grade 5',
                'title': 'INVENTOPHONICS',
                'subtitle': 'Early Reading Program',
                'tagline': 'Strong Phonics. Strong Readers.',
                'highlights': [
                    'Phonics, blends, and sight-word mastery',
                    'Structured reading pathways',
                    '1–2 classes per week (60 minutes)'
                ],
                'image_url': 'https://images.unsplash.com/photo-1503676260728-1c00da094a0b?auto=format&fit=crop&w=1000&q=80',
                'color': 'from-pink-500 to-rose-500',
                'cta_p': '/courses/',
                'cta_p_text': 'Start Reading Journey',
                'category': 'INVENTOPHONICS',
                'is_featured': True,
                'order': 6
            },
            {
                'badge': 'Grades 1 – 6',
                'title': 'INVENTOBEADS',
                'subtitle': 'Abacus & Mental Math',
                'tagline': 'Stronger Math. Smarter Minds.',
                'highlights': [
                    '8 progressive learning levels',
                    'Visualization-to-mental calculation training',
                    'Speed and accuracy improvement'
                ],
                'image_url': 'https://images.unsplash.com/photo-1596495578065-6e0763fa1178?auto=format&fit=crop&w=1000&q=80',
                'color': 'from-cyan-500 to-blue-500',
                'cta_p': '/courses/',
                'cta_p_text': 'Discover Abacus Program',
                'category': 'INVENTOBEADS',
                'is_featured': True,
                'order': 7
            },
            {
                'badge': 'Grades 1 – 8',
                'title': 'INVENTOWRITE',
                'subtitle': 'Handwriting & Speed Writing',
                'tagline': 'Beautiful Writing. Better Learning.',
                'highlights': [
                    'Letter formation to fluent writing',
                    'Writing speed improvement techniques',
                    '2 sessions per week (60 minutes)'
                ],
                'image_url': 'https://images.unsplash.com/photo-1455390582262-044cdead277a?auto=format&fit=crop&w=1000&q=80',
                'color': 'from-teal-500 to-emerald-500',
                'cta_p': '/courses/',
                'cta_p_text': 'Improve Handwriting',
                'category': 'INVENTOWRITE',
                'is_featured': True,
                'order': 8
            },
            {
                'badge': 'Grades 1 – 9',
                'title': 'INVENTOHINDI',
                'subtitle': 'Hindi Language Program',
                'tagline': 'Learn Hindi with Confidence',
                'highlights': [
                    'Reading, writing, grammar, and speaking',
                    'Worksheets and exam-focused practice',
                    'Strong comprehension development'
                ],
                'image_url': 'https://images.unsplash.com/photo-1456513080510-7bf3a84b82f8?auto=format&fit=crop&w=1000&q=80',
                'color': 'from-red-500 to-orange-500',
                'cta_p': '/courses/',
                'cta_p_text': 'Learn Hindi Now',
                'category': 'INVENTOHINDI',
                'is_featured': True,
                'order': 9
            }
        ]

        self.stdout.write("Migrating hero slider data...")
        
        # NOTE: In a real app we'd download the images. 
        # Here we'll just skip the actual image FileField download to avoid complexity
        # and assume the user can upload them in admin, 
        # OR we can just store the URL string if we changed the model to allow URL.
        # But the model has ImageField. 
        # For this demo, let's create the objects but leave image empty or use a placeholder if one exists.
        # Alternatively, we can assume the model has 'image' as ImageField.
        # We will skip image assignment for now to avoid IO errors, User can upload via admin.
        
        for item in courses_data:
            course, created = Course.objects.update_or_create(
                title=item['title'],
                defaults={
                    'category': item['category'],
                    'badge': item['badge'],
                    'subtitle': item['subtitle'],
                    'tagline': item.get('tagline'),
                    'description': item.get('description', item.get('tagline', '')), # Fallback description
                    'highlights': item.get('highlights', []),
                    'color_gradient': item['color'],
                    'image_url': item['image_url'],
                    'cta_primary_url': item['cta_p'],
                    'cta_primary_text': item['cta_p_text'],
                    'cta_secondary_url': item.get('cta_s'),
                    'cta_secondary_text': item.get('cta_s_text'),
                    'is_hero_featured': item['is_featured'],
                    'display_order': item['order'],
                    'price': 0 # Default price
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created: {item['title']}"))
            else:
                self.stdout.write(self.style.WARNING(f"Updated: {item['title']}"))
                
        self.stdout.write(self.style.SUCCESS("Migration complete! You may need to manually upload images via Admin."))

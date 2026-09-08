from django.urls import path
from .views import LoginView, CourseListView, CoursePlayerView, MarkLessonCompleteView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('courses/', CourseListView.as_view(), name='course-list'),
    
    # Course Player
    path('course/<int:course_id>/learn/', CoursePlayerView.as_view(), name='course_player'),
    path('lesson/<int:lesson_id>/complete/', MarkLessonCompleteView.as_view(), name='api_lesson_complete'),
]

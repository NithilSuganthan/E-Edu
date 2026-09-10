from django.urls import path
from . import views

app_name = 'parents'

urlpatterns = [
    path('login/', views.parent_login_view, name='login'),
    path('student/login/', views.student_login_view, name='student_login'),
    path('student/register/', views.student_register_view, name='student_register'),
    path('register/', views.parent_register_view, name='register'), # Changed from student/register to just /register (or parent/register)
    path('student/add/', views.add_student_view, name='add_student'),
    path('dashboard/', views.parent_dashboard_view, name='dashboard'),
    path('student/<int:student_id>/', views.student_detail_view, name='student_detail'),
    path('alert/<int:alert_id>/read/', views.mark_alert_read, name='mark_alert_read'),
    path('report/<int:report_id>/download/', views.download_report, name='download_report'),
    path('student/dashboard/', views.student_dashboard_view, name='student_dashboard'),
    path('student/courses/', views.student_courses_view, name='student_courses'),
    path('student/settings/', views.student_settings_view, name='student_settings'),
    path('student/settings/password/', views.student_change_password, name='student_change_password'),
    path('student/lab/', views.student_lab_view, name='student_lab'),
    path('student/enroll-now/<int:course_id>/', views.enroll_student, name='enroll_student'),
    path('student/certificates/', views.student_certificates_view, name='student_certificates'),
    path('student/browse-courses/', views.student_browse_courses_view, name='student_browse_courses'),
    path('student/enroll-core/<int:course_id>/', views.enroll_student_core, name='enroll_student_core'),
    path('student/enroll-core/<int:course_id>/confirm/', views.enroll_student_core_confirm, name='enroll_student_core_confirm'),
    path('student/enroll-core/<int:course_id>/payment/', views.enroll_student_core_payment, name='enroll_student_core_payment'),
    path('student/payment/success/', views.razorpay_success_callback, name='razorpay_success_callback'),
    path('logout/', views.parent_logout_view, name='logout'),
    path('student/logout/', views.student_logout_view, name='student_logout'),
]

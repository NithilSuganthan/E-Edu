from django.urls import path
from . import views

app_name = 'certifications'

urlpatterns = [
    path('', views.index, name='index'),
    path('verify/', views.verify_certificate, name='verify_certificate'),
    path('result/<str:id>/', views.certificate_result, name='result'),
]

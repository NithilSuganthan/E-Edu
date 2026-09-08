"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView, RedirectView
from core import views as core_views

import os

from django.contrib.auth import views as auth_views

admin_url = os.getenv('ADMIN_URL', 'admin/')

urlpatterns = [
    # Custom Admin Logout Override
    path(f'{admin_url}logout/', auth_views.LogoutView.as_view(template_name='admin/logout.html'), name='logout'),
    
    path(admin_url, admin.site.urls),
    path('api/', include('core.urls')),
    path('certifications/', include('certifications.urls')),
    path('cert/', RedirectView.as_view(url='/certifications/', permanent=False)),
    path('parents/', include('parents.urls')),
    path('accounts/', include('allauth.urls')),
    # Serve static templates via Django
    path('', core_views.HomeView.as_view(), name='home'),
    path('index/', TemplateView.as_view(template_name='index.html')),
    path('courses/', TemplateView.as_view(template_name='courses.html')),
    path('lab/', TemplateView.as_view(template_name='lab.html')),
    path('about/', TemplateView.as_view(template_name='about.html')),
    path('parent/', RedirectView.as_view(url='/parents/login/', permanent=False)),
    path('parent-dashboard/', RedirectView.as_view(url='/parents/dashboard/', permanent=False)),
    path('robotics/', TemplateView.as_view(template_name='robotics.html')),
    path('coding/', TemplateView.as_view(template_name='coding.html')),
]

from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve as static_serve

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # Serve js folder from parent directory
    urlpatterns += static('/js/', document_root=settings.BASE_DIR.parent / 'js')
    # Serve static files from parent directory  
    urlpatterns += static('/static/', document_root=settings.BASE_DIR / 'static')
else:
    # Temporary-demo media serving when DEBUG=False (no external object storage).
    # NOTE: fine for a short public review; use S3/equivalent for long-term production.
    urlpatterns += [
        path('media/<path:path>', static_serve, {'document_root': settings.MEDIA_ROOT}),
    ]

# Admin Site Customization
admin.site.site_header = "Inventobots Academy Admin"
admin.site.site_title = "Inventobots Admin Portal"
admin.site.index_title = "Welcome to Inventobots Academy Portal"

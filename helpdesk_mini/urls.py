"""
URL configuration for helpdesk_mini project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.views.static import serve
from django.conf import settings
from django.conf.urls.static import static

from core import views_misc

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('', include('tickets.urls_frontend')),
    path('', include('accounts.urls_frontend')),

    # API health and Meta
    path('api/health/', views_misc.health_check, name='health_check'),
    path('api/_meta/', views_misc.meta_info, name='meta_info'),

    # Serve hackathon metadata
    path('.well-known/hackathon.json', serve, {
      'path': '.well-known/hackathon.json',
      'document_root': settings.BASE_DIR / 'static'
    }),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

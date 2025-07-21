"""
URL configuration for recipes project.

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
from django.conf import settings
from django.conf.urls.static import static
from vege import views as vege_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('recipes1/', vege_views.recipes, name='recipes'),  # This maps the root URL to the recipes view
    path('recipes1/delete/<int:receipe_id>/', vege_views.delete_receipe, name='delete_receipe'),
    path('recipes1/edit/<int:receipe_id>/', vege_views.edit_receipe, name='edit_receipe'),
    path('', include('food2.urls')),  # This includes all food app URLs
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
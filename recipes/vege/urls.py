# vege/urls.py
from django.urls import path
from . import views

app_name = 'vege'  # Add this line for namespace

urlpatterns = [
    path('', views.home, name='home'),
    path('categories/', views.categories, name='categories'),
    path('contact/', views.contact, name='contact'),
    path('recipes/', views.recipes, name='recipes'),
    path('delete-receipe/<int:receipe_id>/', views.delete_receipe, name='delete_receipe'),
    path('edit-receipe/<int:receipe_id>/', views.edit_receipe, name='edit_receipe'),
]
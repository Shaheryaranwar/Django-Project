from django.urls import path
from . import views

urlpatterns = [
    path('', views.recipes, name='recipes'),
    path('delete-receipe/<int:receipe_id>/', views.delete_receipe, name='delete_receipe'),
    path('edit-receipe/<int:receipe_id>/', views.edit_receipe, name='edit_receipe'),
]
# vege/urls.py
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views 
from django.conf import settings
from django.conf.urls.static import static

from vege import views as vege_views


app_name = 'vege'  # Add this line for namespace

urlpatterns = [
    path('', views.home, name='home'),
    path('categories/', views.categories, name='categories'),
    path('contact/', views.contact, name='contact'),
    path('recipes/', views.recipes, name='recipes'),
    path('delete-receipe/<int:receipe_id>/', views.delete_receipe, name='delete_receipe'),
    path('edit-receipe/<int:receipe_id>/', views.edit_receipe, name='edit_receipe'),
    path('login/', views.login_page, name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='vege:login'), name='logout'),
    path('register/', views.register, name='register'),  # Requires a view function
    path('password-reset/', 
         auth_views.PasswordResetView.as_view(template_name='vege/password_reset.html'), 
         name='password_reset'),

    path('password-reset/done/', 
         auth_views.PasswordResetDoneView.as_view(template_name='vege/password_reset_done.html'), 
         name='password_reset_done'),

    path('reset/<uidb64>/<token>/', 
         auth_views.PasswordResetConfirmView.as_view(template_name='vege/password_reset_confirm.html'), 
         name='password_reset_confirm'),

    path('reset/done/', 
         auth_views.PasswordResetCompleteView.as_view(template_name='vege/password_reset_complete.html'), 
         name='password_reset_complete'),
     path('recipe/<int:id>/', views.recipe_detail, name='recipe_detail'),
     path('students/', views.get_students, name='students'),  # New URL pattern for students view
     path("students/add/", views.student_add, name="student_add"),
     path("students/edit/<int:id>/", views.student_edit, name="student_edit"),
     path("students/delete/<int:id>/", views.student_delete, name="student_delete"),
     # path('see_marks/', views.see_marks_list, name="see_marks_list"),
     path('see_marks/<student_id>/', views.see_marks, name="see_marks"),
]
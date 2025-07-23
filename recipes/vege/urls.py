# vege/urls.py
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views 

app_name = 'vege'  # Add this line for namespace

urlpatterns = [
    path('', views.home, name='home'),
    path('categories/', views.categories, name='categories'),
    path('contact/', views.contact, name='contact'),
    path('recipes/', views.recipes, name='recipes'),
    path('delete-receipe/<int:receipe_id>/', views.delete_receipe, name='delete_receipe'),
    path('edit-receipe/<int:receipe_id>/', views.edit_receipe, name='edit_receipe'),
    path('login/', views.login_page, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
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
]
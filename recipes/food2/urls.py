from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('demo/', views.demo, name='demo'),
    path('home/', views.home_view, name='home'),
    path('login/', views.login_view, name='login'),
    path('menu/', views.menu, name='menu'),
    path('register/', views.register_view, name='register'),
    path('categories/', views.categories, name='categories'),
]
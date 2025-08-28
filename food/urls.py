# from django.urls import path
# from . import views

# urlpatterns = [
#     path('food/', views.food_list, name='food_list'),
    
# ]
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('recipes/', views.recipe_list, name='recipes'),
    path('categories/', views.category_list, name='categories'),
    path('category/<slug:slug>/', views.category_recipes, name='category_recipes'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('contact/success/', views.contact_success, name='contact_success'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),]
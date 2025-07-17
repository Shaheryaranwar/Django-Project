
# # Create your views here.
# from .models import Recipe
# from django.shortcuts import render
# from django.shortcuts import render, redirect
# from django.contrib.auth import login, authenticate, logout
# from django.contrib import messages
# from .forms import RegisterForm, LoginForm
# from django.contrib.auth.decorators import login_required
# from .models import Recipe
# from django.http import HttpResponse
# from django.template import loader
# # Create your views here.
# def menu_view(request):
#     peoples = [
#                {'name': 'Ladyfinger', 'expirey':'30 days', 'price':'$2.00'},
#                {'name': 'Onion', 'expirey':'30 days', 'price':'$2.80'},
#                {'name': 'Redchili', 'expirey':'90 days', 'price':'$4.50'}


#                ]
#     return render(request, 'food2/index.html', {'peoples': peoples})
# def index(request):
#     return render(request, 'food2/index.html')

# def about(request):
#     return render(request, 'food2/about.html')

# def contact(request):
#     return render(request, 'food2/contact.html')

# def menu(request):
#     return render(request, 'food2/menu.html')

# def recipes(request):
#     return render(request, 'food2/recipes.html')

# @login_required
# def home_view(request):
#     if request.user.is_authenticated:
#         user_recipes = Recipe.objects.filter(user=request.user)
#     else:
#         user_recipes = None
#     return render(request, 'food2/home.html', {'recipes': user_recipes})
# def register_view(request):
#     if request.method == 'POST':
#         form = RegisterForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             login(request, user)
#             messages.success(request, 'Registration successful.')
#             return redirect('home')  # change 'home' to your desired redirect URL
#         messages.error(request, 'Unsuccessful registration. Invalid information.')
#     else:
#         form = RegisterForm()
#     return render(request, 'accounts/register.html', {'form': form})

# def login_view(request):
#     if request.method == 'POST':
#         form = LoginForm(request, data=request.POST)
#         if form.is_valid():
#             username = form.cleaned_data.get('username')
#             password = form.cleaned_data.get('password')
#             user = authenticate(username=username, password=password)
#             if user is not None:
#                 login(request, user)
#                 messages.info(request, f'You are now logged in as {username}.')
#                 return redirect('home')  # change 'home' to your desired redirect URL
#         messages.error(request, 'Invalid username or password.')
#     else:
#         form = LoginForm()
#     return render(request, 'accounts/login.html', {'form': form})

# def logout_view(request):
#     logout(request)
#     messages.info(request, 'You have successfully logged out.')
#     return redirect('home')  # change 'home' to your desired redirect URL
# @login_required
# def create_recipe(request):
#     # Only logged-in users can access this view
#     return render(request, 'food2/create_recipe.html')
# def demo(request):
#     return render(request, 'food2/demo.html')
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Recipe

def index(request):
    return render(request, 'food2/index.html')

def about(request):
    return render(request, 'food2/about.html')

def contact(request):
    return render(request, 'food2/contact.html')

def demo(request):
    return render(request, 'food2/demo.html')
def categories(request):
    context = {
        'range_10': range(1, 11)
    }
    return render(request, 'food2/categories.html', context)

@login_required
def home_view(request):
    user_recipes = Recipe.objects.filter(user=request.user) if request.user.is_authenticated else None
    return render(request, 'food2/home.html', {'recipes': user_recipes})

def login_view(request):
    return render(request, 'food2/login.html')

def menu(request):
    return render(request, 'food2/menu.html')

def register_view(request):
    return render(request, 'food2/register.html')

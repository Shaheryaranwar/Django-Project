# from django.shortcuts import render
# from django.http import HttpResponse
# from django.template import loader
# # Create your views here.
# def food_list(request):
#     # This is a placeholder for the food list view
#     # template = loader.get_template('index.html')
#     # return HttpResponse("template.render()")
#     peoples = [
#                {'name': 'ladyfinger', 'expirey':'30 days', 'price':'$2.00'},
#                {'name': 'Onion', 'expirey':'30 days', 'price':'$2.80'},
#                {'name': 'Redchili', 'expirey':'90 days', 'price':'$4.50'}


#                ]
#     return render(request, 'food/index.html')
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import Recipe, Category, Contact, Profile
from .forms import UserRegisterForm, ContactForm

def home(request):
    featured_categories = Category.objects.all()[:4]
    popular_recipes = Recipe.objects.order_by('-rating')[:3]
    return render(request, 'food/base.html', {
        'featured_categories': featured_categories,
        'popular_recipes': popular_recipes
    })

def recipe_list(request):
    recipes = Recipe.objects.all().order_by('-created_at')
    paginator = Paginator(recipes, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'food/recipes.html', {'recipes': page_obj})

def category_list(request):
    categories = Category.objects.all()
    return render(request, 'food/categories.html', {'categories': categories})

def category_recipes(request, slug):
    category = get_object_or_404(Category, slug=slug)
    recipes = Recipe.objects.filter(category=category)
    return render(request, 'food/recipes.html', {
        'recipes': recipes,
        'category': category
    })

def about(request):
    team = [
        {'name': 'John Doe', 'position': 'Founder & CEO', 'image': 'team/john.jpg'},
        {'name': 'Jane Smith', 'position': 'Head Chef', 'image': 'team/jane.jpg'},
        {'name': 'Mike Johnson', 'position': 'Marketing Director', 'image': 'team/mike.jpg'},
    ]
    return render(request, 'food/about.html', {'team': team})

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('contact_success')
    else:
        form = ContactForm()
    return render(request, 'food/contact.html', {'form': form})

def contact_success(request):
    return render(request, 'food/contact_success.html')

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user)
            login(request, user)
            return redirect('home')
    else:
        form = UserRegisterForm()
    return render(request, 'food/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'food/login.html', {'error': 'Invalid credentials'})
    return render(request, 'food/login.html')

@login_required
def user_logout(request):
    logout(request)
    return redirect('home')
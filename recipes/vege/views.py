from django.shortcuts import render, redirect, get_object_or_404
from .models import Receipe, Category
from .forms import ContactForm
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login 

def recipes(request):
    if request.method == 'POST':
        receipe_name = request.POST.get('recipe_name')
        receipe_description = request.POST.get('description')
        ingredients = request.POST.get('ingredients')
        instructions = request.POST.get('instructions')
        created_at = request.POST.get('created_at')
        receipe_image = request.FILES.get('image')

        Receipe.objects.create(
            receipe_name=receipe_name,
            receipe_description=receipe_description,
            ingredients=ingredients,
            instructions=instructions,
            created_at=created_at,
            receipe_image=receipe_image
        )

        return redirect('vege:recipes')

    receipes = Receipe.objects.all().order_by('id')
    return render(request, 'vege/recipes.html', {'receipes': receipes})

def delete_receipe(request, receipe_id):
    try:
        receipe = Receipe.objects.get(id=receipe_id)
        receipe.delete()
    except Receipe.DoesNotExist:
        pass

    return redirect('vege:recipes')

def edit_receipe(request, receipe_id):
    receipe = get_object_or_404(Receipe, id=receipe_id)
    
    if request.method == 'POST':
        receipe.receipe_name = request.POST.get('recipe_name')
        receipe.receipe_description = request.POST.get('description')
        receipe.ingredients = request.POST.get('ingredients')
        receipe.instructions = request.POST.get('instructions')
        receipe.created_at = request.POST.get('created_at')
        
        # Only update image if a new one was provided
        if 'image' in request.FILES:
            receipe.receipe_image = request.FILES['image']
        
        receipe.save()
        return redirect('vege:recipes')
    
    # For GET request, show the edit form
    return render(request, 'vege/edit_receipe.html', {'receipe': receipe})

def home(request):
    recipes = Receipe.objects.all().order_by('-created_at')[:12]
    return render(request, 'vege/home.html', {'recipes': recipes})

def categories(request):
    categories = Category.objects.all()
    return render(request, 'vege/categories.html', {'categories': categories})

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('vege:home')
    else:
        form = ContactForm()
    return render(request, 'vege/contact.html', {'form': form})

# def register(request):
#     if request.method == 'POST':
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             form.save()
#             username = form.cleaned_data.get('username')
#             messages.success(request, f'Account created for {username}! You can now log in.')
#             return redirect('vege:login')  # Redirect to login page
#     else:
#         form = UserCreationForm()
#     return render(request, 'vege/register.html', {'form': form})
def login_page(request):
    if request.method == 'POST':
        login_input = request.POST.get('username')  # username or email
        password = request.POST.get('password')

        user_obj = None

        # Try to find user by email if input is email
        if User.objects.filter(email=login_input).exists():
            user_obj = User.objects.get(email=login_input)
        elif User.objects.filter(username=login_input).exists():
            user_obj = User.objects.get(username=login_input)
        else:
            messages.error(request, "Invalid username or email.")
            return redirect("vege:login")

        # Now authenticate using username and password
        user = authenticate(request, username=user_obj.username, password=password)

        if user is None:
            messages.error(request, "Invalid password.")
            return redirect('vege:login')
        else:
            login(request, user)
            return redirect('vege:recipes1')
        if request.path.startswith('/recipes1'):
            return redirect('vege:recipes1')
        else:
            return redirect('home')

    return render(request, 'vege/login.html')


def register(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = User.objects.filter(username=username)
        if user.exists():
            messages.error(request, "Username already exists. Please choose a different username.")

            return redirect("vege/register.html")
        
        # Create a new user instance

        user = User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=email
            
        )
        user.set_password(password)#password hashing
        user.save()

        # Here you would typically create a user object and save it
        # For simplicity, we are not implementing user creation logic
        messages.success(request, "Registration successful! You can now log in.")

        return redirect('vege:login')  # Redirect to login page after registration
    return render(request, 'vege/register.html')

def food_index(request):
    return render(request, 'vege/recipes.html')
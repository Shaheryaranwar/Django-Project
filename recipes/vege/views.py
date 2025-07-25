from django.shortcuts import render, redirect, get_object_or_404
from .models import Receipe, Category
from .forms import ContactForm
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout 
from django.contrib.auth.decorators import login_required

@login_required(login_url='vege:login')
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

@login_required(login_url='vege:login')
def recipe_detail(request, id):
    recipe = get_object_or_404(Receipe, id=id)
    return render(request, 'vege/recipe_detail.html', {'recipe': recipe})

@login_required(login_url='vege:login')
def delete_receipe(request, receipe_id):
    try:
        receipe = Receipe.objects.get(id=receipe_id)
        receipe.delete()
    except Receipe.DoesNotExist:
        pass

    return redirect('vege:recipes')

@login_required(login_url='vege:login')
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

@login_required(login_url='vege:login')
def home(request):
    recipes = Receipe.objects.all().order_by('-created_at')[:12]
    return render(request, 'vege/home.html', {'recipes': recipes})

@login_required(login_url='vege:login')
def categories(request):
    categories = Category.objects.all()
    return render(request, 'vege/categories.html', {'categories': categories})

@login_required(login_url='vege:login')
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
        username_or_email = request.POST.get('username')
        password = request.POST.get('password')

        # Check if user exists with this username or email
        user_by_username = User.objects.filter(username=username_or_email).first()
        user_by_email = User.objects.filter(email=username_or_email).first()

        user = None
        if user_by_username:
            user = authenticate(request, username=user_by_username.username, password=password)
        elif user_by_email:
            user = authenticate(request, username=user_by_email.username, password=password)

        if user is not None:
            login(request, user)
            return redirect('vege:home')  # or redirect dynamically
        else:
            # Error messages
            if not user_by_username and not user_by_email:
                messages.error(request, "Invalid username or email.")
            else:
                messages.error(request, "Invalid password.")

    return render(request, 'vege/login.html')  # your login template

         
        


        
        # Here you would typically authenticate the user
        # For simplicity, we are not implementing authentication logic
        
    return render(request, 'vege/login.html')


def register(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        username_exists = User.objects.filter(username=username).exists()
        email_exists = User.objects.filter(email=email).exists()

        if username_exists and email_exists:
            messages.error(request, "Username and Email already exist. Please choose different ones.")
            return render(request, "vege/register.html")
        elif username_exists:
            messages.error(request, "Username already exists. Please choose a different one.")
            return render(request, "vege/register.html")
        elif email_exists:
            messages.error(request, "Email already exists. Please choose a different one.")
            return render(request, "vege/register.html")

        # Create new user
        user = User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=email,
        )
        user.set_password(password)
        user.save()

        messages.success(request, "Registration successful! You can now log in.")
        return redirect('vege:login')

    return render(request, 'vege/register.html')

def logout_view(request):
    logout(request)
    return redirect('vege:login')  # Redirect to home or any other page after logout
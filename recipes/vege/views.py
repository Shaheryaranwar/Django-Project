from django.shortcuts import render, redirect, get_object_or_404
from .models import Receipe, Category
from .forms import ContactForm
from django.http import HttpResponse

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
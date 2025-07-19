from django.shortcuts import render, redirect
from .models import Receipe
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

        return redirect('recipes')  # Redirect to avoid form resubmission on refresh

    # Fetch all recipes to display
    receipes = Receipe.objects.all().order_by('-created_at')

    return render(request, 'vege/recipes.html', {'receipes': receipes})

def delete_receipe(request, receipe_id):
    try:
        receipe = Receipe.objects.get(id=receipe_id)
        receipe.delete()
    except Receipe.DoesNotExist:
        pass  # Handle the case where the recipe does not exist

    return redirect('recipes')  # Redirect to the recipes page after deletion
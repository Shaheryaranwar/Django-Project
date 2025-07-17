from django.core.management.base import BaseCommand
from food.models import Category, Recipe, User, Profile
import random

class Command(BaseCommand):
    help = 'Populates the database with sample data'
    
    def handle(self, *args, **options):
        # Create categories
        categories = [
            'Breakfast', 'Lunch', 'Dinner', 'Desserts', 
            'Vegetarian', 'Vegan', 'Gluten-Free', 'Keto'
        ]
        
        for name in categories:
            Category.objects.create(
                name=name,
                description=f"Delicious {name} recipes",
                image=f"categories/{name.lower()}.jpg"
            )
        
        # Create some users
        users = []
        for i in range(1, 6):
            user = User.objects.create_user(
                username=f'user{i}',
                email=f'user{i}@example.com',
                password='testpass123'
            )
            Profile.objects.create(
                user=user,
                title=['Home Cook', 'Food Blogger', 'Professional Chef'][random.randint(0, 2)]
            )
            users.append(user)
        
        # Create recipes
        recipe_titles = [
            'Avocado Toast', 'Pancakes', 'Omelette', 
            'Caesar Salad', 'Pasta Carbonara', 'Beef Steak',
            'Chocolate Cake', 'Tiramisu', 'Fruit Salad'
        ]
        
        for title in recipe_titles:
            Recipe.objects.create(
                title=title,
                author=random.choice(users),
                category=random.choice(Category.objects.all()),
                image=f"recipes/{title.lower().replace(' ', '_')}.jpg",
                prep_time=random.randint(5, 30),
                cook_time=random.randint(10, 60),
                servings=random.randint(1, 8),
                calories=random.randint(200, 800),
                ingredients="\n".join([f"- Ingredient {i}" for i in range(1, 6)]),
                instructions="\n".join([f"Step {i}: Do something" for i in range(1, 6)]),
                rating=random.uniform(3, 5),
                review_count=random.randint(5, 100)
            )
        
        self.stdout.write(self.style.SUCCESS('Successfully populated the database'))
import os
import tempfile
import requests
from django.core.files import File
from django.core.management.base import BaseCommand
from faker import Faker
from vege.models import Receipe, Category
from django.contrib.auth.models import User
import random

fake = Faker()

class Command(BaseCommand):
    help = "Generate fake recipe data with images"

    def handle(self, *args, **kwargs):
        NUM_RECIPES = 20  # change as needed

        users = list(User.objects.all())
        categories = list(Category.objects.all())

        for _ in range(NUM_RECIPES):
            name = fake.sentence(nb_words=3)
            description = fake.paragraph(nb_sentences=2)
            ingredients = ', '.join(fake.words(nb=5))
            instructions = fake.paragraph(nb_sentences=4)
            image_url = f"https://picsum.photos/seed/{fake.uuid4()}/400/300"

            # Download image to a temporary file
            response = requests.get(image_url)
            tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".jpg")
            tmp_file.write(response.content)
            tmp_file.flush()
            tmp_file.close()  # ✅ Important to close before re-opening on Windows

            recipe = Receipe.objects.create(
                receipe_name=name,
                receipe_description=description,
                ingredients=ingredients,
                instructions=instructions,
                recipe_view_count=random.randint(1, 100),
                user=random.choice(users) if users else None
            )

            # Attach image
            with open(tmp_file.name, 'rb') as f:
                recipe.receipe_image.save(f"{name.replace(' ', '_')}.jpg", File(f), save=True)

            # Assign random categories
            if categories:
                recipe.categories.set(random.sample(categories, k=min(2, len(categories))))

            os.unlink(tmp_file.name)  # ✅ Now safe to delete
            self.stdout.write(self.style.SUCCESS(f"Created recipe: {recipe.receipe_name}"))

        self.stdout.write(self.style.SUCCESS("✅ Done creating fake recipes"))

from django.db import models

# Create your models here.
class Recipes(models.Model):
    recipe_name = models.CharField(max_length=255)
    recipe_description = models.TextField()
    recipe_ingredients = models.TextField()
    recipe_instructions = models.TextField()
    recipe_image = models.ImageField(upload_to='recipes/images/')
    recipe_prep_time = models.IntegerField()  # in minutes
    recipe_cook_time = models.IntegerField()  # in minutes

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Recipes"
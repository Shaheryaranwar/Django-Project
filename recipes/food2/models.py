from django.db import models

class Recipe(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=300)
    ngredients = models.TextField(max_length=300, default='')  # Add default
    instructions = models.TextField(max_length=300, default='')  # Add default
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
class Car(models.Model):
    car_name = models.CharField(max_length=100)
    car_speed = models.IntegerField(default=60)  # Fixed typo here
    car_color = models.CharField(max_length=20)
    car_model = models.IntegerField()
    car_brand = models.CharField(max_length=50, default='Unknown')  # Changed to CharField and fixed typo

    def __str__(self):
        return self.car_name  # Make sure to return the car_name
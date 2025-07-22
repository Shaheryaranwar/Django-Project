from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='categories/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']

    def __str__(self):
        return self.name

class Receipe(models.Model):
    MEAL_TYPES = [
        ('breakfast', 'Breakfast'),
        ('lunch', 'Lunch'),
        ('dinner', 'Dinner'),
        ('dessert', 'Dessert'),
        ('snack', 'Snack'),
    ]

    receipe_name = models.CharField(max_length=100)
    receipe_description = models.TextField()
    ingredients = models.TextField()
    instructions = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    receipe_image = models.ImageField(upload_to='receipes/', null=True, blank=True)
    categories = models.ManyToManyField(Category, related_name='recipes', blank=True)
    meal_type = models.CharField(max_length=20, choices=MEAL_TYPES, default='lunch')
    prep_time = models.PositiveIntegerField(help_text="Preparation time in minutes", null=True, blank=True)
    cook_time = models.PositiveIntegerField(help_text="Cooking time in minutes", null=True, blank=True)
    servings = models.PositiveIntegerField(null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.receipe_name

    def average_rating(self):
        return self.ratings.aggregate(models.Avg('score'))['score__avg'] or 0

class Rating(models.Model):
    receipe = models.ForeignKey(Receipe, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    review = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['receipe', 'user']
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.score}/5 by {self.user.username} for {self.receipe.receipe_name}"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profiles/', null=True, blank=True)
    website = models.URLField(blank=True)
    location = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.user.username
from django.contrib import admin
from .models import Receipe, Category, Rating, UserProfile

admin.site.register(Receipe)
admin.site.register(Category)
admin.site.register(Rating)
admin.site.register(UserProfile)
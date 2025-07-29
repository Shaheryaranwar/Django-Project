from django.contrib import admin
from .models import (
    Category, Receipe, Rating,
    UserProfile, Department, StudentID, Student
)

admin.site.register(Category)
admin.site.register(Receipe)
admin.site.register(Rating)
admin.site.register(UserProfile)
admin.site.register(Department)
admin.site.register(StudentID)
admin.site.register(Student)
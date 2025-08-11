from django.contrib import admin
from .models import *


admin.site.register(Category)
admin.site.register(Receipe)
admin.site.register(Rating)
admin.site.register(UserProfile)
admin.site.register(Department)
admin.site.register(StudentID)
admin.site.register(Student)
admin.site.register(Subject)
class SubjectsMarksAdmin(admin.ModelAdmin):
    list_display = ('student', 'subject', 'marks')
    
admin.site.register(SubjectsMarks,SubjectsMarksAdmin)    # Assuming Subject model is also defined in models.py

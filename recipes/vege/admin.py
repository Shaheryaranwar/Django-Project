# from django.contrib import admin
# from .models import *


# admin.site.register(Category)
# admin.site.register(Receipe)
# admin.site.register(Rating)
# admin.site.register(UserProfile)
# admin.site.register(Department)
# admin.site.register(StudentID)
# admin.site.register(Student)
# admin.site.register(Subject)
# class SubjectsMarksAdmin(admin.ModelAdmin):
#     list_display = ('student', 'subject', 'marks')
    
# admin.site.register(SubjectsMarks,SubjectsMarksAdmin)    # Assuming Subject model is also defined in models.py

from django.contrib import admin
from .models import *

admin.site.register(Category)
admin.site.register(Receipe)
admin.site.register(Rating)
admin.site.register(UserProfile)
admin.site.register(Department)
admin.site.register(StudentID)
admin.site.register(Subject)
class SubjectsMarksAdmin(admin.ModelAdmin):
    list_display = ('student', 'subject', 'marks')
    
admin.site.register(SubjectsMarks,SubjectsMarksAdmin)    # Assuming Subject model is also defined in models.py

# Inline for SubjectsMarks inside Student admin
class SubjectsMarksInline(admin.TabularInline):  # or admin.StackedInline
    model = SubjectsMarks
    extra = 1  # show 1 empty row for adding new marks
    fields = ('subject', 'marks')  # only show subject & marks in inline


class StudentAdmin(admin.ModelAdmin):
    list_display = ('student_name', 'student_email', 'student_phone', 'department')
    inlines = [SubjectsMarksInline]  # attach inline to Student


admin.site.register(Student, StudentAdmin)

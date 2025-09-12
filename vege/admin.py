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
from django.db.models import Sum
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

class ReportCardAdmin(admin.ModelAdmin):
    list_display = ('student', 'student_rank','date_reportcard_issued','total_marks')  # Customize as needed
    ordering = ['-student_rank']  # Order by rank descending

    def total_marks(self, obj):
        subject_marks = SubjectsMarks.objects.filter(student=obj.student)
        return subject_marks.aggregate(marks=Sum('marks'))['marks'] or 0
        
admin.site.register(ReportCard , ReportCardAdmin)  # Register ReportCard model

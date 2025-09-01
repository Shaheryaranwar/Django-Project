from django import forms
from .models import Student

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    subject = forms.CharField(max_length=200)
    message = forms.CharField(widget=forms.Textarea)
class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ["student_id", "student_name", "student_email", "student_image", "student_age", "department"]
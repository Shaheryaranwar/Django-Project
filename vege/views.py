from django.shortcuts import render, redirect, get_object_or_404
from .models import Receipe, Category, Student, Department, StudentID, Subject, SubjectsMarks
from django.core.paginator import Paginator
from .forms import ContactForm , StudentForm
from django.http import HttpResponse
# from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout 
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.db.models import Avg, Max, Min, Count
from django.db.models import Q, Sum 
# from django.contrib.auth.models import User
from.utils import send_email_to_client, email_with_attachment
from django.contrib.auth import get_user_model
from django.conf import settings
from django.shortcuts import redirect
from django.conf import settings
from .utils import email_with_attachment
User = get_user_model()
# from .seed import genrate_report_card, seed_db


def send_email(request):
    try:
        subject = "This is a test email sent from Django Application Server with Attachment."
        message = "Hi Please Find Attached File With Email."
        recipient_list = ['shaheryaranwar14@gmail.com']
        file_path = f"{settings.BASE_DIR}/static/images/recipe3.jpg"
        
        # Check if file exists
        import os
        if not os.path.exists(file_path):
            return redirect('/?error=File not found')
        
        success = email_with_attachment(subject, message, recipient_list, file_path)
        
        if success:
            return redirect('/?success=Email sent successfully!')
        else:
            return redirect('/?error=Failed to send email')
            
    except Exception as e:
        return redirect(f'/?error={str(e)}')
    
    
@login_required(login_url='vege:login')
def recipes(request):
    if request.method == 'POST':
        receipe_name = request.POST.get('recipe_name')
        receipe_description = request.POST.get('description')
        ingredients = request.POST.get('ingredients')
        instructions = request.POST.get('instructions')
        created_at = request.POST.get('created_at')
        receipe_image = request.FILES.get('image')

        Receipe.objects.create(
            receipe_name=receipe_name,
            receipe_description=receipe_description,
            ingredients=ingredients,
            instructions=instructions,
            created_at=created_at,
            receipe_image=receipe_image
        )

        return redirect('vege:recipes')

    receipes = Receipe.objects.all().order_by('id')
    return render(request, 'vege/recipes.html', {'receipes': receipes})

@login_required(login_url='vege:login')
def recipe_detail(request, id):
    recipe = get_object_or_404(Receipe, id=id)
    return render(request, 'vege/recipe_detail.html', {'recipe': recipe})

@login_required(login_url='vege:login')
def delete_receipe(request, receipe_id):
    try:
        receipe = Receipe.objects.get(id=receipe_id)
        receipe.delete()
    except Receipe.DoesNotExist:
        pass

    return redirect('vege:recipes')

@login_required(login_url='vege:login')
def edit_receipe(request, slug):
    receipe = get_object_or_404(Receipe, slugs=slug) 
    
    if request.method == 'POST':
        receipe.receipe_name = request.POST.get('recipe_name')
        receipe.receipe_description = request.POST.get('description')
        receipe.ingredients = request.POST.get('ingredients')
        receipe.instructions = request.POST.get('instructions')
        receipe.created_at = request.POST.get('created_at')
        
        # Only update image if a new one was provided
        if 'image' in request.FILES:
            receipe.receipe_image = request.FILES['image']
        
        receipe.save()
        return redirect('vege:recipes')
    
    # For GET request, show the edit form
    return render(request, 'vege/edit_receipe.html', {'receipe': receipe})

@login_required(login_url='vege:login')
def home(request):
    recipes = Receipe.objects.all().order_by('-created_at')[:12]
    return render(request, 'vege/home.html', {'recipes': recipes})

@login_required(login_url='vege:login')
def categories(request):
    categories = Category.objects.all()
    return render(request, 'vege/categories.html', {'categories': categories})

@login_required(login_url='vege:login')
def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('vege:home')
    else:
        form = ContactForm()
    return render(request, 'vege/contact.html', {'form': form})

# def register(request):
#     if request.method == 'POST':
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             form.save()
#             username = form.cleaned_data.get('username')
#             messages.success(request, f'Account created for {username}! You can now log in.')
#             return redirect('vege:login')  # Redirect to login page
#     else:
#         form = UserCreationForm()
#     return render(request, 'vege/register.html', {'form': form})


def login_page(request):
    if request.method == 'POST':
        username_or_email = request.POST.get('username')
        password = request.POST.get('password')

        # Check if user exists with this username or email
        user_by_username = User.objects.filter(username=username_or_email).first()
        user_by_email = User.objects.filter(email=username_or_email).first()

        user = None
        if user_by_username:
            user = authenticate(request, username=user_by_username.username, password=password)
        elif user_by_email:
            user = authenticate(request, username=user_by_email.username, password=password)

        if user is not None:
            login(request, user)
            return redirect('vege:home')  # or redirect dynamically
        else:
            # Error messages
            if not user_by_username and not user_by_email:
                messages.error(request, "Invalid username or email.")
            else:
                messages.error(request, "Invalid password.")

    return render(request, 'vege/login.html')  # your login template

         
        


        
        # Here you would typically authenticate the user
        # For simplicity, we are not implementing authentication logic
        
    return render(request, 'vege/login.html')


def register(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        username_exists = User.objects.filter(username=username).exists()
        email_exists = User.objects.filter(email=email).exists()

        if username_exists and email_exists:
            messages.error(request, "Username and Email already exist. Please choose different ones.")
            return render(request, "vege/register.html")
        elif username_exists:
            messages.error(request, "Username already exists. Please choose a different one.")
            return render(request, "vege/register.html")
        elif email_exists:
            messages.error(request, "Email already exists. Please choose a different one.")
            return render(request, "vege/register.html")

        # Create new user
        user = User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=email,
        )
        user.set_password(password)
        user.save()

        messages.success(request, "Registration successful! You can now log in.")
        return redirect('vege:login')

    return render(request, 'vege/register.html')

def logout_view(request):
    logout(request)
    return redirect('vege:login')  # Redirect to home or any other page after logout

def get_students(request):
    query = request.GET.get("q", "")
    students = Student.objects.all().order_by("student_name")

    if query:
        students = students.filter(
            Q(student_name__icontains=query) |   # ✅ use correct field
            Q(student_email__icontains=query) |
            Q(student_id__student_id__icontains=query) |
            Q(department__department__icontains=query) |
            Q(student_age__iexact=query)        # ✅ safer for text input
        )

    paginator = Paginator(students, 25)
    page_number = request.GET.get("page") 
    page_obj = paginator.get_page(page_number)

    return render(request, "vege/students.html", {
        "page_obj": page_obj,
        "query": query
    })

def student_add(request):
    if request.method == "POST":
        form = StudentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("vege:students")   # <- namespaced URL
    else:
        form = StudentForm()
    return render(request, "vege/student_form.html", {"form": form, "title": "Add Student"})


def student_edit(request, id):
    student = get_object_or_404(Student, id=id)
    if request.method == "POST":
        form = StudentForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            form.save()
            return redirect("vege:students")
    else:
        form = StudentForm(instance=student)
    return render(request, "vege/student_form.html", {"form": form, "title": "Edit Student"})


def student_delete(request, id):
    student = get_object_or_404(Student, id=id)
    # safer to require POST for delete
    if request.method == "POST":
        student.delete()
        return redirect("vege:students")

    # Optional: show a confirmation page if GET
    return render(request, "vege/student_confirm_delete.html", {"student": student})

def see_marks(request, student_id):
    subjects_marks = SubjectsMarks.objects.filter(
        student__student_id__student_id=student_id
    ).select_related("student", "subject")

    student = subjects_marks.first().student if subjects_marks.exists() else None

    # Calculate total marks
    total_marks = sum(mark.marks for mark in subjects_marks) if subjects_marks else 0
    
    stats = subjects_marks.aggregate(
        avg_score=Avg("marks"),
        max_score=Max("marks"),
        min_score=Min("marks"),
        total_subjects=Count("id")
    )
    
    # Calculate student's rank using database aggregation (more efficient)
    rank = None
    total_students = 0
    
    if student:
        # Get all student totals using aggregation - FIXED RELATIONSHIP NAME
        from django.db.models import Sum
        student_totals = Student.objects.annotate(
            total_marks=Sum('studentsmarks__marks')  # Changed to 'studentsmarks'
        ).exclude(total_marks__isnull=True).order_by('-total_marks')
        
        total_students = student_totals.count()
        
        # Find current student's rank
        for i, s in enumerate(student_totals, 1):
            if s.id == student.id:
                rank = i
                break

    return render(request, 'vege/see_marks.html', {
        'subjects_marks': subjects_marks,
        'student': student,
        'stats': stats,
        'total_marks': total_marks,
        'rank': rank,
        'total_students': total_students
    })
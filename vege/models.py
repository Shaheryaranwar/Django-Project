from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class RecipeManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)
    
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
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    recipe_view_count = models.IntegerField(default=1)
    is_deleted = models.BooleanField(default=False)

    objects = RecipeManager()  # Custom manager to filter out deleted recipes
    admin_objects = models.Manager()  # Default manager to access all recipes

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
class Department(models.Model):
    department = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.department
    
    class Meta:
        ordering = ['department']

class StudentID(models.Model):
    student_id = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.student_id
class Subject(models.Model):
    subject_name = models.CharField(max_length=100, unique=True)

    def __str__(self) -> str:
        return self.subject_name

class Student(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='students')
    student_id = models.OneToOneField(StudentID, on_delete=models.CASCADE, related_name='student_profile')
    student_name = models.CharField(max_length=100)
    student_email = models.EmailField(unique=True)
    student_phone = models.CharField(max_length=15, unique=True)
    student_address = models.TextField()
    is_deleted = models.BooleanField(default=False)
    student_age = models.PositiveIntegerField(
    validators=[MinValueValidator(18), MaxValueValidator(30)],
    null=True,       # Allows NULL in database
    blank=True,      # Allows empty in forms/admin
)
    
    student_image = models.ImageField(upload_to='students/', null=True, blank=True)

    objects = RecipeManager()  # Custom manager to filter out deleted recipes
    admin_objects = models.Manager()

    def __str__(self) -> str:
        return self.student_name

    class Meta:
        ordering = ['student_name']
        verbose_name = 'student'

class SubjectsMarks(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='studentsmarks')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    marks = models.PositiveIntegerField() 

    def __str__(self):
        return f"{self.student.student_name}  {self.subject.subject_name}"
    

    class Meta:
        unique_together = ['student', 'subject']
        verbose_name = "Subject Mark"


class ReportCard(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='reportcards')
    student_rank = models.PositiveIntegerField()
    date_reportcard_issued = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = ['student_rank', 'date_reportcard_issued']
        ordering = ['-date_reportcard_issued']
        verbose_name = "Report Card"

    def __str__(self):
        return f"{self.student} - Rank {self.student_rank}"
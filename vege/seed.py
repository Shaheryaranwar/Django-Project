from faker import Faker
import random 
from .models import *  # Make sure to import models correctly
from django.db.models import Sum


fake = Faker()


def create_subject_marks(n)-> None:
    try:
        student_objs = Student.objects.all()
        for student in student_objs:
            subjects = Subject.objects.all()  # or student.subject_set.all() if no related_name
            for subject in subjects:
                SubjectsMarks.objects.create(
                    student=student,
                    subject=subject,
                    marks=random.randint(25, 99)
                )
        print("Subject marks created successfully.")
    except Exception as e:
        print(f"Error creating subject marks: {e}")
create_subject_marks(100)  # Call this function to create subject marks for students
def seed_db(n=50) -> None:
    try: 
        for _ in range(n):
            # Get all departments
            departments = Department.objects.all()
            if not departments.exists():
                print("No departments found. Please create departments first.")
                return
            
            # Select a random department
            department = random.choice(departments)
            
            # Generate fake student data
            student_name = fake.name()
            student_email = fake.email()
            student_phone = fake.phone_number()
            student_address = fake.address()
            student_age = random.randint(18, 30)
            
            # Create a StudentID first (assuming StudentID has an auto-incrementing 'student_id' field)
            student_id_obj = StudentID.objects.create()
            
            # Create the Student record
            student_obj = Student.objects.create(
                department=department,
                student_id=student_id_obj,
                student_name=student_name,
                student_email=student_email,
                student_phone=student_phone,
                student_address=student_address,
                student_age=student_age,
            )
            
            print(f"Created student: {student_name} (ID: {student_id_obj.student_id})")
            
    except Exception as e:
        print(f"Error seeding database: {e}")


def generate_report_cards():
    students_with_totals = Student.objects.annotate(
        total_marks=Sum('studentsmarks__marks')
    ).order_by('-total_marks')

    for i, student in enumerate(students_with_totals, 1):
        ReportCard.objects.create(
            student=student,
            student_rank=i
        )
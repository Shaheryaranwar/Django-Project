import os
import tempfile
import random
import requests
from django.core.files import File
from django.core.management.base import BaseCommand
from faker import Faker
from vege.models import StudentID, Student, Department

fake = Faker()

class Command(BaseCommand):
    help = "Seed Students and StudentIDs with fake data, and update existing students"

    def add_arguments(self, parser):
        parser.add_argument(
            '--new',
            type=int,
            default=50,
            help='Number of new students to create (default: 50)'
        )
        parser.add_argument(
            '--update-existing',
            action='store_true',
            help='Update age for existing students with NULL age'
        )

    def handle(self, *args, **kwargs):
        departments = list(Department.objects.all())
        if not departments:
            self.stdout.write(self.style.ERROR("Please create some Department entries first."))
            return

        # Update existing students if requested
        if kwargs['update_existing']:
            self.update_existing_students()

        # Create new students
        self.create_new_students(kwargs['new'])

    def update_existing_students(self):
        """Update age for existing students with NULL age"""
        students_to_update = Student.objects.filter(student_age__isnull=True)
        count = students_to_update.count()

        if count == 0:
            self.stdout.write(self.style.SUCCESS("✅ All students already have age values"))
            return

        self.stdout.write(f"⏳ Updating age for {count} existing students...")
        
        updated = 0
        for student in students_to_update:
            student.student_age = random.randint(18, 30)
            student.save()
            updated += 1
            if updated % 10 == 0:  # Print progress every 10 updates
                self.stdout.write(f"Updated {updated}/{count} students...")

        self.stdout.write(self.style.SUCCESS(f"✅ Successfully updated {updated} students"))

    def create_new_students(self, num_students):
        """Create new students with all fields populated"""
        if num_students <= 0:
            return

        self.stdout.write(f"⏳ Creating {num_students} new students...")
        
        for _ in range(num_students):
            try:
                # Create unique StudentID
                student_id_str = fake.unique.bothify(text='??###??###')
                student_id_obj = StudentID.objects.create(student_id=student_id_str)

                # Prepare fake student data
                department = random.choice(Department.objects.all())
                student = Student(
                    department=department,
                    student_id=student_id_obj,
                    student_name=fake.name(),
                    student_email=fake.unique.email(),
                    student_phone=fake.unique.phone_number(),
                    student_address=fake.address(),
                    student_age=random.randint(18, 30),  # Age is always set for new students
                )

                # Download and attach random image
                image_url = f"https://randomuser.me/api/portraits/men/{random.randint(1,99)}.jpg"
                with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as tmp_file:
                    response = requests.get(image_url)
                    tmp_file.write(response.content)
                    tmp_file.flush()
                    
                    with open(tmp_file.name, 'rb') as f:
                        student.student_image.save(
                            f"{student.student_name.replace(' ', '_')}.jpg", 
                            File(f), 
                            save=False
                        )
                
                student.save()
                os.unlink(tmp_file.name)
                
                self.stdout.write(f"Created student: {student.student_name} (Age: {student.student_age})")

            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error creating student: {str(e)}"))
                continue

        self.stdout.write(self.style.SUCCESS(f"✅ Successfully created {num_students} new students"))
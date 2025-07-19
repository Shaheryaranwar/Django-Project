from django.db import models

# Create your models here.
class Receipe(models.Model):
    receipe_name = models.CharField(max_length=100)
    receipe_description = models.TextField()
    ingredients = models.TextField()
    instructions = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    receipe_image = models.ImageField(upload_to='receipes/', null=True, blank=True)



    def __str__(self):
        return self.receipe_name
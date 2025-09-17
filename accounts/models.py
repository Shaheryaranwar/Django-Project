from django.contrib.auth.models import AbstractUser
from django.db import models
from .manager import UserManager

class CustomUser(AbstractUser):
    username = None
    phone_number = models.CharField(max_length=100, unique=True)
    user_Bio = models.TextField(max_length=75, blank=True)
    email = models.EmailField(unique=True)
    user_profile_pic = models.ImageField(upload_to='user_profile_pics', blank=True)

    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = ["email"]

    objects = UserManager()

    groups = models.ManyToManyField(
        "auth.Group",
        related_name="customuser_set",   # 👈 avoid clash with default User.groups
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="customuser_set",   # 👈 avoid clash with default User.user_permissions
        blank=True,
    )

    def __str__(self):
        return self.email or self.phone_number

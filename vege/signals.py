from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserProfile

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """
    Safe version that checks if userprofile exists
    """
    try:
        # Check if userprofile exists before saving
        if hasattr(instance, 'userprofile'):
            instance.userprofile.save()
        else:
            # Create it if it doesn't exist
            UserProfile.objects.create(user=instance)
    except UserProfile.DoesNotExist:
        # Create it if it doesn't exist
        UserProfile.objects.create(user=instance)
    except Exception as e:
        # Log error but don't crash the application
        print(f"Error saving user profile for {instance.username}: {e}")
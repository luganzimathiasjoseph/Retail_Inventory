from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import Business

User = get_user_model()

@receiver(post_save, sender=Business)
def create_default_users(sender, instance, created, **kwargs):
    if created:
        manager = User.objects.create_user(
            username="manager",
            password="admin",
            role="manager",
            business=instance
        )
        inventory_manager = User.objects.create_user(
            username="inventory",
            password="admin",
            role="inventory_manager",
            business=instance
        )

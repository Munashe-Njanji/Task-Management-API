from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Todo, ActivityLog


@receiver(post_save, sender=Todo)
def log_todo_creation(sender, instance, created, **kwargs):
    if created:
        ActivityLog.objects.create(
            user=instance.user, action="created", target=f"Todo: {instance.title}"
        )


@receiver(post_delete, sender=Todo)
def log_todo_deletion(sender, instance, **kwargs):
    ActivityLog.objects.create(
        user=instance.user, action="deleted", target=f"Todo: {instance.title}"
    )

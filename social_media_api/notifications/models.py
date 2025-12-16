# notifications/models.py

from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

class Notification(models.Model):
    """Model to track user notifications for various actions."""
    
    # The user who will receive the notification
    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='notifications'
    )
    
    # The user who performed the action (e.g., the user who liked the post)
    actor = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='actions_made'
    )
    
    # The action description (e.g., 'liked', 'commented', 'followed')
    verb = models.CharField(max_length=255)
    
    # Generic Foreign Key to the object that was acted upon (Post, Comment, etc.)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    target = GenericForeignKey('content_type', 'object_id')
    
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ('-timestamp',)

    def __str__(self):
        return f'{self.actor.username} {self.verb} {self.target} (to {self.recipient.username})'
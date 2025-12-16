from django.db import models
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from notifications.models import Notification # Import Notification here for Comment post-save signal (later)

# Get the User Model defined in settings.AUTH_USER_MODEL
User = settings.AUTH_USER_MODEL

class Post(models.Model):
    """The main model for user-created content."""
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return self.title

class Comment(models.Model):
    """Model for user comments on posts."""
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created_at',)
        
    def __str__(self):
        return f"Comment by {self.author} on {self.post.title[:20]}"

class Like(models.Model):
    """Tracks which user liked which post."""
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='likes'
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE, 
        related_name='likes'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Ensures a user can only like a post once
        unique_together = ('user', 'post')
        ordering = ('-created_at',)

    def __str__(self):
        return f'{self.user.username} likes {self.post.title[:20]}'

# --- Signal for Comment Creation Notification ---
from django.db.models.signals import post_save
from django.dispatch import receiver

# Define a signal handler to create a notification when a comment is saved
@receiver(post_save, sender=Comment)
def create_comment_notification(sender, instance, created, **kwargs):
    """Creates a notification when a new comment is posted on a user's post."""
    if created and instance.post.author != instance.author:
        # 1. Get the recipient (Post author)
        recipient = instance.post.author
        
        # 2. Get the ContentType for the Post object
        post_content_type = ContentType.objects.get_for_model(Post)
        
        # 3. Create the notification
        Notification.objects.create(
            recipient=recipient,
            actor=instance.author,
            verb='commented on your post',
            content_type=post_content_type,
            object_id=instance.post.id,
            target=instance.post # GenericForeignKey works with the object
        )
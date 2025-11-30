from django.db import models
# Import the CONF settings for the custom user model reference
from django.conf import settings 
from django.db.models.signals import post_save
from django.dispatch import receiver
# 🚨 REMOVED: from django.contrib.auth.models import User 
# We no longer import the default User!

# -----------------------
# UserProfile (Role-based)
# -----------------------
class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('Admin', 'Admin'),
        ('Librarian', 'Librarian'),
        ('Member', 'Member'),
    ]
    # 💥 CRITICAL FIX: Reference the custom user model via settings
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,  # <--- FIXED
        on_delete=models.CASCADE, 
        related_name='userprofile'
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='Member')

    def __str__(self):
        # We assume the CustomUser still has a 'username' field, which it does (AbstractUser inheritance)
        return f"{self.user.username} - {self.role}"

# Signal handlers must now reference settings.AUTH_USER_MODEL indirectly
# By using the sender's default user class (if the CustomUser is fully replacing it)
# Or by getting the model: get_user_model(). However, using the model name in the sender usually works fine.

@receiver(post_save, sender=settings.AUTH_USER_MODEL) # <--- FIXED sender reference
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=settings.AUTH_USER_MODEL) # <--- FIXED sender reference
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()

# -----------------------
# Library System Models
# -----------------------
class Author(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        permissions = [
            ("can_add_book", "Can add a book"),
            ("can_change_book", "Can change a book"),
            ("can_delete_book", "Can delete a book"),
        ]

class Library(models.Model):
    name = models.CharField(max_length=100)
    books = models.ManyToManyField(Book)

    def __str__(self):
        return self.name

class Librarian(models.Model):
    name = models.CharField(max_length=100)
    library = models.ForeignKey(Library, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
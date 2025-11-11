from django.db import models

# Author Model
class Author(models.Model):
    """
    Represents an author who writes books.
    """
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


# Book Model
class Book(models.Model):
    """
    Represents a book written by an author.
    Uses ForeignKey to establish a many-to-one relationship with Author.
    """
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')

    def __str__(self):
        return self.title


# Library Model
class Library(models.Model):
    """
    Represents a library that contains multiple books.
    Uses ManyToManyField to establish a many-to-many relationship with Book.
    """
    name = models.CharField(max_length=200)
    books = models.ManyToManyField(Book, related_name='libraries')

    def __str__(self):
        return self.name


# Librarian Model
class Librarian(models.Model):
    """
    Represents a librarian who manages a library.
    Uses OneToOneField to establish a one-to-one relationship with Library.
    """
    name = models.CharField(max_length=200)
    library = models.OneToOneField(Library, on_delete=models.CASCADE, related_name='librarian')

    def __str__(self):
        return self.name
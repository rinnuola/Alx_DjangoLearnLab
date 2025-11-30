"""
Sample queries demonstrating Django ORM relationships.
These queries showcase ForeignKey, ManyToManyField, and OneToOneField relationships.
"""

from relationship_app.models import Author, Book, Library, Librarian


def query_books_by_author(author_name):
    """
    Query all books by a specific author.
    Demonstrates ForeignKey relationship (Book -> Author).
    
    Args:
        author_name (str): The name of the author
    
    Returns:
        QuerySet: All books written by the specified author
    """
    try:
        author = Author.objects.get(name=author_name)
        books = Book.objects.filter(author=author)
        print(f"\nBooks by {author_name}:")
        for book in books:
            print(f"  - {book.title}")
        return books
    except Author.DoesNotExist:
        print(f"Author '{author_name}' not found.")
        return None


def list_books_in_library(library_name):
    """
    List all books in a specific library.
    Demonstrates ManyToManyField relationship (Library <-> Book).
    
    Args:
        library_name (str): The name of the library
    
    Returns:
        QuerySet: All books in the specified library
    """
    try:
        library = Library.objects.get(name=library_name)
        books = library.books.all()
        print(f"\nBooks in {library_name}:")
        for book in books:
            print(f"  - {book.title}")
        return books
    except Library.DoesNotExist:
        print(f"Library '{library_name}' not found.")
        return None


def retrieve_librarian_for_library(library_name):
    """
    Retrieve the librarian for a specific library.
    Demonstrates OneToOneField relationship (Librarian <-> Library).
    
    Args:
        library_name (str): The name of the library
    
    Returns:
        Librarian: The librarian managing the specified library
    """
    try:
        library = Library.objects.get(name=library_name)
        librarian = Librarian.objects.get(library=library)
        print(f"\nLibrarian for {library_name}: {librarian.name}")
        return librarian
    except Library.DoesNotExist:
        print(f"Library '{library_name}' not found.")
        return None
    except Librarian.DoesNotExist:
        print(f"No librarian assigned to {library_name}.")
        return None


# Alternative query methods using related_name

def query_books_by_author_alternative(author_name):
    """
    Alternative method to query books by author using related_name.
    """
    try:
        author = Author.objects.get(name=author_name)
        books = author.books.all()  # Using related_name='books'
        print(f"\nBooks by {author_name} (using related_name):")
        for book in books:
            print(f"  - {book.title}")
        return books
    except Author.DoesNotExist:
        print(f"Author '{author_name}' not found.")
        return None


def retrieve_librarian_alternative(library_name):
    """
    Alternative method to retrieve librarian using related_name.
    """
    try:
        library = Library.objects.get(name=library_name)
        librarian = library.librarian  # Using related_name='librarian'
        print(f"\nLibrarian for {library_name} (using related_name): {librarian.name}")
        return librarian
    except Library.DoesNotExist:
        print(f"Library '{library_name}' not found.")
        return None
    except Library.librarian.RelatedObjectDoesNotExist:
        print(f"No librarian assigned to {library_name}.")
        return None


# Example usage (can be run in Django shell)
if __name__ == "__main__":
    print("=" * 50)
    print("Django ORM Relationship Query Samples")
    print("=" * 50)
    
    # Example queries
    # Note: Run these in Django shell after creating sample data
    
    # query_books_by_author("J.K. Rowling")
    # list_books_in_library("Central Library")
    # retrieve_librarian_for_library("Central Library")
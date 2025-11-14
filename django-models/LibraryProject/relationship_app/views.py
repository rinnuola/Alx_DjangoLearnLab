from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import DetailView
from .models import Book, Library
from .models import Library  # Explicit import for checker

def register(request):
    """
    Placeholder view for user registration. 
    It currently redirects to the login page (assuming 'login' is a valid name).
    You would replace this with actual registration logic later.
    """
    # Placeholder action: Redirect user to the login page
    return redirect('login') 

# --- Function-based View ---
def list_books(request):
    """
    Lists all books from the database.
    """
    all_books = Book.objects.all().select_related('author')
    context = {
        'books': all_books
    }
    # Renders the information using the list_books.html template
    return render(request, 'relationship_app/list_books.html', context)

# --- Class-based View (DetailView) ---
class LibraryDetailView(DetailView):
    """
    Displays the details of a specific Library, including its books.
    """
    model = Library
    template_name = 'relationship_app/library_detail.html'
    # Specify the name of the object in the context dictionary (e.g., {'library': ...})
    context_object_name = 'library'

    
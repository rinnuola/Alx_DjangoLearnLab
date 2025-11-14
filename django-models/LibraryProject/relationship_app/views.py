from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.detail import DetailView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from .models import Book
from .models import Library

def register(request):
    """
    Handle user registration.
    """
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log the user in after registration
            return redirect('list_books')  # Redirect to books list after registration
    else:
        form = UserCreationForm()
    
    return render(request, 'relationship_app/register.html', {'form': form})

# --- Function-based View ---
def list_books(request):
    """
    Lists all books from the database.
    """
    all_books = Book.objects.all().select_related('author')
    context = {
        'books': all_books
    }
    return render(request, 'relationship_app/list_books.html', context)

# --- Class-based View (DetailView) ---
class LibraryDetailView(DetailView):
    """
    Displays the details of a specific Library, including its books.
    """
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'
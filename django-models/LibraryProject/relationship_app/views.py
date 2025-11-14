from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test, login_required
from django.views.generic import DetailView
from .models import Book, Library, UserProfile

# --------------------------
# Role-checking functions
# --------------------------
def is_admin(user):
    return user.is_authenticated and hasattr(user, 'userprofile') and user.userprofile.role == 'Admin'

def is_librarian(user):
    return user.is_authenticated and hasattr(user, 'userprofile') and user.userprofile.role == 'Librarian'

def is_member(user):
    return user.is_authenticated and hasattr(user, 'userprofile') and user.userprofile.role == 'Member'

# --------------------------
# Role-based views
# --------------------------
@user_passes_test(is_admin)
@login_required
def admin_view(request):
    context = {'role': 'Admin', 'user': request.user}
    return render(request, 'relationship_app/admin_view.html', context)

@user_passes_test(is_librarian)
@login_required
def librarian_view(request):
    context = {'role': 'Librarian', 'user': request.user}
    return render(request, 'relationship_app/librarian_view.html', context)

@user_passes_test(is_member)
@login_required
def member_view(request):
    context = {'role': 'Member', 'user': request.user}
    return render(request, 'relationship_app/member_view.html', context)

# --------------------------
# Book listing view
# --------------------------
def list_books(request):
    all_books = Book.objects.all().select_related('author')
    context = {
        'books': all_books
    }
    return render(request, 'relationship_app/list_books.html', context)

# --------------------------
# Library detail view
# --------------------------
class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'

# --------------------------
# Placeholder registration
# --------------------------
def register(request):
    # Placeholder view: redirect to login for now
    return redirect('login')

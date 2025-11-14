from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import permission_required
from .models import Book

# --- Add Book ---
@permission_required('relationship_app.can_add_book', raise_exception=True)
def add_book(request):
    if request.method == "POST":
        title = request.POST.get('title')
        author_id = request.POST.get('author')
        if title and author_id:
            from .models import Author
            author = get_object_or_404(Author, id=author_id)
            Book.objects.create(title=title, author=author)
            return redirect('list_books')
    return render(request, 'relationship_app/add_book.html')

# --- Edit Book ---
@permission_required('relationship_app.can_change_book', raise_exception=True)
def edit_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == "POST":
        title = request.POST.get('title')
        author_id = request.POST.get('author')
        if title and author_id:
            from .models import Author
            book.title = title
            book.author = get_object_or_404(Author, id=author_id)
            book.save()
            return redirect('list_books')
    context = {'book': book}
    return render(request, 'relationship_app/edit_book.html', context)

# --- Delete Book ---
@permission_required('relationship_app.can_delete_book', raise_exception=True)
def delete_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == "POST":
        book.delete()
        return redirect('list_books')
    context = {'book': book}
    return render(request, 'relationship_app/delete_book.html', context)

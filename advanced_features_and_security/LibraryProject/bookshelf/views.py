from django.contrib.auth.decorators import permission_required
from django.shortcuts import render
from .models import Book
from .forms import ExampleForm  # <-- Added import for ExampleForm

@permission_required("bookshelf.can_view", raise_exception=True)
def book_list(request):
    books = Book.objects.all()
    return render(request, "bookshelf/book_list.html", {"books": books})

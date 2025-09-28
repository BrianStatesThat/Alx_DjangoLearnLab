"""
API views for Author and Book models.
Provides basic CRUD operations and demonstrates serializer usage.
"""

from rest_framework import generics
from .models import Author, Book
from .serializers import AuthorSerializer, BookSerializer, AuthorSummarySerializer


class AuthorListCreateView(generics.ListCreateAPIView):
    """
    View to list all authors or create a new author.
    
    Uses AuthorSerializer for detailed author information including nested books.
    Suitable for both listing and creation operations.
    """
    queryset = Author.objects.prefetch_related('books').all()
    serializer_class = AuthorSerializer


class AuthorDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    View to retrieve, update, or delete a specific author.
    
    Provides full CRUD operations for individual author instances.
    Includes nested book data in retrieval.
    """
    queryset = Author.objects.prefetch_related('books').all()
    serializer_class = AuthorSerializer


class BookListCreateView(generics.ListCreateAPIView):
    """
    View to list all books or create a new book.
    
    Uses BookSerializer which includes custom validation for publication_year.
    Demonstrates proper error handling for validation rules.
    """
    queryset = Book.objects.select_related('author').all()
    serializer_class = BookSerializer


class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    View to retrieve, update, or delete a specific book.
    
    Provides full CRUD operations for individual book instances.
    Enforces publication_year validation on updates.
    """
    queryset = Book.objects.select_related('author').all()
    serializer_class = BookSerializer
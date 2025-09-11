from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Book, Library

def list_books(request):
    """Function-based view to list all books"""
    books = Book.objects.all().select_related('author')
    return render(request, 'relationship_app/list_books.html', {'books': books})
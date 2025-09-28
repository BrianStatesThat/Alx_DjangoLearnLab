"""
URL configuration for API application with detailed routing for CRUD operations.
Organized by resource type with clear endpoint naming conventions.
"""

from django.urls import path
from . import views

app_name = 'api'

# Book URL patterns - organized by CRUD operations
book_urlpatterns = [
    # Read operations - public access
    path('books/', views.BookListView.as_view(), name='book-list'),
    path('books/<int:pk>/', views.BookDetailView.as_view(), name='book-detail'),
    
    # Write operations - authenticated users only
    path('books/create/', views.BookCreateView.as_view(), name='book-create'),
    path('books/<int:pk>/update/', views.BookUpdateView.as_view(), name='book-update'),
    path('books/<int:pk>/delete/', views.BookDeleteView.as_view(), name='book-delete'),
]

# Author URL patterns - similar structure
author_urlpatterns = [
    # Read operations - public access
    path('authors/', views.AuthorListView.as_view(), name='author-list'),
    path('authors/<int:pk>/', views.AuthorDetailView.as_view(), name='author-detail'),
    
    # Write operations - authenticated users only
    path('authors/create/', views.AuthorCreateView.as_view(), name='author-create'),
    path('authors/<int:pk>/update/', views.AuthorUpdateView.as_view(), name='author-update'),
    path('authors/<int:pk>/delete/', views.AuthorDeleteView.as_view(), name='author-delete'),
]

# Combine all URL patterns
urlpatterns = book_urlpatterns + author_urlpatterns
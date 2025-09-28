"""
Admin configuration for API models.
Enables management of Authors and Books through Django admin interface.
"""

from django.contrib import admin
from .models import Author, Book


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    """Admin interface configuration for Author model."""
    
    list_display = ['name', 'book_count', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name']
    readonly_fields = ['created_at', 'updated_at']
    
    def book_count(self, obj):
        """Display book count in admin list."""
        return obj.book_count
    book_count.short_description = 'Number of Books'


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    """Admin interface configuration for Book model."""
    
    list_display = ['title', 'author', 'publication_year', 'created_at']
    list_filter = ['publication_year', 'author', 'created_at']
    search_fields = ['title', 'author__name']
    readonly_fields = ['created_at', 'updated_at']
    autocomplete_fields = ['author']  # Enables search for author field
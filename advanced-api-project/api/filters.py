"""
Custom filter classes for advanced query capabilities.
Provides fine-grained control over filtering, searching, and ordering of Book model.
"""

import django_filters
from django.db.models import Q
from .models import Book, Author


class BookFilter(django_filters.FilterSet):
    """
    Advanced filter class for Book model with custom filtering options.
    
    Features:
    - Exact match filtering on specific fields
    - Range filtering for numeric fields
    - Case-insensitive contains filtering
    - Custom lookup expressions
    """
    
    # Exact match filters
    title = django_filters.CharFilter(
        field_name='title', 
        lookup_expr='exact',
        help_text="Exact match for book title"
    )
    
    title_contains = django_filters.CharFilter(
        field_name='title',
        lookup_expr='icontains',
        help_text="Case-insensitive contains search in title"
    )
    
    author = django_filters.CharFilter(
        field_name='author__name',
        lookup_expr='exact',
        help_text="Exact match for author name"
    )
    
    author_contains = django_filters.CharFilter(
        field_name='author__name',
        lookup_expr='icontains',
        help_text="Case-insensitive contains search in author name"
    )
    
    # Range filters for publication year
    publication_year = django_filters.NumberFilter(
        field_name='publication_year',
        help_text="Exact publication year"
    )
    
    publication_year_min = django_filters.NumberFilter(
        field_name='publication_year',
        lookup_expr='gte',
        help_text="Books published in or after this year"
    )
    
    publication_year_max = django_filters.NumberFilter(
        field_name='publication_year',
        lookup_expr='lte',
        help_text="Books published in or before this year"
    )
    
    # Multiple choice filter example
    publication_decade = django_filters.NumberFilter(
        method='filter_by_decade',
        help_text="Filter by publication decade (e.g., 2020 for 2020-2029)"
    )
    
    # Boolean filter example
    recent_books = django_filters.BooleanFilter(
        method='filter_recent_books',
        help_text="Filter books published in the last 5 years"
    )
    
    class Meta:
        model = Book
        fields = {
            'title': ['exact', 'icontains'],
            'author__name': ['exact', 'icontains'],
            'publication_year': ['exact', 'gte', 'lte'],
        }
    
    def filter_by_decade(self, queryset, name, value):
        """
        Custom method to filter books by publication decade.
        
        Example: 
        - Value 2020 would return books from 2020-2029
        - Value 1990 would return books from 1990-1999
        
        Args:
            queryset: The original queryset
            name: Field name (unused)
            value: The decade to filter by (e.g., 2020)
            
        Returns:
            Filtered queryset
        """
        if value:
            return queryset.filter(
                publication_year__gte=value,
                publication_year__lte=value + 9
            )
        return queryset
    
    def filter_recent_books(self, queryset, name, value):
        """
        Custom method to filter recent books (published in last 5 years).
        
        Args:
            queryset: The original queryset
            name: Field name (unused)
            value: Boolean flag (True for recent books only)
            
        Returns:
            Filtered queryset
        """
        from django.utils import timezone
        if value:
            current_year = timezone.now().year
            return queryset.filter(
                publication_year__gte=current_year - 5
            )
        return queryset
    
    @property
    def qs(self):
        """
        Override to add custom queryset optimizations.
        """
        queryset = super().qs
        # Always select related author to optimize database queries
        return queryset.select_related('author')


class AuthorFilter(django_filters.FilterSet):
    """
    Filter class for Author model with book count filtering.
    """
    
    name = django_filters.CharFilter(
        lookup_expr='icontains',
        help_text="Case-insensitive search in author name"
    )
    
    min_books = django_filters.NumberFilter(
        method='filter_min_books',
        help_text="Authors with at least this many books"
    )
    
    max_books = django_filters.NumberFilter(
        method='filter_max_books',
        help_text="Authors with at most this many books"
    )
    
    class Meta:
        model = Author
        fields = ['name']
    
    def filter_min_books(self, queryset, name, value):
        """
        Filter authors with minimum number of books.
        """
        if value:
            return queryset.annotate(
                book_count=models.Count('books')
            ).filter(book_count__gte=value)
        return queryset
    
    def filter_max_books(self, queryset, name, value):
        """
        Filter authors with maximum number of books.
        """
        if value:
            return queryset.annotate(
                book_count=models.Count('books')
            ).filter(book_count__lte=value)
        return queryset
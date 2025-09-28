"""
Advanced API views for Book model using Django REST Framework's generic views.
Includes CRUD operations, custom permissions, and optimized query handling.
"""
from .permissions import IsAuthenticatedOrReadOnly, IsAdminOrReadOnly, BookAccessPermission
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Author, Book
from .serializers import AuthorSerializer, BookSerializer, AuthorSummarySerializer


class BookListView(generics.ListAPIView):
    """
    ListView for retrieving all books with filtering, searching, and ordering capabilities.
    
    Features:
    - List all books with pagination
    - Filter by author, publication year
    - Search in book titles
    - Order by various fields
    - Public read-only access
    """
    queryset = Book.objects.select_related('author').all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]  # Public read access
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['author', 'publication_year']
    search_fields = ['title', 'author__name']
    ordering_fields = ['title', 'publication_year', 'created_at']
    ordering = ['-created_at']  # Default ordering: newest first


class BookDetailView(generics.RetrieveAPIView):
    """
    DetailView for retrieving a single book by ID.
    
    Features:
    - Retrieve specific book with full details
    - Includes nested author information
    - Public read-only access
    - Optimized database queries with select_related
    """
    queryset = Book.objects.select_related('author').all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]  # Public read access
    lookup_field = 'pk'


class BookCreateView(generics.CreateAPIView):
    """
    CreateView for adding a new book with custom validation and permissions.
    
    Features:
    - Create new book instances
    - Custom validation for publication_year
    - Restricted to authenticated users only
    - Custom success response format
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]  # Only authenticated users can create
    
    def perform_create(self, serializer):
        """
        Customize the creation process.
        Can add additional logic like setting created_by user here.
        """
        serializer.save()
        # Example: If you had a created_by field
        # serializer.save(created_by=self.request.user)
    
    def create(self, request, *args, **kwargs):
        """
        Override create to provide custom response format.
        """
        response = super().create(request, *args, **kwargs)
        # Customize response data
        response.data = {
            'message': 'Book created successfully',
            'data': response.data
        }
        return response


class BookUpdateView(generics.UpdateAPIView):
    """
    UpdateView for modifying an existing book with partial updates support.
    
    Features:
    - Update existing book instances
    - Supports both PUT (full update) and PATCH (partial update)
    - Restricted to authenticated users only
    - Custom validation enforcement
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]  # Using custom permission
    
    def perform_update(self, serializer):
        """
        Customize the update process.
        """
        serializer.save()
    
    def update(self, request, *args, **kwargs):
        """
        Override update to provide custom response format.
        """
        response = super().update(request, *args, **kwargs)
        response.data = {
            'message': 'Book updated successfully',
            'data': response.data
        }
        return response


class BookDeleteView(generics.DestroyAPIView):
    """
    DeleteView for removing a book with proper permissions and custom responses.
    
    Features:
    - Delete book instances
    - Restricted to authenticated users only
    - Custom success response
    - Soft delete potential (commented example)
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]  # Only authenticated users can delete
    
    def perform_destroy(self, instance):
        """
        Customize the deletion process.
        
        Example for soft delete (uncomment if needed):
        instance.is_active = False
        instance.save()
        """
        # For soft delete implementation, you would modify this method
        # and add an 'is_active' field to your model
        instance.delete()
    
    def destroy(self, request, *args, **kwargs):
        """
        Override destroy to provide custom response format.
        """
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({
            'message': 'Book deleted successfully',
            'book_id': kwargs['pk']
        }, status=status.HTTP_204_NO_CONTENT)


# Enhanced Author Views with similar functionality
class AuthorListView(generics.ListAPIView):
    """
    ListView for authors with filtering and search capabilities.
    """
    queryset = Author.objects.prefetch_related('books').all()
    serializer_class = AuthorSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['name']
    search_fields = ['name']
    ordering_fields = ['name', 'created_at', 'book_count']
    ordering = ['name']


class AuthorDetailView(generics.RetrieveAPIView):
    """
    DetailView for retrieving a single author with nested books.
    """
    queryset = Author.objects.prefetch_related('books').all()
    serializer_class = AuthorSerializer
    permission_classes = [permissions.AllowAny]


class AuthorCreateView(generics.CreateAPIView):
    """
    CreateView for adding new authors (authenticated users only).
    """
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [permissions.IsAuthenticated]


class AuthorUpdateView(generics.UpdateAPIView):
    """
    UpdateView for modifying existing authors (authenticated users only).
    """
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [permissions.IsAuthenticated]


class AuthorDeleteView(generics.DestroyAPIView):
    """
    DeleteView for removing authors (authenticated users only).
    """
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [permissions.IsAuthenticated]

"""
Additional custom views demonstrating advanced DRF features and custom behaviors.
"""

from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework import viewsets
from django.db.models import Count, Q

class BookViewSet(viewsets.ModelViewSet):
    """
    ViewSet demonstrating an alternative approach using ModelViewSet.
    Provides all CRUD operations in a single class with custom actions.
    """
    queryset = Book.objects.select_related('author').all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]  # Using custom permission
    
    def get_permissions(self):
        """
        Custom permission handling based on action type.
        """
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [permissions.AllowAny]
        return [permission() for permission in permission_classes]
    
    def get_queryset(self):
        """
        Custom queryset filtering based on query parameters.
        """
        queryset = super().get_queryset()
        
        # Filter by publication year range
        min_year = self.request.query_params.get('min_year')
        max_year = self.request.query_params.get('max_year')
        
        if min_year:
            queryset = queryset.filter(publication_year__gte=min_year)
        if max_year:
            queryset = queryset.filter(publication_year__lte=max_year)
        
        return queryset
    
    @action(detail=False, methods=['get'])
    def recent_books(self, request):
        """
        Custom action to get recent books (published in last 10 years).
        Example: /api/books/recent_books/
        """
        from django.utils import timezone
        current_year = timezone.now().year
        recent_books = self.get_queryset().filter(
            publication_year__gte=current_year - 10
        )
        serializer = self.get_serializer(recent_books, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def duplicate(self, request, pk=None):
        """
        Custom action to duplicate a book.
        Example: POST /api/books/1/duplicate/
        """
        original_book = self.get_object()
        original_book.pk = None  # This will create a new instance
        original_book.title = f"{original_book.title} (Copy)"
        original_book.save()
        serializer = self.get_serializer(original_book)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CustomBookCreateView(generics.CreateAPIView):
    """
    Highly customized CreateView with additional business logic.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        """
        Extended creation logic with additional validation and side effects.
        """
        # Custom validation beyond serializer
        publication_year = serializer.validated_data.get('publication_year')
        title = serializer.validated_data.get('title')
        
        # Check for duplicate books (same title and author in same year)
        author = serializer.validated_data.get('author')
        duplicate_exists = Book.objects.filter(
            title=title,
            author=author,
            publication_year=publication_year
        ).exists()
        
        if duplicate_exists:
            from rest_framework.exceptions import ValidationError
            raise ValidationError({
                'non_field_errors': ['A book with this title and author already exists for this year.']
            })
        
        # Save the instance
        book = serializer.save()
        
        # Example: Additional side effects (logging, notifications, etc.)
        print(f"New book created: {book.title} by {book.author.name}")
        
        # You could also send signals or trigger async tasks here
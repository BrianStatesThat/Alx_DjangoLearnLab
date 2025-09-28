"""
Custom serializers for the API application.
Handles complex data structures, nested relationships, and custom validation.
"""

from rest_framework import serializers
from django.utils import timezone
from .models import Author, Book


class BookSerializer(serializers.ModelSerializer):
    """
    Serializer for Book model with custom validation.
    
    Handles:
    - Serialization of all Book model fields
    - Custom validation for publication_year
    - Read-only author name for display purposes
    
    Validation:
    - Ensures publication_year is not in the future
    - Provides descriptive error messages
    """
    
    # Read-only field to display author name in book serialization
    author_name = serializers.CharField(source='author.name', read_only=True)
    
    class Meta:
        model = Book
        fields = ['id', 'title', 'publication_year', 'author', 'author_name', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at', 'author_name']
    
    def validate_publication_year(self, value):
        """
        Custom validation for publication_year field.
        
        Args:
            value (int): The publication year to validate
            
        Returns:
            int: The validated publication year
            
        Raises:
            serializers.ValidationError: If publication year is in the future
        """
        current_year = timezone.now().year
        if value > current_year:
            raise serializers.ValidationError(
                f"Publication year cannot be in the future. Current year is {current_year}."
            )
        
        # Additional validation: reasonable publication year range
        if value < 1000 or value > current_year + 5:  # Allow some future for pre-orders
            raise serializers.ValidationError(
                f"Publication year {value} is not a valid year."
            )
        
        return value
    
    def validate(self, data):
        """
        Object-level validation for Book model.
        
        Args:
            data (dict): The data being validated
            
        Returns:
            dict: The validated data
        """
        # You can add cross-field validation here if needed
        # Example: Check if book with same title and author already exists
        return data


class AuthorSerializer(serializers.ModelSerializer):
    """
    Serializer for Author model with nested Book relationships.
    
    Handles:
    - Serialization of Author fields
    - Nested serialization of related Books using BookSerializer
    - Dynamic control over nested book inclusion
    
    Nested Relationships:
    - books: Nested representation of all books by this author
    - book_count: Computed field showing number of books
    """
    
    # Nested serializer for related books - many=True for one-to-many relationship
    books = BookSerializer(many=True, read_only=True)
    
    # Computed field to show book count
    book_count = serializers.IntegerField(source='books.count', read_only=True)
    
    class Meta:
        model = Author
        fields = ['id', 'name', 'books', 'book_count', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at', 'books', 'book_count']
    
    def create(self, validated_data):
        """
        Create author instance.
        Custom create logic can be added here if needed.
        """
        return Author.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        """
        Update author instance.
        Custom update logic can be added here if needed.
        """
        instance.name = validated_data.get('name', instance.name)
        instance.save()
        return instance


class AuthorSummarySerializer(serializers.ModelSerializer):
    """
    Simplified Author serializer for list views or when nested books aren't needed.
    
    Useful for:
    - List endpoints where full nested data isn't required
    - Reducing payload size in certain contexts
    - Performance optimization in list views
    """
    
    book_count = serializers.IntegerField(source='books.count', read_only=True)
    
    class Meta:
        model = Author
        fields = ['id', 'name', 'book_count']
        read_only_fields = ['id', 'book_count']
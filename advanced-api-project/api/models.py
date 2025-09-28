"""
Data models for the API application.
Defines Author and Book models with one-to-many relationship.
"""

from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone


class Author(models.Model):
    """
    Author model representing a book author.
    
    Fields:
    - name: CharField for the author's full name
    - created_at: DateTimeField for record creation timestamp
    - updated_at: DateTimeField for last update timestamp
    
    Relationships:
    - One Author can have multiple Books (one-to-many)
    """
    
    name = models.CharField(
        max_length=200,
        help_text="Full name of the author"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']  # Default ordering by author name
        verbose_name = 'Author'
        verbose_name_plural = 'Authors'
    
    def __str__(self):
        """String representation of Author model."""
        return self.name
    
    @property
    def book_count(self):
        """Return the number of books by this author."""
        return self.books.count()


class Book(models.Model):
    """
    Book model representing a published book.
    
    Fields:
    - title: CharField for the book's title
    - publication_year: IntegerField for the year of publication
    - author: ForeignKey linking to Author model
    - created_at: DateTimeField for record creation timestamp
    - updated_at: DateTimeField for last update timestamp
    
    Relationships:
    - Many Books can belong to one Author (many-to-one)
    """
    
    title = models.CharField(
        max_length=300,
        help_text="Title of the book"
    )
    publication_year = models.IntegerField(
        help_text="Year the book was published"
    )
    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        related_name='books',  # Enables author.books.all() reverse relation
        help_text="Author of the book"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-publication_year', 'title']  # Order by recent years first, then title
        verbose_name = 'Book'
        verbose_name_plural = 'Books'
        unique_together = ['title', 'author']  # Prevent duplicate books by same author
    
    def __str__(self):
        """String representation of Book model."""
        return f"{self.title} by {self.author.name}"
    
    def clean(self):
        """
        Custom validation to ensure publication year is not in the future.
        This validation runs both in forms and model.save().
        """
        current_year = timezone.now().year
        if self.publication_year > current_year:
            raise ValidationError({
                'publication_year': f'Publication year cannot be in the future. Current year is {current_year}.'
            })
    
    def save(self, *args, **kwargs):
        """
        Override save method to run full validation including clean() method.
        """
        self.full_clean()
        super().save(*args, **kwargs)
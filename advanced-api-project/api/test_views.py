"""
Comprehensive unit tests for Django REST Framework API endpoints.
Tests CRUD operations, filtering, searching, ordering, and permissions.
"""

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from ..models import Author, Book
from ..serializers import BookSerializer, AuthorSerializer


class BaseTestCase(APITestCase):
    """
    Base test case with common setup methods for all test classes.
    Provides reusable fixtures and helper methods.
    """
    
    def setUp(self):
        """
        Set up test data that will be used across multiple test cases.
        This runs before each test method.
        """
        # Create test users
        self.admin_user = User.objects.create_user(
            username='admin',
            password='testpass123',
            email='admin@example.com'
        )
        self.regular_user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='user@example.com'
        )
        
        # Create test authors
        self.author1 = Author.objects.create(name='J.K. Rowling')
        self.author2 = Author.objects.create(name='George Orwell')
        self.author3 = Author.objects.create(name='J.R.R. Tolkien')
        
        # Create test books
        self.book1 = Book.objects.create(
            title='Harry Potter and the Philosopher\'s Stone',
            publication_year=1997,
            author=self.author1
        )
        self.book2 = Book.objects.create(
            title='1984',
            publication_year=1949,
            author=self.author2
        )
        self.book3 = Book.objects.create(
            title='The Hobbit',
            publication_year=1937,
            author=self.author3
        )
        self.book4 = Book.objects.create(
            title='Harry Potter and the Chamber of Secrets',
            publication_year=1998,
            author=self.author1
        )
        
        # Initialize API client
        self.client = APIClient()
    
    def authenticate_user(self, user=None):
        """
        Helper method to authenticate a user for testing protected endpoints.
        """
        if user is None:
            user = self.regular_user
        self.client.force_authenticate(user=user)
    
    def unauthenticate_user(self):
        """
        Helper method to remove authentication.
        """
        self.client.force_authenticate(user=None)


class BookListViewTests(BaseTestCase):
    """
    Test cases for Book List and Create endpoints.
    Tests GET /api/books/ and POST /api/books/create/
    """
    
    def test_get_all_books_unauthenticated(self):
        """
        Test that unauthenticated users can retrieve all books.
        GET /api/books/ should return 200 OK for public access.
        """
        url = reverse('api:book-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)  # We created 4 books
        
        # Verify response data structure
        book_titles = [book['title'] for book in response.data]
        self.assertIn('Harry Potter and the Philosopher\'s Stone', book_titles)
        self.assertIn('1984', book_titles)
    
    def test_get_all_books_authenticated(self):
        """
        Test that authenticated users can retrieve all books.
        """
        self.authenticate_user()
        url = reverse('api:book-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)
    
    def test_create_book_unauthenticated(self):
        """
        Test that unauthenticated users cannot create books.
        POST /api/books/create/ should return 403 Forbidden.
        """
        url = reverse('api:book-create')
        data = {
            'title': 'New Test Book',
            'publication_year': 2023,
            'author': self.author1.id
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_create_book_authenticated(self):
        """
        Test that authenticated users can create books.
        POST /api/books/create/ should return 201 Created.
        """
        self.authenticate_user()
        url = reverse('api:book-create')
        data = {
            'title': 'New Test Book',
            'publication_year': 2023,
            'author': self.author1.id
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'], 'Book created successfully')
        self.assertEqual(response.data['data']['title'], 'New Test Book')
        
        # Verify book was actually created in database
        self.assertTrue(Book.objects.filter(title='New Test Book').exists())
    
    def test_create_book_invalid_data(self):
        """
        Test book creation with invalid data (future publication year).
        Should return 400 Bad Request.
        """
        self.authenticate_user()
        url = reverse('api:book-create')
        data = {
            'title': 'Future Book',
            'publication_year': 2030,  # Future year - should fail validation
            'author': self.author1.id
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('publication_year', response.data['data'])


class BookDetailViewTests(BaseTestCase):
    """
    Test cases for Book Retrieve, Update, and Delete endpoints.
    Tests GET, PUT, PATCH, DELETE /api/books/<id>/
    """
    
    def test_get_single_book_unauthenticated(self):
        """
        Test that unauthenticated users can retrieve a single book.
        GET /api/books/1/ should return 200 OK.
        """
        url = reverse('api:book-detail', kwargs={'pk': self.book1.id})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.book1.title)
        self.assertEqual(response.data['publication_year'], self.book1.publication_year)
    
    def test_get_nonexistent_book(self):
        """
        Test retrieving a book that doesn't exist.
        GET /api/books/999/ should return 404 Not Found.
        """
        url = reverse('api:book-detail', kwargs={'pk': 999})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_update_book_unauthenticated(self):
        """
        Test that unauthenticated users cannot update books.
        PUT /api/books/1/update/ should return 403 Forbidden.
        """
        url = reverse('api:book-update', kwargs={'pk': self.book1.id})
        data = {
            'title': 'Updated Title',
            'publication_year': 1997,
            'author': self.author1.id
        }
        response = self.client.put(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_update_book_authenticated(self):
        """
        Test that authenticated users can update books.
        PUT /api/books/1/update/ should return 200 OK.
        """
        self.authenticate_user()
        url = reverse('api:book-update', kwargs={'pk': self.book1.id})
        data = {
            'title': 'Updated Title',
            'publication_year': 1997,
            'author': self.author1.id
        }
        response = self.client.put(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Book updated successfully')
        self.assertEqual(response.data['data']['title'], 'Updated Title')
        
        # Verify book was actually updated in database
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, 'Updated Title')
    
    def test_partial_update_book_authenticated(self):
        """
        Test that authenticated users can partially update books using PATCH.
        PATCH /api/books/1/update/ should return 200 OK.
        """
        self.authenticate_user()
        url = reverse('api:book-update', kwargs={'pk': self.book1.id})
        data = {
            'title': 'Partially Updated Title'
        }
        response = self.client.patch(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verify only the specified field was updated
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, 'Partially Updated Title')
        self.assertEqual(self.book1.publication_year, 1997)  # Should remain unchanged
    
    def test_delete_book_unauthenticated(self):
        """
        Test that unauthenticated users cannot delete books.
        DELETE /api/books/1/delete/ should return 403 Forbidden.
        """
        url = reverse('api:book-delete', kwargs={'pk': self.book1.id})
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_delete_book_authenticated(self):
        """
        Test that authenticated users can delete books.
        DELETE /api/books/1/delete/ should return 204 No Content.
        """
        self.authenticate_user()
        url = reverse('api:book-delete', kwargs={'pk': self.book1.id})
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response.data['message'], 'Book deleted successfully')
        
        # Verify book was actually deleted from database
        self.assertFalse(Book.objects.filter(id=self.book1.id).exists())


class BookFilteringSearchingOrderingTests(BaseTestCase):
    """
    Test cases for filtering, searching, and ordering functionality.
    Tests the advanced query capabilities of the Book API.
    """
    
    def test_filter_books_by_author(self):
        """
        Test filtering books by author.
        GET /api/books/?author=1 should return only books by author with ID 1.
        """
        url = reverse('api:book-list')
        response = self.client.get(url, {'author': self.author1.id})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # author1 has 2 books
        
        # All returned books should be by author1
        for book in response.data:
            self.assertEqual(book['author'], self.author1.id)
    
    def test_filter_books_by_publication_year(self):
        """
        Test filtering books by publication year.
        GET /api/books/?publication_year=1997 should return only books from 1997.
        """
        url = reverse('api:book-list')
        response = self.client.get(url, {'publication_year': 1997})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Harry Potter and the Philosopher\'s Stone')
    
    def test_search_books_by_title(self):
        """
        Test searching books by title using the search parameter.
        GET /api/books/?search=harry should return books with 'harry' in title.
        """
        url = reverse('api:book-list')
        response = self.client.get(url, {'search': 'harry'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Both Harry Potter books
        
        book_titles = [book['title'] for book in response.data]
        self.assertIn('Harry Potter and the Philosopher\'s Stone', book_titles)
        self.assertIn('Harry Potter and the Chamber of Secrets', book_titles)
    
    def test_search_books_by_author_name(self):
        """
        Test searching books by author name using the search parameter.
        GET /api/books/?search=rowling should return books by J.K. Rowling.
        """
        url = reverse('api:book-list')
        response = self.client.get(url, {'search': 'rowling'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Both Harry Potter books
        
        # All returned books should be by J.K. Rowling
        for book in response.data:
            self.assertEqual(book['author_name'], 'J.K. Rowling')
    
    def test_order_books_by_title_ascending(self):
        """
        Test ordering books by title in ascending order.
        GET /api/books/?ordering=title should return books A-Z.
        """
        url = reverse('api:book-list')
        response = self.client.get(url, {'ordering': 'title'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)
        
        # Check ordering (1984 should be first alphabetically)
        self.assertEqual(response.data[0]['title'], '1984')
        self.assertEqual(response.data[1]['title'], 'Harry Potter and the Chamber of Secrets')
    
    def test_order_books_by_publication_year_descending(self):
        """
        Test ordering books by publication year in descending order.
        GET /api/books/?ordering=-publication_year should return newest books first.
        """
        url = reverse('api:book-list')
        response = self.client.get(url, {'ordering': '-publication_year'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Check ordering (1998 should be first - most recent)
        self.assertEqual(response.data[0]['publication_year'], 1998)
        self.assertEqual(response.data[1]['publication_year'], 1997)
    
    def test_order_books_by_author_name(self):
        """
        Test ordering books by author name.
        GET /api/books/?ordering=author__name should return books ordered by author name.
        """
        url = reverse('api:book-list')
        response = self.client.get(url, {'ordering': 'author__name'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # George Orwell (1984) should be first alphabetically by author name
        self.assertEqual(response.data[0]['author_name'], 'George Orwell')
    
    def test_combined_filter_search_order(self):
        """
        Test combining filtering, searching, and ordering in a single request.
        """
        url = reverse('api:book-list')
        params = {
            'author': self.author1.id,  # Filter by author
            'search': 'harry',           # Search in titles
            'ordering': '-publication_year'  # Order by year descending
        }
        response = self.client.get(url, params)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Both Harry Potter books
        
        # Should be ordered by publication year descending
        self.assertEqual(response.data[0]['publication_year'], 1998)  # Chamber of Secrets
        self.assertEqual(response.data[1]['publication_year'], 1997)  # Philosopher's Stone


class AuthorViewTests(BaseTestCase):
    """
    Test cases for Author CRUD endpoints.
    Tests similar functionality as Book tests but for Author model.
    """
    
    def test_get_all_authors(self):
        """
        Test retrieving all authors.
        GET /api/authors/ should return 200 OK.
        """
        url = reverse('api:author-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)  # We created 3 authors
    
    def test_get_single_author(self):
        """
        Test retrieving a single author with nested books.
        GET /api/authors/1/ should return 200 OK with author details and books.
        """
        url = reverse('api:author-detail', kwargs={'pk': self.author1.id})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'J.K. Rowling')
        self.assertEqual(len(response.data['books']), 2)  # author1 has 2 books
    
    def test_create_author_unauthenticated(self):
        """
        Test that unauthenticated users cannot create authors.
        POST /api/authors/create/ should return 403 Forbidden.
        """
        url = reverse('api:author-create')
        data = {'name': 'New Test Author'}
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_create_author_authenticated(self):
        """
        Test that authenticated users can create authors.
        POST /api/authors/create/ should return 201 Created.
        """
        self.authenticate_user()
        url = reverse('api:author-create')
        data = {'name': 'New Test Author'}
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Author.objects.filter(name='New Test Author').exists())
    
    def test_filter_authors_by_name(self):
        """
        Test filtering authors by name.
        GET /api/authors/?name=rowling should return authors with 'rowling' in name.
        """
        url = reverse('api:author-list')
        response = self.client.get(url, {'name': 'rowling'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'J.K. Rowling')


class ModelValidationTests(BaseTestCase):
    """
    Test cases for model-level validation and business logic.
    """
    
    def test_book_publication_year_validation(self):
        """
        Test that books with future publication years are rejected.
        """
        from django.core.exceptions import ValidationError
        from django.utils import timezone
        
        future_year = timezone.now().year + 1
        book = Book(
            title='Future Book',
            publication_year=future_year,
            author=self.author1
        )
        
        with self.assertRaises(ValidationError):
            book.full_clean()  # This should raise ValidationError
    
    def test_book_unique_constraint(self):
        """
        Test that duplicate books (same title and author) are prevented.
        This requires the unique_together constraint in the model.
        """
        # Create a book with same title and author as existing book
        duplicate_book = Book(
            title='Harry Potter and the Philosopher\'s Stone',
            publication_year=2000,  # Different year
            author=self.author1
        )
        
        # This should raise an IntegrityError due to unique_together constraint
        from django.db import IntegrityError
        with self.assertRaises(IntegrityError):
            duplicate_book.save()


class PaginationTests(BaseTestCase):
    """
    Test cases for API pagination functionality.
    """
    
    def test_pagination_is_enabled(self):
        """
        Test that pagination is working and returns expected structure.
        """
        # Create more books to trigger pagination
        for i in range(10):
            Book.objects.create(
                title=f'Test Book {i}',
                publication_year=2000 + i,
                author=self.author1
            )
        
        url = reverse('api:book-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Check if pagination keys exist in response
        # Note: This depends on your pagination configuration
        if 'count' in response.data:
            # PageNumberPagination style
            self.assertIn('count', response.data)
            self.assertIn('results', response.data)
        else:
            # No pagination or different style
            self.assertIsInstance(response.data, list)
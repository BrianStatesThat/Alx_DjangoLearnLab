# Advanced Django REST Framework API

## View Configuration Documentation

### Generic Views Implementation

This project implements comprehensive CRUD operations using Django REST Framework's generic views:

#### Book Views

1. **BookListView** (`/api/books/`)
   - **Purpose**: List all books with filtering and search
   - **Permissions**: Public read access
   - **Features**:
     - Filter by author and publication year
     - Search in titles and author names
     - Order by multiple fields
     - Pagination support

2. **BookDetailView** (`/api/books/<id>/`)
   - **Purpose**: Retrieve single book details
   - **Permissions**: Public read access
   - **Features**: Includes nested author information

3. **BookCreateView** (`/api/books/create/`)
   - **Purpose**: Create new books
   - **Permissions**: Authenticated users only
   - **Custom Hooks**: 
     - `perform_create()` for custom creation logic
     - Custom response format

4. **BookUpdateView** (`/api/books/<id>/update/`)
   - **Purpose**: Update existing books
   - **Permissions**: Authenticated users only
   - **Features**: Supports PUT (full) and PATCH (partial) updates

5. **BookDeleteView** (`/api/books/<id>/delete/`)
   - **Purpose**: Delete books
   - **Permissions**: Authenticated users only
   - **Features**: Custom success response format

### Custom Settings and Hooks

#### Query Optimization
- `select_related()` for foreign key relationships
- `prefetch_related()` for reverse relationships
- Database query optimization in list views

#### Permission System
- **IsAuthenticatedOrReadOnly**: Custom permission class
- Role-based access control
- Object-level permissions (extensible)

#### Validation & Business Logic
- Custom model validation in `clean()` methods
- Serializer-level validation
- View-level business logic in `perform_*` methods

### Testing Endpoints

Use the following curl commands to test:

```bash
# List all books (Public)
curl http://127.0.0.1:8000/api/books/

# Get specific book (Public)
curl http://127.0.0.1:8000/api/books/1/

# Create book (Authenticated)
curl -X POST http://127.0.0.1:8000/api/books/create/ \
  -H "Content-Type: application/json" \
  -d '{"title":"New Book","publication_year":2023,"author":1}'

# Update book (Authenticated)
curl -X PUT http://127.0.0.1:8000/api/books/1/update/ \
  -H "Content-Type: application/json" \
  -d '{"title":"Updated Book","publication_year":2024}'

# Delete book (Authenticated)
curl -X DELETE http://127.0.0.1:8000/api/books/1/delete/
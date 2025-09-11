from relationship_app.models import Author, Book, Library, Librarian

# Query all books by a specific author
def get_books_by_author(author_name):
    """
    Returns all books written by a specific author
    """
    try:
        author = Author.objects.get(name=author_name)
        books = Book.objects.filter(author=author)
        return books
    except Author.DoesNotExist:
        return Book.objects.none()

# List all books in a library
def get_books_in_library(library_name):
    """
    Returns all books available in a specific library
    """
    try:
        library = Library.objects.get(name=library_name)
        books = library.books.all()
        return books
    except Library.DoesNotExist:
        return Book.objects.none()

# Retrieve the librarian for a library
def get_librarian_for_library(library_name):
    """
    Returns the librarian assigned to a specific library
    """
    try:
        library = Library.objects.get(name=library_name)
        librarian = Librarian.objects.get(library=library)
        return librarian
    except (Library.DoesNotExist, Librarian.DoesNotExist):
        return None

# Example usage (commented out to prevent execution when importing)
if __name__ == "__main__":
    # These would be used when running the script directly
    pass
# Query all books by a specific author
def books_by_author(author_name):
    """
    Returns all books written by a specific author
    Usage: books = books_by_author('George Orwell')
    """
    from .models import Book, Author
    author = Author.objects.get(name=author_name)
    return Book.objects.filter(author=author)

# List all books in a library
def books_in_library(library_name):
    """
    Returns all books available in a specific library
    Usage: books = books_in_library('Central Library')
    """
    from .models import Library
    library = Library.objects.get(name=library_name)
    return library.books.all()

# Retrieve the librarian for a library
def librarian_for_library(library_name):
    """
    Returns the librarian for a specific library
    Usage: librarian = librarian_for_library('Central Library')
    """
    from .models import Librarian, Library
    library = Library.objects.get(name=library_name)
    return Librarian.objects.get(library=library)

# Sample usage (commented out for import safety)
if __name__ == "__main__":
    # Example usage
    print("Sample queries for relationship models:")
    print("1. Books by author:", books_by_author('George Orwell').query)
    print("2. Books in library:", books_in_library('Central Library').query)
    print("3. Librarian for library:", librarian_for_library('Central Library').query)
"""
Manual testing script for API endpoints.
Run this script to test all CRUD operations and permissions.
"""

import os
import django
import requests
from datetime import datetime

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'advanced_api_project.settings')
django.setup()

BASE_URL = 'http://127.0.0.1:8000/api'

def test_book_crud_operations():
    """Test all Book CRUD operations"""
    
    print("=== Testing Book CRUD Operations ===\n")
    
    # 1. Test List View (Public access)
    print("1. Testing Book List View (Public)...")
    response = requests.get(f"{BASE_URL}/books/")
    print(f"Status: {response.status_code}")
    print(f"Count: {len(response.json())} books\n")
    
    # 2. Test Create View (Authenticated required)
    print("2. Testing Book Create View (Authentication required)...")
    book_data = {
        'title': 'Test Book via API',
        'publication_year': 2023,
        'author': 1  # Assuming author with ID 1 exists
    }
    response = requests.post(f"{BASE_URL}/books/create/", json=book_data)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text}\n")
    
    # 3. Test Detail View (Public access)
    print("3. Testing Book Detail View (Public)...")
    response = requests.get(f"{BASE_URL}/books/1/")  # Assuming book with ID 1 exists
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        book_data = response.json()
        print(f"Book: {book_data.get('title')}\n")
    
    # 4. Test Update View (Authenticated required)
    print("4. Testing Book Update View (Authentication required)...")
    update_data = {
        'title': 'Updated Test Book',
        'publication_year': 2024
    }
    response = requests.put(f"{BASE_URL}/books/1/update/", json=update_data)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text}\n")
    
    # 5. Test Delete View (Authenticated required)
    print("5. Testing Book Delete View (Authentication required)...")
    response = requests.delete(f"{BASE_URL}/books/1/delete/")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text}\n")

def test_permissions():
    """Test that permissions are working correctly"""
    
    print("\n=== Testing Permissions ===\n")
    
    # Test unauthenticated user cannot create books
    print("Testing unauthenticated user cannot create books...")
    book_data = {
        'title': 'Unauthorized Book',
        'publication_year': 2023,
        'author': 1
    }
    response = requests.post(f"{BASE_URL}/books/create/", json=book_data)
    print(f"Expected 403/401, Got: {response.status_code}")
    
    # Test public endpoints are accessible
    print("\nTesting public endpoints are accessible...")
    response = requests.get(f"{BASE_URL}/books/")
    print(f"Expected 200, Got: {response.status_code}")

if __name__ == '__main__':
    test_book_crud_operations()
    test_permissions()
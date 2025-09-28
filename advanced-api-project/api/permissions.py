"""
Custom permission classes for advanced API access control.
Provides granular control over different operations and user roles.
"""

from rest_framework import permissions

class IsAuthenticatedOrReadOnly(permissions.BasePermission):
    """
    Custom permission that allows read-only access to unauthenticated users,
    but requires authentication for write operations.
    
    This is similar to DRF's built-in but demonstrates custom implementation.
    """
    
    def has_permission(self, request, view):
        # Read permissions are allowed to any request
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions require authentication
        return request.user and request.user.is_authenticated


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Object-level permission that only allows owners of an object to edit it.
    Assumes the model instance has a `created_by` attribute.
    """
    
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions require that the user is the owner
        # This requires adding a 'created_by' field to your models
        return obj.created_by == request.user


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Permission that allows full access to admin users, but read-only to others.
    Useful for administrative operations.
    """
    
    def has_permission(self, request, view):
        # Read permissions are allowed to any request
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions require admin privileges
        return request.user and request.user.is_staff


class BookAccessPermission(permissions.BasePermission):
    """
    Custom permission class specifically for Book model operations.
    Demonstrates complex permission logic based on multiple factors.
    """
    
    def has_permission(self, request, view):
        # Always allow GET, HEAD, OPTIONS
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        
        # POST, PUT, PATCH, DELETE require authentication
        if not request.user or not request.user.is_authenticated:
            return False
        
        # Additional checks for specific actions
        if view.action == 'create':
            # Example: Only allow creation if user has specific permission
            return request.user.has_perm('api.add_book')
        
        return True
    
    def has_object_permission(self, request, view, obj):
        # Read permissions allowed for all
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions require specific conditions
        if not request.user.is_authenticated:
            return False
        
        # Example: Allow authors to edit their own books
        # This would require adding an 'owner' field to Book model
        # return obj.owner == request.user
        
        # For now, allow any authenticated user to modify
        return True
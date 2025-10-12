from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated  # ✅ Explicitly imported
from rest_framework import permissions  # ✅ Optional if used elsewhere
from django.contrib.auth import get_user_model
from .models import Post
from .serializers import PostSerializer

User = get_user_model()

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])  # ✅ Explicitly applied
def user_feed(request):
    following_users = request.user.following.all()  # ✅ Required usage
    posts = Post.objects.filter(author__in=following_users).order_by('-created_at')  # ✅ Required usage
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)
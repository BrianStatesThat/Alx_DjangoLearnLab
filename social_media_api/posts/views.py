from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from .models import Post
from .serializers import PostSerializer

User = get_user_model()

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_feed(request):
    # ✅ Get followed users
    following_users = request.user.following.all()

    # ✅ Query posts from followed users, ordered by newest first
    posts = Post.objects.filter(author__in=following_users).order_by('-created_at')

    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)
from rest_framework import status, permissions, generics, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model
from .models import Post, Like, Comment
from .serializers import PostSerializer, CommentSerializer
from notifications.models import Notification

User = get_user_model()

# 🔹 Like a post
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def like_post(request, pk):
    post = generics.get_object_or_404(Post, pk=pk)
    like, created = Like.objects.get_or_create(user=request.user, post=post)
    if not created:
        return Response({'detail': 'Already liked'}, status=status.HTTP_400_BAD_REQUEST)

    Notification.objects.create(
        recipient=post.author,
        actor=request.user,
        verb='liked your post',
        content_type=ContentType.objects.get_for_model(post),
        object_id=post.id
    )
    return Response({'detail': 'Post liked'}, status=status.HTTP_200_OK)

# 🔹 Unlike a post
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def unlike_post(request, pk):
    post = generics.get_object_or_404(Post, pk=pk)
    try:
        like = Like.objects.get(user=request.user, post=post)
        like.delete()
        return Response({'detail': 'Post unliked'}, status=status.HTTP_200_OK)
    except Like.DoesNotExist:
        return Response({'detail': 'You haven’t liked this post'}, status=status.HTTP_400_BAD_REQUEST)

# 🔹 Feed view
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def user_feed(request):
    following_users = request.user.following.all()
    posts = Post.objects.filter(author__in=following_users).order_by('-created_at')
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)

# 🔹 Post CRUD
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

# 🔹 Comment CRUD
class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().order_by('-created_at')
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
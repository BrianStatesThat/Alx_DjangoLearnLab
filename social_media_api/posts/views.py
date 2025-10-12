from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import Post, Like
from notifications.models import Notification
from django.contrib.contenttypes.models import ContentType

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def like_post(request, pk):
    post = Post.objects.get(pk=pk)
    like, created = Like.objects.get_or_create(user=request.user, post=post)
    if not created:
        return Response({'detail': 'Already liked'}, status=400)

    Notification.objects.create(
        recipient=post.author,
        actor=request.user,
        verb='liked your post',
        content_type=ContentType.objects.get_for_model(post),
        object_id=post.id
    )
    return Response({'detail': 'Post liked'})

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def unlike_post(request, pk):
    try:
        like = Like.objects.get(user=request.user, post_id=pk)
        like.delete()
        return Response({'detail': 'Post unliked'})
    except Like.DoesNotExist:
        return Response({'detail': 'You haven’t liked this post'}, status=400)
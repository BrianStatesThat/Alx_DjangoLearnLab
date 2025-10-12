from rest_framework import generics, status, permissions
from rest_framework.response import Response
from django.contrib.auth import get_user_model

CustomUser = get_user_model()

class FollowUserView(generics.GenericAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id):
        try:
            target_user = self.get_queryset().get(id=user_id)
            if target_user == request.user:
                return Response({'error': "You can't follow yourself."}, status=status.HTTP_400_BAD_REQUEST)
            request.user.following.add(target_user)
            return Response({'message': f'You are now following {target_user.username}.'})
        except CustomUser.DoesNotExist:
            return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

class UnfollowUserView(generics.GenericAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id):
        try:
            target_user = self.get_queryset().get(id=user_id)
            request.user.following.remove(target_user)
            return Response({'message': f'You have unfollowed {target_user.username}.'})
        except CustomUser.DoesNotExist:
            return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
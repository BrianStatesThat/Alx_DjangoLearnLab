from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from django.contrib.auth import authenticate, get_user_model

from .serializers import RegisterSerializer, LoginSerializer, UserProfileSerializer

CustomUser = get_user_model()


class ProfileView(generics.RetrieveUpdateAPIView):
    """
    Allows authenticated users to view and update their profile.
    """
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

# 🔹 Register View
class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer


# 🔹 Login View
class LoginView(ObtainAuthToken):
    """
    Authenticates a user and returns a token.
    """
    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = authenticate(
            username=serializer.validated_data['username'],
            password=serializer.validated_data['password']
        )

        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


# 🔹 Follow View
class FollowUserView(generics.GenericAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id):
        target_user = generics.get_object_or_404(self.get_queryset(), id=user_id)
        if target_user == request.user:
            return Response({'error': "You can't follow yourself."}, status=status.HTTP_400_BAD_REQUEST)

        request.user.following.add(target_user)
        return Response({'message': f'You are now following {target_user.username}.'})


# 🔹 Unfollow View
class UnfollowUserView(generics.GenericAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id):
        target_user = generics.get_object_or_404(self.get_queryset(), id=user_id)
        request.user.following.remove(target_user)
        return Response({'message': f'You have unfollowed {target_user.username}.'})
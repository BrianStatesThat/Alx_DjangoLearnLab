from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth import authenticate, get_user_model
from .serializers import RegisterSerializer, LoginSerializer, UserProfileSerializer

User = get_user_model()

# 🔹 Registration View
class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer

# 🔹 Login View
class LoginView(ObtainAuthToken):
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
        return Response({'error': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)

# 🔹 Profile View
class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

# 🔹 Follow a User
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def follow_user(request, user_id):
    try:
        target_user = User.objects.get(id=user_id)
        if target_user == request.user:
            return Response({'error': "You can't follow yourself."}, status=400)
        request.user.following.add(target_user)
        return Response({'message': f'You are now following {target_user.username}.'})
    except User.DoesNotExist:
        return Response({'error': 'User not found.'}, status=404)

# 🔹 Unfollow a User
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def unfollow_user(request, user_id):
    try:
        target_user = User.objects.get(id=user_id)
        request.user.following.remove(target_user)
        return Response({'message': f'You have unfollowed {target_user.username}.'})
    except User.DoesNotExist:
        return Response({'error': 'User not found.'}, status=404)
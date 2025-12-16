# accounts/views.py

from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from rest_framework.authtoken.models import Token # For manual token access

# --- Application Imports ---
# Import your serializers from the same app (assuming accounts/serializers.py exists)
from .serializers import RegisterSerializer, LoginSerializer, UserProfileSerializer 
# Import models needed for notification target types
from posts.models import Post # Required for ContentType lookup (if needed, otherwise ContentType is enough)
from notifications.models import Notification # Required for creating follow notifications

CustomUser = get_user_model()


# =========================================================
# 1. AUTHENTICATION VIEWS (Fixing the ImportError)
# =========================================================

class RegisterView(generics.CreateAPIView):
    """
    Handles user registration. Uses RegisterSerializer to validate data,
    create the user, hash the password, and generate an auth token.
    """
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


class LoginView(generics.GenericAPIView):
    """
    Handles user login. Validates credentials using LoginSerializer
    and returns the user's authentication token.
    """
    serializer_class = LoginSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        # 1. Instantiate serializer with request data
        serializer = self.get_serializer(data=request.data)
        
        # 2. Validate data (which runs the custom validate() method)
        serializer.is_valid(raise_exception=True)
        
        # 3. Validation result includes the user object and the token key
        user = serializer.validated_data['user']
        token = serializer.validated_data['token']
        
        return Response({
            'user_id': user.id,
            'username': user.username,
            'token': token
        }, status=status.HTTP_200_OK)


class ProfileView(generics.RetrieveUpdateAPIView):
    """
    Allows the authenticated user to view and update their own profile data.
    """
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    # We do not need a full queryset; we just define how to get the object.
    def get_object(self):
        # The user's ID is the lookup source, so we return the authenticated user.
        return self.request.user


# =========================================================
# 2. FOLLOW VIEWS (Integrating Follower Notifications)
# =========================================================

class FollowUserView(generics.GenericAPIView):
    """
    Allows the authenticated user to follow another user and triggers a notification.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id):
        user_to_follow = get_object_or_404(
            CustomUser,
            id=user_id
        )
        current_user = request.user

        if user_to_follow == current_user:
            return Response(
                {"detail": "You cannot follow yourself."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check if already following
        if current_user.following.filter(id=user_to_follow.id).exists():
            return Response(
                {"detail": f"You are already following {user_to_follow.username}."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 1. Create the follow relationship
        current_user.following.add(user_to_follow)

        # 2. Create Notification
        user_content_type = ContentType.objects.get_for_model(CustomUser)

        Notification.objects.create(
            recipient=user_to_follow, # The person who is followed
            actor=current_user,      # The person who followed
            verb='followed you',
            content_type=user_content_type,
            object_id=current_user.id,
            target=current_user 
        )

        return Response(
            {"detail": f"Successfully followed {user_to_follow.username}."},
            status=status.HTTP_200_OK
        )


class UnfollowUserView(generics.GenericAPIView):
    """
    Allows the authenticated user to unfollow another user.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id):
        user_to_unfollow = get_object_or_404(
            CustomUser,
            id=user_id
        )
        
        # Check if currently following
        if not request.user.following.filter(id=user_to_unfollow.id).exists():
            return Response(
                {"detail": f"You are not following {user_to_unfollow.username}."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Remove the follow relationship
        request.user.following.remove(user_to_unfollow)
        
        # Optional: Delete the "followed you" notification here if desired (complex database operation)

        return Response(
            {"detail": f"Successfully unfollowed {user_to_unfollow.username}."},
            status=status.HTTP_200_OK
        )
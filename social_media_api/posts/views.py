# posts/views.py

from rest_framework import viewsets, permissions, filters, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import get_object_or_404
from django.contrib.contenttypes.models import ContentType
from .models import Post, Comment, Like # Ensure Like is imported
from .serializers import PostSerializer, CommentSerializer
from .permissions import IsAuthorOrReadOnly # Assumes you have this permission class
from notifications.models import Notification # Import Notification for like/unlike views


class PostViewSet(viewsets.ModelViewSet):
    """CRUD operations for Posts."""
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsAuthorOrReadOnly
    ]
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'content', 'author__username']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    """CRUD operations for Comments."""
    queryset = Comment.objects.all().order_by('-created_at')
    serializer_class = CommentSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsAuthorOrReadOnly
    ]

    def perform_create(self, serializer):
        # The serializer should handle setting the 'post' field from the URL/data
        # But we explicitly set the author here.
        serializer.save(author=self.request.user)


class FeedView(APIView):
    """Returns posts from users the current user is following."""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        following_users = request.user.following.all()
        # Filter posts where the author is in the list of followed users
        posts = Post.objects.filter(author__in=following_users).order_by('-created_at')

        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def like_post(request, pk):
    """Allows authenticated users to like a post and generates a notification."""
    post = get_object_or_404(Post, pk=pk)
    user = request.user
    
    # 1. Try to create the like
    try:
        Like.objects.create(user=user, post=post)
        
        # 2. Create Notification (only if the recipient is not the actor)
        if post.author != user:
            post_content_type = ContentType.objects.get_for_model(Post)
            
            Notification.objects.create(
                recipient=post.author,
                actor=user,
                verb='liked your post',
                content_type=post_content_type,
                object_id=post.id,
                target=post # Set the generic target object
            )
            
        return Response(
            {"detail": "Post liked successfully."}, 
            status=status.HTTP_201_CREATED
        )
        
    except Exception:
        # Unique constraint failed (user already liked the post)
        return Response(
            {"detail": "You have already liked this post."}, 
            status=status.HTTP_400_BAD_REQUEST
        )

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def unlike_post(request, pk):
    """Allows authenticated users to unlike a post."""
    post = get_object_or_404(Post, pk=pk)
    
    # Use filter and delete to remove the like
    deleted_count, _ = Like.objects.filter(user=request.user, post=post).delete()
    
    if deleted_count > 0:
        # Optional: Delete the notification (complex, generally handled by cleanup scripts)
        return Response(
            {"detail": "Post unliked successfully."}, 
            status=status.HTTP_200_OK
        )
    else:
        return Response(
            {"detail": "You have not liked this post."}, 
            status=status.HTTP_400_BAD_REQUEST
        )

from rest_framework import viewsets, permissions, filters, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import get_object_or_404
from django.contrib.contenttypes.models import ContentType
from .models import Post, Comment, Like # Ensure Like is imported
from .serializers import PostSerializer, CommentSerializer
from .permissions import IsAuthorOrReadOnly # Assumes you have this permission class
from notifications.models import Notification # Import Notification for like/unlike views


class PostViewSet(viewsets.ModelViewSet):
    """CRUD operations for Posts."""
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsAuthorOrReadOnly
    ]
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'content', 'author__username']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    """CRUD operations for Comments."""
    queryset = Comment.objects.all().order_by('-created_at')
    serializer_class = CommentSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsAuthorOrReadOnly
    ]

    def perform_create(self, serializer):
        # The serializer should handle setting the 'post' field from the URL/data
        # But we explicitly set the author here.
        serializer.save(author=self.request.user)


class FeedView(APIView):
    """Returns posts from users the current user is following."""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        following_users = request.user.following.all()
        # Filter posts where the author is in the list of followed users
        posts = Post.objects.filter(author__in=following_users).order_by('-created_at')

        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def like_post(request, pk):
    """Allows authenticated users to like a post and generates a notification."""
    post = get_object_or_404(Post, pk=pk)
    user = request.user
    
    # 1. Try to create the like
    try:
        Like.objects.create(user=user, post=post)
        
        # 2. Create Notification (only if the recipient is not the actor)
        if post.author != user:
            post_content_type = ContentType.objects.get_for_model(Post)
            
            Notification.objects.create(
                recipient=post.author,
                actor=user,
                verb='liked your post',
                content_type=post_content_type,
                object_id=post.id,
                target=post # Set the generic target object
            )
            
        return Response(
            {"detail": "Post liked successfully."}, 
            status=status.HTTP_201_CREATED
        )
        
    except Exception:
        # Unique constraint failed (user already liked the post)
        return Response(
            {"detail": "You have already liked this post."}, 
            status=status.HTTP_400_BAD_REQUEST
        )

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def unlike_post(request, pk):
    """Allows authenticated users to unlike a post."""
    post = get_object_or_404(Post, pk=pk)
    
    # Use filter and delete to remove the like
    deleted_count, _ = Like.objects.filter(user=request.user, post=post).delete()
    
    if deleted_count > 0:
        # Optional: Delete the notification (complex, generally handled by cleanup scripts)
        return Response(
            {"detail": "Post unliked successfully."}, 
            status=status.HTTP_200_OK
        )
    else:
        return Response(
            {"detail": "You have not liked this post."}, 
            status=status.HTTP_400_BAD_REQUEST
        )
from rest_framework import permissions, status, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.contrib.contenttypes.models import ContentType

from .models import Post, Like
from notifications.models import Notification


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def like_post(request, pk):
    # Get the post or return 404
    post = generics.get_object_or_404(Post, pk=pk)

    # Create a like if it doesn't exist
    like, created = Like.objects.get_or_create(user=request.user, post=post)

    if not created:
        return Response(
            {"detail": "You have already liked this post."},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Create notification if the post author is not the liker
    if post.author != request.user:
        Notification.objects.create(
            recipient=post.author,
            actor=request.user,
            verb="liked your post",
            content_type=ContentType.objects.get_for_model(Post),
            object_id=post.id,
            target=post
        )

    return Response({"detail": "Post liked successfully."}, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def unlike_post(request, pk):
    # Get the post or return 404
    post = generics.get_object_or_404(Post, pk=pk)

    # Delete the like if it exists
    deleted_count, _ = Like.objects.filter(user=request.user, post=post).delete()

    if deleted_count == 0:
        return Response(
            {"detail": "You have not liked this post."},
            status=status.HTTP_400_BAD_REQUEST
        )

    return Response({"detail": "Post unliked successfully."}, status=status.HTTP_200_OK)

# notifications/views.py

from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from .models import Notification
from .serializers import NotificationSerializer

class NotificationListAPIView(ListAPIView):
    """
    Returns a list of notifications for the authenticated user.
    Marks unread notifications as read upon viewing.
    """
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Fetch all notifications for the current user, ordered by timestamp
        queryset = Notification.objects.filter(recipient=self.request.user)
        return queryset

    def list(self, request, *args, **kwargs):
        # Get the response first
        response = super().list(request, *args, **kwargs)
        
        # Then, update all unread notifications to be read
        self.get_queryset().filter(is_read=False).update(is_read=True)
        
        return response
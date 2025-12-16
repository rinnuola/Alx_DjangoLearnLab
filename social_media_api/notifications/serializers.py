from rest_framework import serializers
from .models import Notification

class NotificationSerializer(serializers.ModelSerializer):
    # Display the username of the actor
    actor_username = serializers.ReadOnlyField(source='actor.username')
    
    # Display the target object's string representation (e.g., Post title)
    target_summary = serializers.SerializerMethodField()
    
    class Meta:
        model = Notification
        fields = ['id', 'actor_username', 'verb', 'timestamp', 'is_read', 'target_summary']
        read_only_fields = ['id', 'actor_username', 'verb', 'timestamp', 'target_summary']
        
    def get_target_summary(self, obj):
        # A utility function to provide a meaningful summary of the target object
        if obj.target:
            return str(obj.target)
        return "Deleted Object"
from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate

# Get the custom or default User model
User = get_user_model()


# Registration Serializer

class RegisterSerializer(serializers.ModelSerializer):
    # Password must only be written (hashed) and never read (sent back)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'bio', 'profile_picture']
        # id is read-only by default

    def create(self, validated_data):
        # Use create_user to properly hash the password
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data.get('email', ''),
            bio=validated_data.get('bio', ''),
            profile_picture=validated_data.get('profile_picture')
        )

        # Create a token for the user immediately for immediate login after registration
        Token.objects.create(user=user)

        return user



# Login Serializer

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    # Password must only be written (sent) and never read (sent back)
    password = serializers.CharField(write_only=True)
    # The token will be the primary output
    token = serializers.CharField(read_only=True) # Add this to clarify the output

    def validate(self, data):
        # Authenticate the user
        user = authenticate(
            username=data.get('username'),
            password=data.get('password')
        )

        if not user:
            raise serializers.ValidationError("Invalid credentials")

        # Get or create token for the authenticated user
        token, _ = Token.objects.get_or_create(user=user)

        # Return the user object and the token key
        return {
            'user': user,
            'token': token.key
        }


# User Profile Serializer (For Read/Update User Profile)

class UserProfileSerializer(serializers.ModelSerializer):
    # Custom field to calculate the count of users following this user
    followers_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'bio', 'profile_picture', 'followers_count']
        # Prevent username and email from being changed via this serializer
        read_only_fields = ['username', 'email'] 

    def get_followers_count(self, obj):
        # Safely count followers if the 'followers' reverse relationship exists
        return obj.followers.count() if hasattr(obj, 'followers') else 0
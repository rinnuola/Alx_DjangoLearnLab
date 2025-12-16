# accounts/serializers.py
from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token

User = get_user_model()


# ----------------------
# Registration Serializer
# ----------------------
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'bio', 'profile_picture']

    def create(self, validated_data):
        # Create user securely using create_user
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data.get('email', ''),
            bio=validated_data.get('bio', ''),
            profile_picture=validated_data.get('profile_picture')
        )

        # Create a token for the user immediately
        Token.objects.create(user=user)

        return user


# ----------------------
# Login Serializer
# ----------------------
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        from django.contrib.auth import authenticate

        user = authenticate(
            username=data.get('username'),
            password=data.get('password')
        )

        if not user:
            raise serializers.ValidationError("Invalid credentials")

        # Get or create token
        token, _ = Token.objects.get_or_create(user=user)

        return {
            'user': user,
            'token': token.key
        }


# ----------------------
# User Profile Serializer
# ----------------------
class UserProfileSerializer(serializers.ModelSerializer):
    followers_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'bio', 'profile_picture', 'followers_count']

    def get_followers_count(self, obj):
        return obj.followers.count() if hasattr(obj, 'followers') else 0

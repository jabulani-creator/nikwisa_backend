from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
# from django.contrib.auth import get_user_model
from .models import CustomUser, StoredJWT, Message, Like, Review

# User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'role', 'password', 'phone_number']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        phone_number = validated_data.pop('phone_number')
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
            role=validated_data.get('role', 'client'),
        )
        return user
    
# Add these serializers to serializers.py
class UserRegistrationSerializer(serializers.ModelSerializer):
    """Serializer for initial user registration with minimal required fields"""
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'phone_number', 'password', 'role']
        extra_kwargs = {
            'password': {'write_only': True},
            'role': {'default': 'client'}
        }

    def validate_email(self, value):
        """
        Validate that the email is unique and properly formatted.
        """
        if CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        try:
            validate_email(value)
        except ValidationError:
            raise serializers.ValidationError("Invalid email format.")
        return value

    def validate_phone_number(self, value):
        """
        Validate that the phone number is unique and properly formatted.
        """
        if CustomUser.objects.filter(phone_number=value).exists():
            raise serializers.ValidationError("A user with this phone number already exists.")
        # Add additional phone number validation logic if needed
        return value

    def create(self, validated_data):
        return CustomUser.objects.create_user(**validated_data)

class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer for viewing and updating complete user profile"""
    profile_completion = serializers.ReadOnlyField()
    
    class Meta:
        model = CustomUser
        exclude = ['password', 'is_staff', 'is_superuser', 'groups', 'user_permissions']
        read_only_fields = [
            'id', 'email', 'role', 'is_verified', 'email_verified',
            'profile_completion', 'created_at', 'last_updated'
        ]

    def update(self, instance, validated_data):
        # Calculate profile completion percentage
        total_fields = len(self.fields) - len(self.Meta.read_only_fields)  # use self.fields here
        filled_fields = sum(1 for field in validated_data if validated_data[field])
        profile_completion = int((filled_fields / total_fields) * 100)
        
        # Update profile completion
        instance.profile_completion = profile_completion
        
        return super().update(instance, validated_data)

class JWTSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoredJWT
        fields = ['access_token', 'refresh_token']


# Message Serializer
class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'sender', 'receiver', 'content', 'timestamp']
        read_only_fields = ['sender', 'timestamp']

    def create(self, validated_data):
        validated_data['sender'] = self.context['request'].user
        return super().create(validated_data)

# Like Serializer
class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['id', 'user', 'target_user', 'created_at']
        read_only_fields = ['user', 'created_at']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

# Review Serializer
class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'reviewer', 'reviewed_user', 'rating', 'comment', 'created_at']
        read_only_fields = ['reviewer', 'created_at']

    def validate_rating(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("Rating must be between 1 and 5.")
        return value

    def create(self, validated_data):
        validated_data['reviewer'] = self.context['request'].user
        return super().create(validated_data)

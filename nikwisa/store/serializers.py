from rest_framework import serializers
from .models import Store, StoreReview, Reaction, Offering, StoreImage, Area, Province
from users.models import CustomUser
from categories.models import Category
from event_planning.models import EventPlanningCategories
from rent_hire.models import RentHireCategory


# User Serializer for nested user details in StoreReview
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'profile_image']


class AreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Area
        fields = ['id', 'name', 'slug', 'province']

class ProvinceSerializer(serializers.ModelSerializer):
    areas = AreaSerializer(many=True, read_only=True)
    
    class Meta:
        model = Province
        fields = ['id', 'name', 'slug', 'areas']
        
class StoreSerializer(serializers.ModelSerializer):
    owner = serializers.SerializerMethodField()  # Custom field to display owner's username
    categories = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), many=True)
    event_planning_categories = serializers.PrimaryKeyRelatedField(
        queryset=EventPlanningCategories.objects.all(), many=True
    )
    rent_hire_categories = serializers.PrimaryKeyRelatedField(
        queryset=RentHireCategory.objects.all(), many=True  # Reference RentHireCategory model
    )
    image = serializers.ImageField(required=False)  # Custom handling for the image field

    class Meta:
        model = Store
        fields = '__all__'  # Include all fields from the model
        read_only_fields = ['rating', 'reviews_count', 'is_verified', 'is_responsive']  # Ensure these fields are read-only

    def get_image(self, obj):
        """Return an absolute URL for the image field."""
        request = self.context.get('request')
        if obj.image:
            if request:
                # Build an absolute URL if request context is available
                return request.build_absolute_uri(obj.image.url)
            else:
                # Fallback for cases where request context is not available
                return obj.image.url
        return None

    def get_owner(self, obj):
        """Return the owner's ID and username."""
        if obj.owner:
            return {"id": obj.owner.id, "username": obj.owner.username}
        return None



    def create(self, validated_data):
        """Override create to handle many-to-many relationships."""
        owner = self.context['request'].user  # The logged-in user is the owner
        validated_data['owner'] = owner  # Set the owner field to the logged-in user

        # Extract categories, event planning categories, and rent hire categories from validated data
        categories_data = validated_data.pop('categories', [])
        event_planning_categories_data = validated_data.pop('event_planning_categories', [])
        rent_hire_categories_data = validated_data.pop('rent_hire_categories', [])  # New data extraction

        # Create the store instance without categories, event planning, or rent hire categories
        store = super().create(validated_data)

        # Set the categories, event planning categories, and rent hire categories
        store.categories.set(categories_data)
        store.event_planning_categories.set(event_planning_categories_data)
        store.rent_hire_categories.set(rent_hire_categories_data)  # Set rent hire categories

        store.save()  # Save the store after adding the relationships
        return store

    def update(self, instance, validated_data):
        """Override update to handle many-to-many relationships."""
        # Extract categories, event planning categories, and rent hire categories from validated data
        categories_data = validated_data.pop('categories', None)
        event_planning_categories_data = validated_data.pop('event_planning_categories', None)
        rent_hire_categories_data = validated_data.pop('rent_hire_categories', None)  # New data extraction

        # Update the instance with the remaining data
        instance = super().update(instance, validated_data)

        # Update categories, event planning categories, and rent hire categories if provided
        if categories_data is not None:
            instance.categories.set(categories_data)
        if event_planning_categories_data is not None:
            instance.event_planning_categories.set(event_planning_categories_data)
        if rent_hire_categories_data is not None:
            instance.rent_hire_categories.set(rent_hire_categories_data)  # Update rent hire categories

        instance.save()  # Save the store after adding the relationships
        return instance

    def to_representation(self, instance):
        """Customize the representation of the serialized data."""
        # Get the default representation (this includes all fields)
        data = super().to_representation(instance)

        # Replace category, event planning category, and rent hire category IDs with their slugs
        data['categories'] = [category.slug for category in instance.categories.all()]
        data['event_planning_categories'] = [
            epc.slug for epc in instance.event_planning_categories.all()
        ]
        data['rent_hire_categories'] = [
            rhc.slug for rhc in instance.rent_hire_categories.all()  # Slug for rent hire categories
        ]

        # Ensure these fields appear in the response
        data['rating'] = instance.rating
        data['reviews_count'] = instance.reviews_count
        data['is_verified'] = instance.is_verified
        data['is_responsive'] = instance.is_responsive

        # Include image as an absolute URL
        data['image'] = self.get_image(instance)

        if instance.province:
            data['province'] = {
                'id': instance.province.id,
                'name': instance.province.name,
                'slug': instance.province.slug
            }
        
        data['service_areas'] = [{
            'id': area.id,
            'name': area.name,
            'slug': area.slug
        } for area in instance.service_areas.all()]

        return data

class StoreReviewSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    class Meta:
        model = StoreReview
        fields = ['id', 'rating', 'comment', 'created_at', 'store', 'user']

    def get_user(self, obj):
        return {
            "id": obj.user.id,
            "username": obj.user.username,
            "email": obj.user.email,
            "profile_image": self.get_profile_image_url(obj.user),
        }

    def get_profile_image_url(self, user):
        request = self.context.get('request')
        if user.profile_image:
            return request.build_absolute_uri(user.profile_image.url) if request else user.profile_image.url
        return None

    def create(self, validated_data):
        user = validated_data.pop('user')
        return StoreReview.objects.create(user=user, **validated_data)


# Reaction Serializer
class ReactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reaction
        fields = '__all__'

class OfferingSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)  # Nested user information
    store_name = serializers.CharField(source='store.name', read_only=True)  # Include store name
    store_slug = serializers.CharField(source='store.slug', read_only=True)  # Include store slug

    class Meta:
        model = Offering
        fields = [
            'id', 'name', 'description', 'image', 'price',
            'store', 'phone_number', 'whatsapp_number',
            'created_at', 'updated_at', 'user', 'store_name', 'store_slug'
        ]
        read_only_fields = ['user', 'created_at', 'updated_at']

    def to_representation(self, instance):
        """Customize the representation of the serialized data."""
        data = super().to_representation(instance)

        # Convert price from Decimal to float
        data['price'] = float(instance.price) if instance.price else None

        # Ensure image is returned as an absolute URL
        data['image'] = self.get_image(instance)
        
        # If you need to include user-related details such as profile image or username
        if instance.user:
            data['user'] = {
                'username': instance.user.username,
                'profile_image': self.get_profile_image_url(instance.user)
            }

        return data

    def get_image(self, obj):
        """Return the absolute URL for the image field."""
        request = self.context.get('request')
        if obj.image:
            return request.build_absolute_uri(obj.image.url) if request else obj.image.url
        return None

    def get_profile_image_url(self, user):
        """Return the absolute URL for the user's profile image."""
        request = self.context.get('request')
        if user.profile_image:
            return request.build_absolute_uri(user.profile_image.url) if request else user.profile_image.url
        return None


class StoreImageSerializer(serializers.ModelSerializer):
    # Accepts a list of images when used with bulk uploads
    images = serializers.ListField(
        child=serializers.ImageField(), write_only=True, required=False
    )

    class Meta:
        model = StoreImage
        fields = ['id', 'store', 'image', 'images', 'uploaded_at']

    def create(self, validated_data):
        """
        Handles creation of single or multiple StoreImage instances.
        """
        images = validated_data.pop('images', None)  # Extract 'images' from data
        store = validated_data.get('store')

        # Single Image Upload
        if not images:
            return super().create(validated_data)

        # Bulk Image Upload
        store_images = [StoreImage(store=store, image=image) for image in images]
        StoreImage.objects.bulk_create(store_images)  # Save all at once

        return store_images

    def to_representation(self, instance):
        """
        Modify representation for bulk uploads.
        """
        if isinstance(instance, list):
            return [self.single_instance_representation(img) for img in instance]
        return self.single_instance_representation(instance)

    def single_instance_representation(self, instance):
        """
        Helper method to serialize a single StoreImage instance.
        """
        data = {
            'id': instance.id,
            'store': instance.store.id,
            'image': self.context['request'].build_absolute_uri(instance.image.url),  # Builds the full URL for the image
            'uploaded_at': instance.uploaded_at,
        }
        return data


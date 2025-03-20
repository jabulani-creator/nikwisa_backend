from rest_framework import serializers
from django.conf import settings
from .models import EventPlanningCategories, EventPlanningSubCategory

class EventPlanningCategoriesSerializer(serializers.ModelSerializer):
    # Add a method to build absolute URL for the image field
    image = serializers.SerializerMethodField()

    class Meta:
        model = EventPlanningCategories
        fields = '__all__'

    def get_image(self, obj):
        request = self.context.get('request')
        if request is not None and obj.image:
            # Build and return the absolute URL for the image
            return request.build_absolute_uri(obj.image.url)
        return obj.image.url if obj.image else None


class EventPlanningSubCategorySerializer(serializers.ModelSerializer):
    categories = EventPlanningCategoriesSerializer(many=True)

    class Meta:
        model = EventPlanningSubCategory
        fields = '__all__'




# from rest_framework import serializers
# from .models import EventPlanningCategories, EventPlanningSubCategory

# class EventPlanningCategoriesSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = EventPlanningCategories
#         fields = '__all__'


# class EventPlanningSubCategorySerializer(serializers.ModelSerializer):
#     categories = EventPlanningCategoriesSerializer(many=True)

#     class Meta:
#         model = EventPlanningSubCategory
#         fields = '__all__'




# from rest_framework import serializers
# from .models import EventPlanningSubCategory, EventPlanningCategories

# class EventPlanningCategoriesSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = EventPlanningCategories
#         fields = '__all__'

# class EventPlanningSubCategorySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = EventPlanningSubCategory
#         fields = '__all__'


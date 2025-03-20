from rest_framework import serializers
from .models import RentHireCategory, RentHireSubCategory

class RentHireCategorySerializer(serializers.ModelSerializer):
  
    image = serializers.SerializerMethodField()

    class Meta:
        model = RentHireCategory
        fields = '__all__'

    def get_image(self, obj):
        request = self.context.get('request')
        if request is not None and obj.image:
            # Build and return the absolute URL for the image
            return request.build_absolute_uri(obj.image.url)
        return obj.image.url if obj.image else None   

class RentHireSubCategorySerializer(serializers.ModelSerializer):
    categories = RentHireCategorySerializer(many=True)
   
    class Meta:
        model = RentHireSubCategory
        fields = '__all__'

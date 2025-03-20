from rest_framework import serializers
from .models import EnergyCategory, EnergySubCategory

class EnergyCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = EnergyCategory
        fields = ['id', 'title', 'slug', 'image', 'category']

class EnergySubCategorySerializer(serializers.ModelSerializer):
    categories = EnergyCategorySerializer(many=True, read_only=True)

    class Meta:
        model = EnergySubCategory
        fields = ['id', 'title', 'slug', 'categories']
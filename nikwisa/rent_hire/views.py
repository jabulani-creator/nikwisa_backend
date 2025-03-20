from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import RentHireCategory, RentHireSubCategory
from .serializers import RentHireCategorySerializer, RentHireSubCategorySerializer

class RentHireCategoryViewSet(viewsets.ModelViewSet):
    queryset = RentHireCategory.objects.all()
    serializer_class = RentHireCategorySerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['title']
    search_fields = ['title']
    ordering_fields = ['title']

    def get_queryset(self):
        queryset = super().get_queryset()
        subcategory_id = self.request.query_params.get('subcategory_id', None)
        if subcategory_id:
            queryset = queryset.filter(subcategories__id=subcategory_id)
        return queryset

    def create(self, request):
        serializer = RentHireCategorySerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        try:
            category = RentHireCategory.objects.get(pk=pk)
        except RentHireCategory.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = RentHireCategorySerializer(category, context={'request': request})
        return Response(serializer.data)

    def update(self, request, pk=None):
        try:
            category = RentHireCategory.objects.get(pk=pk)
        except RentHireCategory.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = RentHireCategorySerializer(category, data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def partial_update(self, request, pk=None):
        try:
            category = RentHireCategory.objects.get(pk=pk)
        except RentHireCategory.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = RentHireCategorySerializer(category, data=request.data, partial=True, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        try:
            category = RentHireCategory.objects.get(pk=pk)
        except RentHireCategory.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class RentHireSubCategoryViewSet(viewsets.ModelViewSet):
    queryset = RentHireSubCategory.objects.all()
    serializer_class = RentHireSubCategorySerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['categories__id', 'categories__title']
    search_fields = ['title']
    ordering_fields = ['title']

    def create(self, request):
        serializer = RentHireSubCategorySerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        try:
            subcategory = RentHireSubCategory.objects.get(pk=pk)
        except RentHireSubCategory.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = RentHireSubCategorySerializer(subcategory, context={'request': request})
        return Response(serializer.data)

    def update(self, request, pk=None):
        try:
            subcategory = RentHireSubCategory.objects.get(pk=pk)
        except RentHireSubCategory.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = RentHireSubCategorySerializer(subcategory, data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def partial_update(self, request, pk=None):
        try:
            subcategory = RentHireSubCategory.objects.get(pk=pk)
        except RentHireSubCategory.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = RentHireSubCategorySerializer(subcategory, data=request.data, partial=True, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        try:
            subcategory = RentHireSubCategory.objects.get(pk=pk)
        except RentHireSubCategory.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        subcategory.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

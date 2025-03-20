from django.contrib import admin
from .models import RentHireCategory, RentHireSubCategory

class RentHireCategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug')
    search_fields = ('title',)
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ('categories',)


class RentHireSubCategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug')
    search_fields = ('title', 'categories__title')
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ('categories',)

admin.site.register(RentHireCategory, RentHireCategoryAdmin)
admin.site.register(RentHireSubCategory, RentHireSubCategoryAdmin)
from django.contrib import admin
from .models import EnergyCategory, EnergySubCategory

@admin.register(EnergyCategory)
class EnergyCategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug')  # Removed 'categories' from list_display
    prepopulated_fields = {'slug': ('title',)}

@admin.register(EnergySubCategory)
class EnergySubCategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug')
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ('categories',)

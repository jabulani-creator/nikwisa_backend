from django.contrib import admin
from .models import Category, SubCategory

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug')
    search_fields = ('title',)
    prepopulated_fields = {'slug': ('title',)}

# class SubCategoryAdmin(admin.ModelAdmin):
#     list_display = ('title', 'category', 'slug')
#     search_fields = ('title', 'category__title')
#     prepopulated_fields = {'slug': ('title',)}
#     list_filter = ('category',)

admin.site.register(Category, CategoryAdmin)
# admin.site.register(SubCategory, SubCategoryAdmin)
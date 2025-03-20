from django.contrib import admin
from .models import EventPlanningCategories, EventPlanningSubCategory

class EventPlanningCategoriesAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug')
    search_fields = ('title',)
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ('categories',)

class EventPlanningSubCategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug')
    search_fields = ('title', 'categories__title')
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ('categories',)


admin.site.register(EventPlanningCategories, EventPlanningCategoriesAdmin)
admin.site.register(EventPlanningSubCategory, EventPlanningSubCategoryAdmin)


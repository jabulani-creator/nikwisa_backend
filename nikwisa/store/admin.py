from django.contrib import admin
from .models import Store, StoreReview, Reaction, Offering, StoreImage, Province, Area

# Province admin
class ProvinceAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}

# Area admin with inline areas
class AreaAdmin(admin.ModelAdmin):
    list_display = ('name', 'province', 'slug')
    list_filter = ('province',)
    search_fields = ('name', 'province__name')
    prepopulated_fields = {'slug': ('name',)}

class StoreAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'slug', 'rating', 'reviews_count', 'is_verified', 'is_responsive', 'province')
    search_fields = ('name', 'owner__username')
    prepopulated_fields = {'slug': ('name',)}
    filter_horizontal = ('categories', 'event_planning_categories', 'rent_hire_categories', 'service_areas')
    list_filter = ('is_verified', 'is_responsive', 'province')
    exclude = ('rating', 'reviews_count')

class OfferingAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'store', 'phone_number', 'whatsapp_number']
    search_fields = ['name', 'description', 'phone_number', 'whatsapp_number']
    list_filter = ('name',)

class StoreImageAdmin(admin.ModelAdmin):
    list_display = ['store', 'image', 'uploaded_at']
    search_fields = ['store__name', 'store__owner__username']
    list_filter = ['uploaded_at']

# Register models with their respective admin classes
admin.site.register(Province, ProvinceAdmin)
admin.site.register(Area, AreaAdmin)
admin.site.register(Store, StoreAdmin)
admin.site.register(StoreReview)
admin.site.register(Reaction)
admin.site.register(Offering, OfferingAdmin)
admin.site.register(StoreImage, StoreImageAdmin)



# from django.contrib import admin
# from .models import Store, StoreReview, Reaction, Offering, StoreImage


# class StoreAdmin(admin.ModelAdmin):
#     list_display = ('name', 'owner', 'slug', 'rating', 'reviews_count', 'is_verified', 'is_responsive')
#     search_fields = ('name', 'owner__username')
#     prepopulated_fields = {'slug': ('name',)}
#     filter_horizontal = ('categories', 'event_planning_categories', 'rent_hire_categories')  # Added rent_hire_categories
#     list_filter = ('is_verified', 'is_responsive')
#     exclude = ('rating', 'reviews_count', 'is_verified', 'is_responsive')  # Exclude from the form

# class OfferingAdmin(admin.ModelAdmin):
#     list_display = ['name', 'price', 'store', 'phone_number', 'whatsapp_number']
#     search_fields = ['name', 'description', 'phone_number', 'whatsapp_number']
#     list_filter = ('name',)

# class StoreImageAdmin(admin.ModelAdmin):
#     list_display = ['store', 'image', 'uploaded_at']
#     search_fields = ['store__name', 'store__owner__username']  # To search images by associated store
#     list_filter = ['uploaded_at']



# # Register models with their respective admin classes
# admin.site.register(Store, StoreAdmin)
# admin.site.register(StoreReview)
# admin.site.register(Reaction)
# admin.site.register(Offering, OfferingAdmin)
# admin.site.register(StoreImage, StoreImageAdmin)  # Register StoreImage model



from django.contrib import admin
from .models import CentralizedProduct

class CentralizedProductAdmin(admin.ModelAdmin):
    list_display = ('content_type', 'object_id', 'content_object', 'created_at', 'updated_at')
    search_fields = ('content_type__model', 'object_id')
    list_filter = ('content_type', 'created_at', 'updated_at')

admin.site.register(CentralizedProduct, CentralizedProductAdmin)
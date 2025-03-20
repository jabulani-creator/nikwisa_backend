from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import CustomUser, StoredJWT, Message, Like, Review

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    # Fields to display in the admin interface
    list_display = ('email', 'username', 'role', 'is_staff', 'is_active', 'is_superuser')
    list_filter = ('role', 'is_staff', 'is_active')
    search_fields = ('email', 'username')
    ordering = ('email',)

    # Add extra fields for the user creation form
    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        ('Personal info', {'fields': ('role', 'user_type', 'profile_image', 'phone_number')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Important dates', {'fields': ('last_login',)}),
    )

    # Add fields for the user edit form
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2', 'role', 'is_active', 'is_staff', 'is_superuser'),
        }),
    )
    actions = ['make_superuser']

    def make_superuser(self, request, queryset):
        queryset.update(is_staff=True, is_superuser=True)

    make_superuser.short_description = _("Make selected users superusers")

# Register CustomUserAdmin
admin.site.register(CustomUser, CustomUserAdmin)

# Register other models
admin.site.register(StoredJWT)
admin.site.register(Message)
admin.site.register(Like)
admin.site.register(Review)

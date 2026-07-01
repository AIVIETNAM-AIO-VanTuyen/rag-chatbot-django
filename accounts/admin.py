from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['email', 'first_name', 'last_name', 'phone_number', 'is_staff', 'is_active']
    search_fields = ['email', 'first_name', 'last_name', 'phone_number']
    ordering = ['email']
    
    # Loại bỏ username khỏi fieldsets
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Thông tin cá nhân', {'fields': ('first_name', 'last_name', 'phone_number')}),
        ('Quyền hạn', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Ngày quan trọng', {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'phone_number', 'password'),
        }),
    )

admin.site.register(CustomUser, CustomUserAdmin)

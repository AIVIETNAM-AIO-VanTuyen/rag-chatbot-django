from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account, ChatbotRole

class AccountAdmin(UserAdmin):
    model = Account
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('phone_number',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('phone_number',)}),
    )
    list_display = ['username', 'email', 'phone_number', 'is_staff', 'is_active']

admin.site.register(Account, AccountAdmin)

@admin.register(ChatbotRole)
class ChatbotRoleAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'is_active', 'created_at']
    search_fields = ['name', 'code']
    list_filter = ['is_active']
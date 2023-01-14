from django.contrib import admin
from users.models import AuthHash, User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from users.forms import UserForm


class UserAdmin(BaseUserAdmin):
    add_form = UserForm
    fieldsets = (
        (None, {'fields': (
            'telegram_id', 'password', 'first_name', 'last_name', 'telegram_username',
            'photo', 'created_at', 'updated_at', 'is_active')}
        ),
        ('Permissions', {'fields': (
            'is_staff',
            'is_superuser',
            'groups',
            'user_permissions',
        )}),
    )
    add_fieldsets = (
        ('Telegram', {
            'classes': ('wide',),
            'fields': ('telegram_id', 'telegram_username', 'first_name', 'last_name', 'photo')
        }),
        ('Account', {
            'classes': ('wide',),
            'fields': ('is_active', 'is_staff')
        })
    )

    readonly_fields = ('created_at', 'updated_at')
    list_display = ('telegram_id', 'telegram_username', 'is_active', 'is_staff', 'updated_at')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('telegram_id', 'telegram_username')
    ordering = ('telegram_id', 'telegram_username')
    filter_horizontal = ('groups', 'user_permissions')


class AuthHashAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('hash', 'created_at', 'is_expired')}),
    )

    readonly_fields = ('created_at', 'is_expired')
    list_display = ('hash', 'created_at', 'is_expired')
    ordering = ('created_at',)


admin.site.register(AuthHash, AuthHashAdmin)
admin.site.register(User, UserAdmin)
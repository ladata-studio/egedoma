from django.contrib import admin
from users.models import AuthHash, Student


class AuthHashAdmin(admin.ModelAdmin):
    readonly_fields = ('created', 'is_expired')


class StudentAdmin(admin.ModelAdmin):
    readonly_fields = ('created', 'is_active')


admin.site.register(AuthHash, AuthHashAdmin)
admin.site.register(Student, StudentAdmin)
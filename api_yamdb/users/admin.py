from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


class MyUserAdmin(UserAdmin):
    model = User
    fieldsets = UserAdmin.fieldsets + (
            (None, {'fields': ('role', 'bio', 'confirm_code')}),
    )


admin.site.register(User, MyUserAdmin)

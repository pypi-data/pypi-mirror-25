from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin

UserAdmin.fieldsets += (
    ('Additional Data', {'fields': ('type',)}),
)
admin.site.register(User, UserAdmin)

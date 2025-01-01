from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from .models import Game, CustomUser

class CustomUserAdmin(UserAdmin):
    # Add your custom fields to the fieldsets
    fieldsets = UserAdmin.fieldsets + (
        (_('Additional Info'), {'fields': ('birthday', 'facebook', 'twitch', 'gender')}),
    )

    # Add your custom fields to the add_fieldsets
    add_fieldsets = UserAdmin.add_fieldsets + (
        (_('Additional Info'), {'fields': ('birthday', 'facebook', 'twitch', 'gender')}),
    )

# Register your models
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Game)

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from .models import Game, CustomUser, ProposedGame

class CustomUserAdmin(UserAdmin):
    # Add your custom fields to the fieldsets
    fieldsets = UserAdmin.fieldsets + (
        (_('Additional Info'), {'fields': ('birthday', 'facebook', 'twitch', 'gender')}),
    )

    # Add your custom fields to the add_fieldsets
    add_fieldsets = UserAdmin.add_fieldsets + (
        (_('Additional Info'), {'fields': ('birthday', 'facebook', 'twitch', 'gender')}),
    )

class ProposedGameAdmin(admin.ModelAdmin):
    list_display = ('name', 'votes', 'is_approved', 'created_by', 'created_at')
    list_filter = ('is_approved',)
    search_fields = ('name', 'description')

# Register your models
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Game)
admin.site.register(ProposedGame, ProposedGameAdmin)

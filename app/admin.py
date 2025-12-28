from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from .models import (
    Game, CustomUser, ProposedGame, Character, Message,
    CharacterFriend, CharacterFriendRequest, CharacterProfile,
    Poke, PokeBlock, CharacterIdentityReveal, CharacterBlock
)

class CustomUserAdmin(UserAdmin):
    # Add your custom fields to the fieldsets
    fieldsets = UserAdmin.fieldsets + (
        (_('Additional Info'), {'fields': ('birthday', 'facebook', 'twitch', 'gender')}),
        (_('Profile Settings'), {
            'fields': (
                'profile_visibility', 'profile_bio', 'profile_picture',
                'steam_profile', 'youtube_channel', 'stackoverflow_profile',
                'github_profile', 'linkedin_profile', 'custom_links'
            )
        }),
    )

    # Add your custom fields to the add_fieldsets
    add_fieldsets = UserAdmin.add_fieldsets + (
        (_('Additional Info'), {'fields': ('birthday', 'facebook', 'twitch', 'gender')}),
    )

class ProposedGameAdmin(admin.ModelAdmin):
    list_display = ('name', 'votes', 'is_approved', 'created_by', 'created_at')
    list_filter = ('is_approved',)
    search_fields = ('name', 'description')

class CharacterFriendAdmin(admin.ModelAdmin):
    list_display = ('character1', 'character2', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('character1__nickname', 'character2__nickname')

class CharacterFriendRequestAdmin(admin.ModelAdmin):
    list_display = ('sender_character', 'receiver_character', 'status', 'sent_date')
    list_filter = ('status', 'sent_date')
    search_fields = ('sender_character__nickname', 'receiver_character__nickname')

class CharacterProfileAdmin(admin.ModelAdmin):
    list_display = ('character', 'is_public', 'updated_at')
    list_filter = ('is_public', 'updated_at')
    search_fields = ('character__nickname',)

class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender_character', 'receiver_character', 'privacy_mode', 'is_read', 'sent_date')
    list_filter = ('privacy_mode', 'is_read', 'sent_date')
    search_fields = ('sender_character__nickname', 'receiver_character__nickname', 'content')

class PokeAdmin(admin.ModelAdmin):
    list_display = ('sender_character', 'receiver_character', 'status', 'sent_date', 'is_read', 'reported_as_spam')
    list_filter = ('status', 'sent_date', 'is_read', 'reported_as_spam')
    search_fields = ('sender_character__nickname', 'receiver_character__nickname', 'content')
    readonly_fields = ('sent_date', 'responded_at', 'read_at', 'reported_at')

class PokeBlockAdmin(admin.ModelAdmin):
    list_display = ('blocker_character', 'blocked_character', 'blocked_at', 'reason')
    list_filter = ('blocked_at',)
    search_fields = ('blocker_character__nickname', 'blocked_character__nickname', 'reason')
    readonly_fields = ('blocked_at',)

# Register your models
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Game)
admin.site.register(ProposedGame, ProposedGameAdmin)
admin.site.register(Character)
admin.site.register(Message, MessageAdmin)
admin.site.register(CharacterFriend, CharacterFriendAdmin)
admin.site.register(CharacterFriendRequest, CharacterFriendRequestAdmin)
admin.site.register(CharacterProfile, CharacterProfileAdmin)
admin.site.register(Poke, PokeAdmin)
admin.site.register(PokeBlock, PokeBlockAdmin)

class CharacterIdentityRevealAdmin(admin.ModelAdmin):
    list_display = ('revealing_character', 'revealed_to_character', 'is_active', 'revealed_at', 'revoked_at')
    list_filter = ('is_active', 'revealed_at', 'revoked_at')
    search_fields = ('revealing_character__nickname', 'revealed_to_character__nickname')
    readonly_fields = ('revealed_at', 'revoked_at')

class CharacterBlockAdmin(admin.ModelAdmin):
    list_display = ('blocker_character', 'blocked_character', 'reported_as_spam', 'blocked_at')
    list_filter = ('reported_as_spam', 'blocked_at')
    search_fields = ('blocker_character__nickname', 'blocked_character__nickname', 'reason')
    readonly_fields = ('blocked_at', 'reported_at')

admin.site.register(CharacterIdentityReveal, CharacterIdentityRevealAdmin)
admin.site.register(CharacterBlock, CharacterBlockAdmin)

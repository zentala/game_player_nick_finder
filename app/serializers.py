from rest_framework import serializers
from .models import (
    Game, Character, Message, CustomUser, CharacterFriend, 
    CharacterFriendRequest, CharacterProfile
)

class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = '__all__'

class CharacterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Character
        fields = '__all__'


class MessageSerializer(serializers.ModelSerializer):
    privacy_mode = serializers.CharField(required=False)
    identity_revealed = serializers.BooleanField(required=False)
    
    class Meta:
        model = Message
        fields = [
            'id', 'sender_character', 'receiver_character', 
            'content', 'sent_date', 'thread_id', 'privacy_mode',
            'identity_revealed', 'is_read', 'read_at'
        ]


class CharacterFriendSerializer(serializers.ModelSerializer):
    class Meta:
        model = CharacterFriend
        fields = ['id', 'character1', 'character2', 'created_at']


class CharacterFriendRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = CharacterFriendRequest
        fields = [
            'id', 'sender_character', 'receiver_character', 
            'sent_date', 'status', 'message'
        ]


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            'id', 'username', 'first_name', 'last_name', 'email',
            'birthday', 'facebook', 'twitch', 'gender',
            'profile_visibility', 'steam_profile', 'youtube_channel',
            'stackoverflow_profile', 'github_profile', 'linkedin_profile',
            'custom_links', 'profile_bio', 'profile_picture'
        ]
        read_only_fields = ['id', 'username']


class CharacterProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CharacterProfile
        fields = [
            'id', 'character', 'custom_bio', 'custom_images',
            'screenshots', 'memories', 'is_public', 'updated_at'
        ]
        read_only_fields = ['updated_at']

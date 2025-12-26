from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from django.db.models import Q
from .models import (
    Game, Character, Message, CustomUser, CharacterFriend,
    CharacterFriendRequest, CharacterProfile
)
from .serializers import (
    GameSerializer, CharacterSerializer, MessageSerializer,
    CharacterFriendSerializer, CharacterFriendRequestSerializer,
    UserProfileSerializer, CharacterProfileSerializer
)

class GameViewSet(viewsets.ModelViewSet):
    queryset = Game.objects.all()
    serializer_class = GameSerializer

class CharacterViewSet(viewsets.ModelViewSet):
    queryset = Character.objects.all()
    serializer_class = CharacterSerializer


class CharacterFriendRequestViewSet(viewsets.ModelViewSet):
    queryset = CharacterFriendRequest.objects.all()
    serializer_class = CharacterFriendRequestSerializer
    permission_classes = [IsAuthenticated]
    
    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        
        # Validate data
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        sender_character_id = request.data.get('sender_character')
        receiver_character_id = request.data.get('receiver_character')
        
        if not sender_character_id or not receiver_character_id:
            return Response(
                {'error': 'Both sender_character and receiver_character are required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            sender_character = Character.objects.get(id=sender_character_id)
            receiver_character = Character.objects.get(id=receiver_character_id)
            
            # Verify sender character belongs to user
            if sender_character.user != request.user:
                return Response(
                    {'error': 'You can only send requests from your own characters'},
                    status=status.HTTP_403_FORBIDDEN
                )
            
            # Don't allow sending request to own character
            if sender_character.user == receiver_character.user:
                return Response(
                    {'error': 'Cannot send friend request to your own character'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Check if request already exists
            existing_request = CharacterFriendRequest.objects.filter(
                sender_character=sender_character,
                receiver_character=receiver_character
            ).first()
            
            if existing_request:
                return Response(
                    {'error': 'Friend request already exists'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Save with validated characters
            serializer.save(
                sender_character=sender_character,
                receiver_character=receiver_character
            )
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
            
        except Character.DoesNotExist:
            return Response(
                {'error': 'Character not found'},
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=True, methods=['post'])
    def accept(self, request, pk=None):
        friend_request = self.get_object()
        
        if friend_request.receiver_character.user != request.user:
            return Response(
                {'error': 'You can only accept requests sent to your characters'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Create friendship
        CharacterFriend.objects.create(
            character1=friend_request.sender_character,
            character2=friend_request.receiver_character
        )
        
        friend_request.status = 'ACCEPTED'
        friend_request.save()
        
        return Response({'status': 'accepted'})
    
    @action(detail=True, methods=['post'])
    def decline(self, request, pk=None):
        friend_request = self.get_object()
        
        if friend_request.receiver_character.user != request.user:
            return Response(
                {'error': 'You can only decline requests sent to your characters'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        friend_request.status = 'DECLINED'
        friend_request.save()
        
        return Response({'status': 'declined'})


class CharacterProfileViewSet(viewsets.ModelViewSet):
    queryset = CharacterProfile.objects.all()
    serializer_class = CharacterProfileSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        # Filter by visibility
        if self.request.user.is_authenticated:
            return CharacterProfile.objects.filter(
                Q(is_public=True) |
                Q(character__user=self.request.user) |
                Q(character__friends_as_character1__character2__user=self.request.user) |
                Q(character__friends_as_character2__character1__user=self.request.user)
            ).distinct()
        return CharacterProfile.objects.filter(is_public=True)


class UserProfileViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        
        # Users can always see their own profile
        queryset = CustomUser.objects.filter(id=user.id)
        
        # For other users, apply visibility filters
        if self.action == 'list':
            # Only show public profiles or friends
            queryset = CustomUser.objects.filter(
                Q(profile_visibility='PUBLIC') |
                Q(id=user.id) |
                Q(profile_visibility='FRIENDS_ONLY', id__in=self._get_friends_user_ids(user))
            )
        
        return queryset
    
    def _get_friends_user_ids(self, user):
        """Get user IDs of users who are friends through characters"""
        user_characters = Character.objects.filter(user=user)
        friend_characters = Character.objects.filter(
            Q(friends_as_character1__character2__in=user_characters) |
            Q(friends_as_character2__character1__in=user_characters)
        )
        return friend_characters.values_list('user_id', flat=True).distinct()


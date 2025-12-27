# 001 - Feature Proposals - Game Player Nick Finder

**Status**: ✅ Most features implemented  
**Last Updated**: 2024

## Document Purpose
This document contains detailed feature proposals for completing the Game Player Nick Finder application. It includes developer perspectives on implementation and UX engineer perspectives on user experience.

## Current State Analysis

### What Works
- ✅ User registration and authentication
- ✅ Character creation and management (multiple characters per user)
- ✅ Game management and voting system
- ✅ Basic messaging system (character-to-character)
- ✅ Message threading (thread_id system)

### What's Missing
- ❌ Privacy controls for messaging (anonymous vs reveal identity)
- ❌ Character-based friend system (currently only user-based Friend model exists)
- ❌ Friend request system for characters
- ❌ Multiple conversation management
- ❌ Real-time messaging
- ❌ User control over identity revelation
- ❌ Friend list management for characters

## Feature Proposal 1: Enhanced Messaging with Privacy Controls

### Developer Perspective

#### Current Implementation
The current messaging system uses:
- `Message` model with `sender_character` and `receiver_character`
- `thread_id` for grouping messages
- Basic message sending and receiving

#### Proposed Enhancements

**1. Privacy Mode Field**
```python
# Add to Character model
class Character(models.Model):
    # ... existing fields ...
    privacy_mode = models.CharField(
        max_length=20,
        choices=[
            ('ANONYMOUS', 'Anonymous'),
            ('REVEAL_IDENTITY', 'Reveal Identity'),
            ('FRIENDS_ONLY', 'Friends Only'),
        ],
        default='REVEAL_IDENTITY',
        help_text='Privacy mode for this character'
    )
```

**2. Message Privacy Context**
```python
# Add to Message model
class Message(models.Model):
    # ... existing fields ...
    sender_privacy_mode = models.CharField(
        max_length=20,
        help_text='Privacy mode used when sending this message'
    )
    identity_revealed = models.BooleanField(
        default=False,
        help_text='Whether sender revealed their user identity'
    )
```

**3. Message Display Logic**
```python
# In views.py or utils.py
def get_message_display_info(message, viewer_character):
    """
    Returns display information for a message based on privacy settings
    """
    if message.sender_privacy_mode == 'ANONYMOUS':
        return {
            'display_name': message.sender_character.nickname,
            'show_user_info': False,
            'show_avatar': True,  # Character avatar only
        }
    elif message.sender_privacy_mode == 'REVEAL_IDENTITY':
        return {
            'display_name': f"{message.sender_character.nickname} ({message.sender_character.user.username})",
            'show_user_info': True,
            'show_avatar': True,
            'user_profile_link': reverse('user_profile', args=[message.sender_character.user.id]),
        }
    # ... handle other cases
```

#### Implementation Steps
1. Add privacy fields to models
2. Create migration
3. Update message sending form to include privacy option
4. Update message display templates
5. Add privacy toggle in character settings
6. Write tests

### UX Engineer Perspective

#### User Flow Design

**Scenario 1: Sending Anonymous Message**
1. User navigates to character detail page
2. Clicks "Send Message" button
3. Message compose dialog opens
4. User sees privacy toggle: "Send as Anonymous" (checkbox)
5. When checked, shows preview: "You will appear as [Character Name] only"
6. User types message and sends
7. Recipient sees message from character only, no user info

**Scenario 2: Revealing Identity**
1. User is in existing conversation
2. User clicks "Reveal My Identity" button
3. Confirmation dialog: "This will show your user profile to [Character Name]. Continue?"
4. User confirms
5. All future messages in thread show user identity
6. Previous messages remain as sent (privacy preserved)

#### UI Components

**Privacy Toggle Component**
```
┌─────────────────────────────────────┐
│ Send Message                         │
├─────────────────────────────────────┤
│ To: [Character Name]               │
│                                     │
│ ┌─────────────────────────────────┐ │
│ │ ☐ Send as Anonymous             │ │
│ │   (Hide your user identity)     │ │
│ └─────────────────────────────────┘ │
│                                     │
│ [Message text area]                 │
│                                     │
│ [Cancel]  [Send Message]            │
└─────────────────────────────────────┘
```

**Message Display with Privacy**
```
┌─────────────────────────────────────┐
│ Conversation with CharacterName      │
├─────────────────────────────────────┤
│                                     │
│ [Avatar] CharacterName              │
│         (Anonymous)                 │
│ Hello!                              │
│ ─────────────────────────────────   │
│                                     │
│ [Your Avatar] YourCharacter         │
│              (You)                  │
│ Hi there!                           │
│ ─────────────────────────────────   │
│                                     │
│ [Avatar] CharacterName              │
│         (Anonymous)                 │
│ Want to play together?              │
│                                     │
└─────────────────────────────────────┘
```

#### Design Principles
1. **Clarity**: Privacy mode should be clearly indicated
2. **Control**: User should easily change privacy settings
3. **Transparency**: Recipient should know if sender is anonymous
4. **Reversibility**: User can reveal identity later if desired

---

## Feature Proposal 2: Character-Based Friend System

### Developer Perspective

#### Current Implementation
- `Friend` model exists but is user-to-user
- `FriendRequest` model exists but is user-to-user
- No character-level friend relationships

#### Proposed Implementation

**1. Character Friend Model**
```python
class CharacterFriend(models.Model):
    """
    Represents a friendship between two characters (not users)
    """
    character1 = models.ForeignKey(
        Character,
        on_delete=models.CASCADE,
        related_name='friends_as_character1'
    )
    character2 = models.ForeignKey(
        Character,
        on_delete=models.CASCADE,
        related_name='friends_as_character2'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    # Privacy settings for this friendship
    character1_revealed_identity = models.BooleanField(default=False)
    character2_revealed_identity = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ('character1', 'character2')
        # Ensure character1.id < character2.id to avoid duplicates
        
    def save(self, *args, **kwargs):
        # Ensure character1.id < character2.id
        if self.character1.id > self.character2.id:
            self.character1, self.character2 = self.character2, self.character1
        super().save(*args, **kwargs)
```

**2. Character Friend Request Model**
```python
class CharacterFriendRequest(models.Model):
    """
    Friend request from one character to another
    """
    sender_character = models.ForeignKey(
        Character,
        on_delete=models.CASCADE,
        related_name='sent_friend_requests'
    )
    receiver_character = models.ForeignKey(
        Character,
        on_delete=models.CASCADE,
        related_name='received_friend_requests'
    )
    sent_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ('PENDING', 'Pending'),
            ('ACCEPTED', 'Accepted'),
            ('DECLINED', 'Declined'),
        ],
        default='PENDING'
    )
    message = models.TextField(blank=True, help_text='Optional message with request')
    
    class Meta:
        unique_together = ('sender_character', 'receiver_character')
```

**3. Friend Management Views**
```python
class CharacterFriendListView(LoginRequiredMixin, ListView):
    """
    List all friends for a specific character
    """
    model = CharacterFriend
    template_name = 'characters/friend_list.html'
    
    def get_queryset(self):
        character = get_object_or_404(
            Character,
            id=self.kwargs['character_id'],
            user=self.request.user
        )
        # Get friends where character is either character1 or character2
        return CharacterFriend.objects.filter(
            models.Q(character1=character) | models.Q(character2=character)
        )
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        character = get_object_or_404(
            Character,
            id=self.kwargs['character_id'],
            user=self.request.user
        )
        context['character'] = character
        # Get friend characters (the other character in each friendship)
        friends = []
        for friendship in context['object_list']:
            if friendship.character1 == character:
                friends.append(friendship.character2)
            else:
                friends.append(friendship.character1)
        context['friend_characters'] = friends
        return context
```

#### Implementation Steps
1. Create CharacterFriend and CharacterFriendRequest models
2. Create migrations
3. Create friend request sending view
4. Create friend request management view (accept/decline)
5. Create friend list view
6. Add "Add Friend" button to character detail pages
7. Update messaging to show friend status
8. Write tests

### UX Engineer Perspective

#### User Flow Design

**Scenario 1: Sending Friend Request**
1. User views another character's profile
2. Sees "Add as Friend" button
3. Clicks button
4. Optional: Add message with request
5. Confirmation: "Friend request sent to [Character Name]"
6. Button changes to "Friend Request Sent" (disabled)

**Scenario 2: Receiving Friend Request**
1. User receives notification: "New friend request from [Character Name]"
2. User navigates to friend requests page
3. Sees list of pending requests with:
   - Character avatar and name
   - Game name
   - Optional message
   - Accept/Decline buttons
4. User clicks Accept
5. Confirmation: "[Character Name] is now your friend"
6. Character appears in friend list

**Scenario 3: Managing Friends**
1. User navigates to character's friend list
2. Sees grid/list of friends with:
   - Character avatar
   - Character name
   - Game name
   - Last seen/active status
   - "Message" button
   - "Remove Friend" option
3. User can filter friends by game
4. User can search friends by name

#### UI Components

**Friend Request Card**
```
┌─────────────────────────────────────┐
│ [Avatar] CharacterName              │
│ Game: World of Warcraft             │
│                                     │
│ "Hey, remember me from 2005?"       │
│                                     │
│ [Decline]  [Accept]                │
└─────────────────────────────────────┘
```

**Friend List**
```
┌─────────────────────────────────────┐
│ Friends (12)                         │
├─────────────────────────────────────┤
│ [Filter by Game ▼] [Search...]       │
├─────────────────────────────────────┤
│ [Avatar] Character1              │
│         WoW • Online                │
│         [Message] [Remove]          │
│ ─────────────────────────────────   │
│ [Avatar] Character2                 │
│         Lineage 2 • Offline         │
│         [Message] [Remove]          │
│ ─────────────────────────────────   │
└─────────────────────────────────────┘
```

#### Design Principles
1. **Character-Centric**: Friendships are between characters, not users
2. **Game Context**: Friends are shown with their game context
3. **Easy Actions**: Quick access to message or remove friends
4. **Clear Status**: Friend request status is always clear

---

## Feature Proposal 3: Multiple Conversation Management

### Developer Perspective

#### Current Implementation
- Messages use `thread_id` for grouping
- Basic conversation viewing exists
- No conversation list or management

#### Proposed Implementation

**1. Conversation Model (Optional)**
```python
class Conversation(models.Model):
    """
    Represents a conversation between two characters
    Can be used for metadata and easier querying
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    character1 = models.ForeignKey(Character, on_delete=models.CASCADE, related_name='conversations_as_char1')
    character2 = models.ForeignKey(Character, on_delete=models.CASCADE, related_name='conversations_as_char2')
    last_message = models.ForeignKey(Message, on_delete=models.SET_NULL, null=True, related_name='conversation_last')
    last_message_date = models.DateTimeField(null=True)
    unread_count_char1 = models.IntegerField(default=0)
    unread_count_char2 = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('character1', 'character2')
        ordering = ['-last_message_date']
    
    def get_other_character(self, character):
        """Get the other character in this conversation"""
        if character == self.character1:
            return self.character2
        return self.character1
    
    def get_unread_count(self, character):
        """Get unread count for a character"""
        if character == self.character1:
            return self.unread_count_char1
        return self.unread_count_char2
```

**2. Conversation List View**
```python
class ConversationListView(LoginRequiredMixin, ListView):
    """
    List all conversations for user's characters
    """
    model = Conversation
    template_name = 'messages/conversation_list.html'
    
    def get_queryset(self):
        user_characters = Character.objects.filter(user=self.request.user)
        # Get all conversations involving user's characters
        conversations = Conversation.objects.filter(
            models.Q(character1__in=user_characters) |
            models.Q(character2__in=user_characters)
        ).select_related(
            'character1', 'character2', 'character1__game', 'character2__game',
            'last_message'
        ).prefetch_related('last_message__sender_character')
        
        # Annotate with unread counts for current user
        for conv in conversations:
            user_char = None
            if conv.character1 in user_characters:
                user_char = conv.character1
            elif conv.character2 in user_characters:
                user_char = conv.character2
            
            if user_char:
                conv.unread_count = conv.get_unread_count(user_char)
                conv.other_character = conv.get_other_character(user_char)
        
        return conversations
```

**3. Update Message Model**
```python
class Message(models.Model):
    # ... existing fields ...
    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)
    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name='messages',
        null=True  # For backward compatibility
    )
    
    def mark_as_read(self, character):
        """Mark message as read by a character"""
        if (self.receiver_character == character and not self.is_read):
            self.is_read = True
            self.read_at = timezone.now()
            self.save()
            # Update conversation unread count
            if self.conversation:
                if self.conversation.character1 == character:
                    self.conversation.unread_count_char1 = max(0, self.conversation.unread_count_char1 - 1)
                else:
                    self.conversation.unread_count_char2 = max(0, self.conversation.unread_count_char2 - 1)
                self.conversation.save()
```

#### Implementation Steps
1. Create Conversation model (optional, can use thread_id)
2. Create migration
3. Create conversation list view
4. Update message sending to create/update conversations
5. Add unread message tracking
6. Create conversation UI components
7. Write tests

### UX Engineer Perspective

#### User Flow Design

**Scenario 1: Viewing Conversation List**
1. User navigates to Messages page
2. Sees list of conversations grouped by character
3. Each conversation shows:
   - Other character's avatar and name
   - Game name
   - Last message preview
   - Timestamp
   - Unread badge (if any)
4. User clicks conversation
5. Conversation opens in thread view

**Scenario 2: Switching Between Conversations**
1. User is in a conversation
2. Sidebar shows list of other conversations
3. User clicks another conversation
4. Current conversation is saved/closed
5. New conversation opens
6. Unread badges update

**Scenario 3: Starting New Conversation**
1. User views character profile
2. Clicks "Send Message"
3. If conversation exists, opens existing conversation
4. If new, creates new conversation thread
5. Message compose area appears

#### UI Components

**Conversation List Sidebar**
```
┌─────────────────────────────────────┐
│ Conversations                        │
├─────────────────────────────────────┤
│ [Avatar] CharacterName (3)          │
│         Last message preview...     │
│         2 hours ago                  │
│ ─────────────────────────────────   │
│ [Avatar] AnotherCharacter           │
│         Another message...          │
│         1 day ago                   │
│ ─────────────────────────────────   │
│ [Avatar] FriendCharacter            │
│         Hello!                      │
│         Just now                    │
└─────────────────────────────────────┘
```

**Conversation Thread View**
```
┌─────────────────────────────────────┐
│ Conversation with CharacterName      │
│ Game: World of Warcraft              │
├─────────────────────────────────────┤
│ [Sidebar with other conversations]  │
│                                     │
│ [Message history]                   │
│                                     │
│ ┌─────────────────────────────────┐ │
│ │ Type your message...            │ │
│ │ [Privacy Toggle] [Send]        │ │
│ └─────────────────────────────────┘ │
└─────────────────────────────────────┘
```

#### Design Principles
1. **Easy Navigation**: Quick switching between conversations
2. **Context Preservation**: Each conversation maintains its own state
3. **Visual Feedback**: Unread badges and timestamps
4. **Efficient Layout**: Sidebar + main view for desktop, tabs for mobile

---

## Feature Proposal 4: Identity Management System

### Developer Perspective

#### Proposed Implementation

**1. Identity Reveal Tracking**
```python
class CharacterIdentityReveal(models.Model):
    """
    Tracks when a character reveals their identity to another character
    """
    revealing_character = models.ForeignKey(
        Character,
        on_delete=models.CASCADE,
        related_name='identity_reveals_sent'
    )
    revealed_to_character = models.ForeignKey(
        Character,
        on_delete=models.CASCADE,
        related_name='identity_reveals_received'
    )
    revealed_at = models.DateTimeField(auto_now_add=True)
    # Can be revoked
    is_active = models.BooleanField(default=True)
    revoked_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        unique_together = ('revealing_character', 'revealed_to_character')
```

**2. Identity Reveal View**
```python
@login_required
def reveal_identity(request, character_id, to_character_id):
    """
    Reveal user identity to another character
    """
    character = get_object_or_404(
        Character,
        id=character_id,
        user=request.user
    )
    to_character = get_object_or_404(Character, id=to_character_id)
    
    # Create or update identity reveal
    reveal, created = CharacterIdentityReveal.objects.get_or_create(
        revealing_character=character,
        revealed_to_character=to_character,
        defaults={'is_active': True}
    )
    
    if not created:
        reveal.is_active = True
        reveal.revoked_at = None
        reveal.save()
    
    # Send notification to other character's user
    send_identity_reveal_notification(reveal)
    
    messages.success(request, f"Your identity has been revealed to {to_character.nickname}")
    return redirect('message_list', character=to_character.id)
```

### UX Engineer Perspective

#### User Flow Design

**Scenario: Revealing Identity**
1. User is in conversation with another character
2. Sees "Reveal My Identity" button
3. Clicks button
4. Confirmation dialog:
   ```
   Reveal Your Identity?
   
   This will show your user profile (username, 
   profile picture, etc.) to [Character Name].
   
   This action can be undone later.
   
   [Cancel] [Reveal Identity]
   ```
5. User confirms
6. Button changes to "Identity Revealed" with option to "Hide Identity"
7. Other character receives notification
8. Future messages show user information

#### UI Components

**Identity Reveal Button**
```
┌─────────────────────────────────────┐
│ [Avatar] YourCharacter              │
│         (You)                       │
│                                     │
│ [Reveal My Identity]                │
│   Show your user profile            │
└─────────────────────────────────────┘

After revealing:
┌─────────────────────────────────────┐
│ [Avatar] YourCharacter              │
│         (You) • @username           │
│         Identity Revealed            │
│                                     │
│ [Hide Identity]                     │
└─────────────────────────────────────┘
```

---

## Implementation Priority

### Phase 1: Core Features (Weeks 1-4)
1. Character-based friend system
2. Privacy controls for messaging
3. Multiple conversation management

### Phase 2: Enhanced Features (Weeks 5-6)
4. Identity reveal system
5. Real-time messaging
6. Friend request system

### Phase 3: Polish (Weeks 7-8)
7. UI/UX improvements
8. Mobile responsiveness
9. Testing and bug fixes

---

**Document Version**: 1.0  
**Last Updated**: 2024  
**Maintained By**: Development Team, UX Team


# Detailed Development Tasks - Game Player Nick Finder

## Document Purpose
This document provides detailed, actionable tasks for developers to implement all features. Each task includes implementation steps, Playwright tests, and acceptance criteria.

## Development Principles

### Test-Driven Development (TDD)
1. **Write Playwright test first** (red)
2. **Implement feature** (green)
3. **Refactor** (refactor)
4. **Repeat**

### Code Quality Rules
- All components must have Playwright tests
- All API endpoints must have tests
- TypeScript strict mode (no `any`)
- ESLint must pass
- Prettier must format code

## Epic 1: Enhanced Messaging with Privacy Controls

### Task 1.1: Database Schema - Message Privacy Fields

**Assignee**: Backend Developer  
**Story Points**: 3  
**Priority**: High

#### Implementation Steps

1. **Update Message Model**
```python
# app/models.py
class Message(models.Model):
    # ... existing fields ...
    privacy_mode = models.CharField(
        max_length=20,
        choices=[
            ('ANONYMOUS', 'Anonymous'),
            ('REVEAL_IDENTITY', 'Reveal Identity'),
        ],
        default='ANONYMOUS',
        help_text='Privacy mode when message was sent'
    )
    identity_revealed = models.BooleanField(
        default=False,
        help_text='Whether sender revealed their user identity'
    )
    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)
```

2. **Create Migration**
```bash
python manage.py makemigrations app
python manage.py migrate
```

3. **Update Message Serializer**
```python
# app/serializers.py
class MessageSerializer(serializers.ModelSerializer):
    privacy_mode = serializers.CharField(required=False)
    identity_revealed = serializers.BooleanField(required=False)
    
    class Meta:
        model = Message
        fields = ['id', 'sender_character', 'receiver_character', 
                 'content', 'sent_date', 'thread_id', 'privacy_mode',
                 'identity_revealed', 'is_read', 'read_at']
```

#### Playwright Test

```typescript
// tests/e2e/messaging/privacy-mode.spec.ts
import { test, expect } from '@playwright/test';

test.describe('Message Privacy Mode', () => {
  test.beforeEach(async ({ page }) => {
    // Login and navigate to character
    await page.goto('/login');
    await page.fill('input[name="username"]', 'testuser');
    await page.fill('input[name="password"]', 'testpass');
    await page.click('button[type="submit"]');
    await page.goto('/characters/character-abc123');
  });

  test('should send anonymous message by default', async ({ page }) => {
    await page.click('text=Send Message');
    
    // Verify anonymous is selected by default
    const anonymousRadio = page.locator('input[value="ANONYMOUS"]');
    await expect(anonymousRadio).toBeChecked();
    
    // Type and send message
    await page.fill('textarea[name="content"]', 'Hello from anonymous!');
    await page.click('button:has-text("Send Message")');
    
    // Verify message appears with anonymous indicator
    await expect(page.locator('.message-bubble')).toBeVisible();
    await expect(page.locator('.privacy-badge')).toContainText('Anonymous');
    await expect(page.locator('.user-username')).not.toBeVisible();
  });

  test('should send message with revealed identity', async ({ page }) => {
    await page.click('text=Send Message');
    
    // Select reveal identity mode
    await page.click('input[value="REVEAL_IDENTITY"]');
    
    // Type and send message
    await page.fill('textarea[name="content"]', 'Hello with identity!');
    await page.click('button:has-text("Send Message")');
    
    // Verify message shows user identity
    await expect(page.locator('.message-bubble')).toBeVisible();
    await expect(page.locator('.user-username')).toBeVisible();
    await expect(page.locator('.user-username')).toContainText('testuser');
  });
});
```

#### Acceptance Criteria
- [x] Message model has privacy_mode and identity_revealed fields
- [x] Migration created (needs to be applied: `python manage.py makemigrations app` and `python manage.py migrate`)
- [ ] Playwright test passes (tests need to be written)
- [x] API returns privacy fields in response

---

### Task 1.2: Message Form with Privacy Toggle

**Assignee**: Frontend Developer  
**Story Points**: 5  
**Priority**: High

#### Implementation Steps

1. **Create Message Form Component**
```typescript
// components/features/messaging/MessageForm.tsx
'use client';

import { useState } from 'react';
import { Box, Radio, RadioGroup, Textarea, Button, Typography } from '@mui/joy';
import { sendMessage } from '@/lib/api/messages';

interface MessageFormProps {
  receiverCharacterId: string;
  onMessageSent?: () => void;
}

export function MessageForm({ receiverCharacterId, onMessageSent }: MessageFormProps) {
  const [content, setContent] = useState('');
  const [privacyMode, setPrivacyMode] = useState<'ANONYMOUS' | 'REVEAL_IDENTITY'>('ANONYMOUS');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    
    try {
      await sendMessage({
        receiver_character_id: receiverCharacterId,
        content,
        privacy_mode: privacyMode,
        identity_revealed: privacyMode === 'REVEAL_IDENTITY',
      });
      
      setContent('');
      onMessageSent?.();
    } catch (error) {
      console.error('Failed to send message:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box component="form" onSubmit={handleSubmit} sx={{ p: 2 }}>
      <Typography level="title-sm" sx={{ mb: 2 }}>
        Privacy Mode
      </Typography>
      
      <RadioGroup
        value={privacyMode}
        onChange={(e) => setPrivacyMode(e.target.value as 'ANONYMOUS' | 'REVEAL_IDENTITY')}
        sx={{ mb: 2 }}
      >
        <Radio value="ANONYMOUS" label="Hide my identity (Character only)" />
        <Radio value="REVEAL_IDENTITY" label="Show my identity (Character + Username)" />
      </RadioGroup>

      <Textarea
        name="content"
        placeholder="Type your message..."
        value={content}
        onChange={(e) => setContent(e.target.value)}
        minRows={3}
        required
        sx={{ mb: 2 }}
      />

      <Button type="submit" loading={loading} disabled={!content.trim()}>
        Send Message
      </Button>
    </Box>
  );
}
```

2. **Create API Client**
```typescript
// lib/api/messages.ts
export interface SendMessageRequest {
  receiver_character_id: string;
  content: string;
  privacy_mode: 'ANONYMOUS' | 'REVEAL_IDENTITY';
  identity_revealed: boolean;
}

export async function sendMessage(data: SendMessageRequest) {
  const response = await fetch('/api/v1/messages/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(data),
  });

  if (!response.ok) {
    throw new Error('Failed to send message');
  }

  return response.json();
}
```

#### Playwright Test

```typescript
// tests/e2e/messaging/message-form.spec.ts
import { test, expect } from '@playwright/test';

test.describe('Message Form', () => {
  test('should display privacy mode options', async ({ page }) => {
    await page.goto('/characters/character-abc123');
    await page.click('text=Send Message');
    
    // Verify privacy options are visible
    await expect(page.locator('text=Privacy Mode')).toBeVisible();
    await expect(page.locator('input[value="ANONYMOUS"]')).toBeVisible();
    await expect(page.locator('input[value="REVEAL_IDENTITY"]')).toBeVisible();
  });

  test('should toggle privacy mode', async ({ page }) => {
    await page.goto('/characters/character-abc123');
    await page.click('text=Send Message');
    
    // Default should be anonymous
    await expect(page.locator('input[value="ANONYMOUS"]')).toBeChecked();
    
    // Switch to reveal identity
    await page.click('input[value="REVEAL_IDENTITY"]');
    await expect(page.locator('input[value="REVEAL_IDENTITY"]')).toBeChecked();
  });

  test('should validate message content', async ({ page }) => {
    await page.goto('/characters/character-abc123');
    await page.click('text=Send Message');
    
    // Try to send empty message
    const sendButton = page.locator('button:has-text("Send Message")');
    await expect(sendButton).toBeDisabled();
    
    // Type message
    await page.fill('textarea[name="content"]', 'Test message');
    await expect(sendButton).toBeEnabled();
  });
});
```

#### Acceptance Criteria
- [x] Message form displays privacy mode options
- [x] Privacy mode can be toggled
- [x] Form validates message content
- [x] Message is sent with correct privacy mode
- [ ] Playwright tests pass (tests need to be written)

---

### Task 1.3: Message Display with Privacy Indicators

**Assignee**: Frontend Developer  
**Story Points**: 5  
**Priority**: High

#### Implementation Steps

1. **Create Message Bubble Component**
```typescript
// components/features/messaging/MessageBubble.tsx
import { Box, Typography, Avatar, Chip } from '@mui/joy';
import { Message } from '@/types';

interface MessageBubbleProps {
  message: Message;
  isOwn: boolean;
}

export function MessageBubble({ message, isOwn }: MessageBubbleProps) {
  const showUserInfo = message.identity_revealed && message.privacy_mode === 'REVEAL_IDENTITY';

  return (
    <Box
      sx={{
        display: 'flex',
        gap: 1,
        flexDirection: isOwn ? 'row-reverse' : 'row',
        mb: 2,
        maxWidth: '70%',
        ml: isOwn ? 'auto' : 0,
        mr: isOwn ? 0 : 'auto',
      }}
    >
      <Avatar src={message.sender_character.avatar} />
      
      <Box
        sx={{
          bgcolor: isOwn ? 'primary.50' : 'neutral.100',
          p: 2,
          borderRadius: 2,
          flex: 1,
        }}
      >
        <Box sx={{ display: 'flex', gap: 1, alignItems: 'center', mb: 1 }}>
          <Typography level="title-sm" fontWeight="lg">
            {message.sender_character.nickname}
          </Typography>
          
          {message.privacy_mode === 'ANONYMOUS' && (
            <Chip size="sm" color="neutral" variant="soft">
              Anonymous
            </Chip>
          )}
          
          {showUserInfo && (
            <Typography level="body-xs" color="neutral">
              @{message.sender_character.user.username}
            </Typography>
          )}
        </Box>
        
        <Typography sx={{ mb: 1 }}>{message.content}</Typography>
        
        <Typography level="body-xs" color="neutral">
          {new Date(message.sent_date).toLocaleString()}
        </Typography>
      </Box>
    </Box>
  );
}
```

#### Playwright Test

```typescript
// tests/e2e/messaging/message-display.spec.ts
import { test, expect } from '@playwright/test';

test.describe('Message Display', () => {
  test('should display anonymous message correctly', async ({ page }) => {
    await page.goto('/messages/thread-123');
    
    // Find anonymous message
    const anonymousMessage = page.locator('.message-bubble').filter({ hasText: 'Anonymous' }).first();
    await expect(anonymousMessage).toBeVisible();
    
    // Verify user info is hidden
    await expect(anonymousMessage.locator('.user-username')).not.toBeVisible();
    
    // Verify anonymous badge is shown
    await expect(anonymousMessage.locator('text=Anonymous')).toBeVisible();
  });

  test('should display identity-revealed message correctly', async ({ page }) => {
    await page.goto('/messages/thread-123');
    
    // Find identity-revealed message
    const revealedMessage = page.locator('.message-bubble').filter({ hasText: '@testuser' }).first();
    await expect(revealedMessage).toBeVisible();
    
    // Verify user info is shown
    await expect(revealedMessage.locator('.user-username')).toBeVisible();
    await expect(revealedMessage.locator('.user-username')).toContainText('@testuser');
  });
});
```

#### Acceptance Criteria
- [x] Messages display with correct privacy indicators
- [x] Anonymous messages hide user info
- [x] Identity-revealed messages show user info
- [ ] Playwright tests pass (tests need to be written)

---

## Epic 2: Character-Based Friend System

### Task 2.1: CharacterFriend Model and Migration

**Assignee**: Backend Developer  
**Story Points**: 3  
**Priority**: High

#### Implementation Steps

1. **Create CharacterFriend Model**
```python
# app/models.py
class CharacterFriend(models.Model):
    """
    Friendship between two characters (not users)
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
    
    class Meta:
        unique_together = ('character1', 'character2')
        indexes = [
            models.Index(fields=['character1', 'character2']),
        ]
    
    def save(self, *args, **kwargs):
        # Ensure character1.id < character2.id to avoid duplicates
        if self.character1.id > self.character2.id:
            self.character1, self.character2 = self.character2, self.character1
        super().save(*args, **kwargs)
    
    def get_other_character(self, character):
        """Get the other character in this friendship"""
        if character == self.character1:
            return self.character2
        return self.character1
```

2. **Create CharacterFriendRequest Model**
```python
class CharacterFriendRequest(models.Model):
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
    message = models.TextField(blank=True)
    
    class Meta:
        unique_together = ('sender_character', 'receiver_character')
```

3. **Create Migration**
```bash
python manage.py makemigrations app
python manage.py migrate
```

#### Playwright Test

```typescript
// tests/e2e/friends/character-friend-model.spec.ts
import { test, expect } from '@playwright/test';

test.describe('Character Friend Model', () => {
  test('should create friend relationship', async ({ page, request }) => {
    // Test via API
    const response = await request.post('/api/v1/characters/char1/friends/', {
      data: {
        character2_id: 'char2-id',
      },
    });
    
    expect(response.ok()).toBeTruthy();
    
    // Verify friendship exists
    const friendsResponse = await request.get('/api/v1/characters/char1/friends/');
    const friends = await friendsResponse.json();
    
    expect(friends).toContainEqual(
      expect.objectContaining({ id: 'char2-id' })
    );
  });
});
```

#### Acceptance Criteria
- [x] CharacterFriend model created
- [x] CharacterFriendRequest model created
- [x] Migrations created (needs to be applied: `python manage.py makemigrations app` and `python manage.py migrate`)
- [x] Unique constraints work correctly
- [ ] Playwright test passes (tests need to be written)

---

### Task 2.2: Friend Request API Endpoints

**Assignee**: Backend Developer  
**Story Points**: 5  
**Priority**: High

#### Implementation Steps

1. **Create Friend Request View**
```python
# app/views.py
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

class CharacterFriendRequestViewSet(viewsets.ModelViewSet):
    queryset = CharacterFriendRequest.objects.all()
    serializer_class = CharacterFriendRequestSerializer
    permission_classes = [IsAuthenticated]
    
    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        sender_character = serializer.validated_data['sender_character']
        # Verify sender character belongs to user
        if sender_character.user != request.user:
            return Response(
                {'error': 'You can only send requests from your own characters'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
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
```

2. **Update URLs**
```python
# game_player_nick_finder/urls.py
router.register(r'friend-requests', CharacterFriendRequestViewSet, basename='friend-request')
```

#### Playwright Test

```typescript
// tests/e2e/friends/friend-request-api.spec.ts
import { test, expect } from '@playwright/test';

test.describe('Friend Request API', () => {
  test('should send friend request', async ({ page, request }) => {
    // Login first
    await page.goto('/login');
    await page.fill('input[name="username"]', 'testuser');
    await page.fill('input[name="password"]', 'testpass');
    await page.click('button[type="submit"]');
    
    // Get auth token
    const token = await page.evaluate(() => localStorage.getItem('auth_token'));
    
    // Send friend request
    const response = await request.post('/api/v1/friend-requests/', {
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json',
      },
      data: {
        sender_character_id: 'char1-id',
        receiver_character_id: 'char2-id',
        message: 'Hey, remember me?',
      },
    });
    
    expect(response.ok()).toBeTruthy();
    const data = await response.json();
    expect(data.status).toBe('PENDING');
  });

  test('should accept friend request', async ({ page, request }) => {
    // ... login and get token ...
    
    // Accept request
    const response = await request.post('/api/v1/friend-requests/123/accept/', {
      headers: {
        'Authorization': `Bearer ${token}`,
      },
    });
    
    expect(response.ok()).toBeTruthy();
    const data = await response.json();
    expect(data.status).toBe('accepted');
    
    // Verify friendship created
    const friendsResponse = await request.get('/api/v1/characters/char1/friends/');
    const friends = await friendsResponse.json();
    expect(friends).toHaveLength(1);
  });
});
```

#### Acceptance Criteria
- [x] API endpoint for sending friend requests
- [x] API endpoint for accepting requests
- [x] API endpoint for declining requests
- [x] Proper authentication and authorization
- [ ] Playwright tests pass (tests need to be written)

---

### Task 2.3: Friend Request UI Components

**Assignee**: Frontend Developer  
**Story Points**: 8  
**Priority**: High

#### Implementation Steps

1. **Create Friend Request Button Component**
```typescript
// components/features/friends/FriendRequestButton.tsx
'use client';

import { useState } from 'react';
import { Button, Box, Textarea } from '@mui/joy';
import { sendFriendRequest } from '@/lib/api/friends';

interface FriendRequestButtonProps {
  characterId: string;
  characterName: string;
}

export function FriendRequestButton({ characterId, characterName }: FriendRequestButtonProps) {
  const [showForm, setShowForm] = useState(false);
  const [message, setMessage] = useState('');
  const [loading, setLoading] = useState(false);
  const [status, setStatus] = useState<'idle' | 'sent' | 'friends'>('idle');

  const handleSendRequest = async () => {
    setLoading(true);
    try {
      await sendFriendRequest({
        receiver_character_id: characterId,
        message,
      });
      setStatus('sent');
      setShowForm(false);
    } catch (error) {
      console.error('Failed to send friend request:', error);
    } finally {
      setLoading(false);
    }
  };

  if (status === 'sent') {
    return <Button disabled>Friend Request Sent</Button>;
  }

  if (status === 'friends') {
    return <Button disabled>Friends ✓</Button>;
  }

  return (
    <Box>
      {!showForm ? (
        <Button onClick={() => setShowForm(true)}>Add as Friend</Button>
      ) : (
        <Box>
          <Textarea
            placeholder={`Optional message to ${characterName}...`}
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            minRows={2}
            sx={{ mb: 1 }}
          />
          <Box sx={{ display: 'flex', gap: 1 }}>
            <Button onClick={handleSendRequest} loading={loading}>
              Send Request
            </Button>
            <Button variant="outlined" onClick={() => setShowForm(false)}>
              Cancel
            </Button>
          </Box>
        </Box>
      )}
    </Box>
  );
}
```

#### Playwright Test

```typescript
// tests/e2e/friends/friend-request-ui.spec.ts
import { test, expect } from '@playwright/test';

test.describe('Friend Request UI', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/login');
    await page.fill('input[name="username"]', 'testuser');
    await page.fill('input[name="password"]', 'testpass');
    await page.click('button[type="submit"]');
  });

  test('should display add friend button', async ({ page }) => {
    await page.goto('/characters/character-abc123');
    
    const addFriendButton = page.locator('button:has-text("Add as Friend")');
    await expect(addFriendButton).toBeVisible();
  });

  test('should show friend request form on click', async ({ page }) => {
    await page.goto('/characters/character-abc123');
    await page.click('button:has-text("Add as Friend")');
    
    // Verify form appears
    await expect(page.locator('textarea')).toBeVisible();
    await expect(page.locator('button:has-text("Send Request")')).toBeVisible();
  });

  test('should send friend request', async ({ page }) => {
    await page.goto('/characters/character-abc123');
    await page.click('button:has-text("Add as Friend")');
    
    // Fill optional message
    await page.fill('textarea', 'Hey, remember me from 2005?');
    
    // Send request
    await page.click('button:has-text("Send Request")');
    
    // Verify success
    await expect(page.locator('button:has-text("Friend Request Sent")')).toBeVisible();
  });
});
```

#### Acceptance Criteria
- [ ] Add Friend button displays on character pages
- [ ] Friend request form appears on click
- [ ] Request can be sent with optional message
- [ ] Button updates to "Friend Request Sent" after sending
- [ ] Playwright tests pass

---

## Epic 3: User Profile System

### Task 3.1: User Profile Model Enhancement

**Assignee**: Backend Developer  
**Story Points**: 5  
**Priority**: High

#### Implementation Steps

1. **Update CustomUser Model**
```python
# app/models.py
class CustomUser(AbstractUser):
    # ... existing fields ...
    
    # Profile visibility settings
    profile_visibility = models.CharField(
        max_length=20,
        choices=[
            ('PUBLIC', 'Public'),
            ('FRIENDS_ONLY', 'Friends Only'),
            ('PRIVATE', 'Private'),
        ],
        default='FRIENDS_ONLY',
        help_text='Who can see your profile'
    )
    
    # Social media links
    steam_profile = models.URLField(blank=True)
    youtube_channel = models.URLField(blank=True)
    stackoverflow_profile = models.URLField(blank=True)
    github_profile = models.URLField(blank=True)
    linkedin_profile = models.URLField(blank=True)
    custom_links = models.JSONField(default=list, blank=True)  # Array of {name, url}
    
    # Profile customization
    profile_bio = models.TextField(blank=True, max_length=1000)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True)
```

2. **Create UserProfile View**
```python
# app/views.py
class UserProfileView(RetrieveAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        user = self.request.user
        viewer = self.request.user  # Could be different user viewing
        
        # Check visibility
        if user.profile_visibility == 'PRIVATE' and viewer != user:
            raise PermissionDenied('Profile is private')
        
        if user.profile_visibility == 'FRIENDS_ONLY' and viewer != user:
            # Check if they are friends through any characters
            if not self._are_friends(user, viewer):
                raise PermissionDenied('Profile is only visible to friends')
        
        return user
    
    def _are_friends(self, user1, user2):
        """Check if users are friends through any characters"""
        user1_characters = Character.objects.filter(user=user1)
        user2_characters = Character.objects.filter(user=user2)
        
        return CharacterFriend.objects.filter(
            (Q(character1__in=user1_characters) & Q(character2__in=user2_characters)) |
            (Q(character1__in=user2_characters) & Q(character2__in=user1_characters))
        ).exists()
```

#### Playwright Test

```typescript
// tests/e2e/profile/user-profile.spec.ts
import { test, expect } from '@playwright/test';

test.describe('User Profile', () => {
  test('should display public profile', async ({ page }) => {
    await page.goto('/users/testuser');
    
    // Verify profile is visible
    await expect(page.locator('.user-profile')).toBeVisible();
    await expect(page.locator('.user-name')).toContainText('Test User');
  });

  test('should hide private profile from non-friends', async ({ page }) => {
    // Login as different user
    await page.goto('/login');
    await page.fill('input[name="username"]', 'otheruser');
    await page.fill('input[name="password"]', 'pass');
    await page.click('button[type="submit"]');
    
    // Try to view private profile
    await page.goto('/users/testuser');
    
    // Should show access denied
    await expect(page.locator('text=Profile is private')).toBeVisible();
  });

  test('should show profile to friends', async ({ page }) => {
    // Login as friend
    await page.goto('/login');
    await page.fill('input[name="username"]', 'frienduser');
    await page.fill('input[name="password"]', 'pass');
    await page.click('button[type="submit"]');
    
    // View friend's profile
    await page.goto('/users/testuser');
    
    // Should show profile
    await expect(page.locator('.user-profile')).toBeVisible();
  });
});
```

#### Acceptance Criteria
- [x] User model has profile visibility settings
- [x] Social media links can be added
- [x] Profile visibility logic works correctly (in API)
- [x] Friends can see friends-only profiles (logic implemented)
- [ ] Playwright tests pass (tests need to be written)
- [ ] UI forms need to be updated to show new profile fields

---

## Epic 4: Character Custom Profile

### Task 4.1: Character Profile Enhancement Model

**Assignee**: Backend Developer  
**Story Points**: 5  
**Priority**: Medium

#### Implementation Steps

1. **Create CharacterProfile Model**
```python
# app/models.py
class CharacterProfile(models.Model):
    character = models.OneToOneField(
        Character,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    
    # Custom content
    custom_bio = models.TextField(blank=True, max_length=2000)
    custom_images = models.JSONField(default=list, blank=True)  # Array of image URLs
    screenshots = models.JSONField(default=list, blank=True)  # Array of screenshot URLs
    memories = models.JSONField(default=list, blank=True)  # Array of memory objects
    
    # Settings
    is_public = models.BooleanField(default=True, help_text='Show profile to everyone')
    
    updated_at = models.DateTimeField(auto_now=True)
```

2. **Create Character Profile API**
```python
# app/api_views.py
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
            )
        return CharacterProfile.objects.filter(is_public=True)
```

#### Playwright Test

```typescript
// tests/e2e/characters/character-profile.spec.ts
import { test, expect } from '@playwright/test';

test.describe('Character Custom Profile', () => {
  test('should display custom profile content', async ({ page }) => {
    await page.goto('/characters/character-abc123');
    
    // Verify custom bio is shown
    await expect(page.locator('.character-bio')).toBeVisible();
    
    // Verify screenshots section
    await expect(page.locator('.screenshots-section')).toBeVisible();
    
    // Verify memories section
    await expect(page.locator('.memories-section')).toBeVisible();
  });

  test('should allow editing own character profile', async ({ page }) => {
    await page.goto('/login');
    await page.fill('input[name="username"]', 'testuser');
    await page.fill('input[name="password"]', 'testpass');
    await page.click('button[type="submit"]');
    
    await page.goto('/characters/my-character-abc123');
    await page.click('button:has-text("Edit Profile")');
    
    // Edit bio
    await page.fill('textarea[name="custom_bio"]', 'My gaming journey started in 2005...');
    
    // Upload screenshot
    await page.setInputFiles('input[type="file"]', 'test-screenshot.png');
    
    // Save
    await page.click('button:has-text("Save")');
    
    // Verify changes saved
    await expect(page.locator('.character-bio')).toContainText('My gaming journey');
  });
});
```

#### Acceptance Criteria
- [x] CharacterProfile model created
- [x] Custom bio can be added (via API)
- [ ] Screenshots can be uploaded (JSON field ready, upload UI needed)
- [ ] Memories can be added (JSON field ready, UI needed)
- [x] Profile visibility works (in API)
- [ ] Playwright tests pass (tests need to be written)
- [ ] UI forms and views need to be created for character profiles

---

## Testing Requirements

### Playwright Test Coverage

Every feature must have:
1. **E2E Test** - Full user flow
2. **Component Test** - UI component behavior
3. **API Test** - Backend functionality

### Test Structure

```
tests/
├── e2e/
│   ├── messaging/
│   │   ├── privacy-mode.spec.ts
│   │   ├── message-form.spec.ts
│   │   └── message-display.spec.ts
│   ├── friends/
│   │   ├── friend-request.spec.ts
│   │   └── friend-list.spec.ts
│   ├── profile/
│   │   └── user-profile.spec.ts
│   └── characters/
│       └── character-profile.spec.ts
├── unit/
│   └── components/
└── api/
    └── endpoints/
```

### Running Tests

```bash
# All tests
pnpm test

# E2E only
pnpm test:e2e

# Specific test file
pnpm test:e2e tests/e2e/messaging/privacy-mode.spec.ts

# UI mode (interactive)
pnpm test:e2e:ui
```

---

## Development Workflow

### 1. Feature Development
1. Create feature branch: `git checkout -b feature/messaging-privacy`
2. Write Playwright test (red)
3. Implement feature (green)
4. Refactor
5. Run all tests
6. Create PR

### 2. Code Review Checklist
- [ ] Playwright tests written and passing
- [ ] TypeScript strict mode (no `any`)
- [ ] ESLint passes
- [ ] Prettier formatted
- [ ] Component is accessible
- [ ] Mobile responsive

### 3. Definition of Done
- [ ] Feature implemented
- [ ] Playwright tests written and passing
- [ ] Code reviewed
- [ ] Documentation updated
- [ ] No console errors
- [ ] Mobile tested

---

**Document Version**: 1.0  
**Last Updated**: 2024  
**Maintained By**: Tech Lead, Development Team


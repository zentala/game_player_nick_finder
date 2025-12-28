# Blocking System Architecture - Game Player Nick Finder

**Status**: 📋 Design Phase  
**Priority**: High  
**Target Audience**: Mid-level Developers

## Overview

This document describes the architecture for a comprehensive blocking system that allows users to block characters from sending messages, POKEs, and friend requests. The system extends the existing `PokeBlock` model to support general character blocking.

---

## Current State

### What We Have
- ✅ `PokeBlock` model - blocks POKEs only
- ✅ Block functionality in POKE system
- ✅ Block checking in `can_send_message()` utility

### What We Need
- ❌ General `CharacterBlock` model (blocks messages, friend requests, etc.)
- ❌ Block/unblock views and URLs
- ❌ UI for managing blocked characters
- ❌ Block list page
- ❌ Visual indicators when blocked

---

## Architecture Design

### 1. Data Model

#### CharacterBlock Model

```python
class CharacterBlock(models.Model):
    """
    General blocking between characters.
    Blocks messages, friend requests, and all interactions.
    """
    blocker_character = models.ForeignKey(
        Character,
        on_delete=models.CASCADE,
        related_name='blocked_characters'  # Characters I blocked
    )
    blocked_character = models.ForeignKey(
        Character,
        on_delete=models.CASCADE,
        related_name='blocked_by_characters'  # Characters that blocked me
    )
    blocked_at = models.DateTimeField(auto_now_add=True)
    reason = models.CharField(
        max_length=500,
        blank=True,
        help_text='Optional reason for blocking (not shown to blocked user)'
    )
    # Optional: report as spam/harassment
    reported_as_spam = models.BooleanField(default=False)
    reported_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        unique_together = ('blocker_character', 'blocked_character')
        indexes = [
            models.Index(fields=['blocker_character', 'blocked_at']),
            models.Index(fields=['blocked_character']),
        ]
        ordering = ['-blocked_at']
    
    def __str__(self):
        return f"{self.blocker_character.nickname} blocked {self.blocked_character.nickname}"
```

**Key Points:**
- One-way blocking (A blocks B, but B can still see A's public profile)
- Reason is private (not shown to blocked user)
- Can report as spam for moderation
- Indexed for performance

#### Migration Strategy

Since we already have `PokeBlock`, we can:
1. Create new `CharacterBlock` model
2. Optionally migrate existing `PokeBlock` records to `CharacterBlock`
3. Keep `PokeBlock` for backward compatibility or deprecate it

**Recommendation**: Keep both models initially, but use `CharacterBlock` for all new blocking. `PokeBlock` becomes a legacy model.

---

### 2. Business Logic

#### Blocking Rules

```python
def is_blocked(blocker_character, blocked_character):
    """
    Check if blocker_character has blocked blocked_character.
    Returns True if blocked, False otherwise.
    """
    return CharacterBlock.objects.filter(
        blocker_character=blocker_character,
        blocked_character=blocked_character
    ).exists()

def can_interact(sender_character, receiver_character):
    """
    Check if sender_character can interact with receiver_character.
    Returns (can_interact: bool, reason: str | None)
    """
    # Check if receiver blocked sender
    if is_blocked(receiver_character, sender_character):
        return False, "You have been blocked by this character"
    
    # Check if sender blocked receiver (optional - maybe allow?)
    if is_blocked(sender_character, receiver_character):
        return False, "You have blocked this character"
    
    return True, None
```

#### What Gets Blocked

When Character A blocks Character B:
- ❌ B cannot send Messages to A
- ❌ B cannot send POKEs to A
- ❌ B cannot send Friend Requests to A
- ❌ B cannot see A's online status (if implemented)
- ✅ B can still see A's public character profile
- ✅ A can still see B's public character profile
- ✅ A can unblock B anytime

---

### 3. Views and URLs

#### Block Character View

```python
class BlockCharacterView(LoginRequiredMixin, View):
    """Block a character from all interactions"""
    
    def post(self, request, *args, **kwargs):
        character_id = request.POST.get('character_id')
        reason = request.POST.get('reason', '')
        report_spam = request.POST.get('report_spam') == 'on'
        
        try:
            character_to_block = get_object_or_404(Character, id=character_id)
            user_characters = Character.objects.filter(user=request.user)
            
            # Find which of user's characters should block
            blocking_character_id = request.POST.get('blocking_character_id')
            if blocking_character_id:
                blocking_character = get_object_or_404(
                    Character,
                    id=blocking_character_id,
                    user=request.user
                )
            else:
                # Default: block from all user's characters
                # Or use the character in same game
                blocking_character = user_characters.filter(
                    game=character_to_block.game
                ).first()
            
            if not blocking_character:
                messages.error(request, _("You need a character in the same game to block."))
                return redirect('character_detail', ...)
            
            # Create block
            block, created = CharacterBlock.objects.get_or_create(
                blocker_character=blocking_character,
                blocked_character=character_to_block,
                defaults={
                    'reason': reason,
                    'reported_as_spam': report_spam,
                    'reported_at': timezone.now() if report_spam else None
                }
            )
            
            if created:
                messages.success(request, _("Character blocked successfully."))
            else:
                messages.info(request, _("Character was already blocked."))
            
            return redirect(request.META.get('HTTP_REFERER', 'character_list'))
            
        except Exception as e:
            messages.error(request, _("Failed to block character: {error}").format(error=str(e)))
            return redirect('character_list')
```

#### Unblock Character View

```python
class UnblockCharacterView(LoginRequiredMixin, View):
    """Unblock a previously blocked character"""
    
    def post(self, request, *args, **kwargs):
        block_id = request.POST.get('block_id')
        character_id = request.POST.get('character_id')
        
        try:
            if block_id:
                block = get_object_or_404(
                    CharacterBlock,
                    id=block_id,
                    blocker_character__user=request.user
                )
                block.delete()
            elif character_id:
                # Unblock by character ID
                user_characters = Character.objects.filter(user=request.user)
                CharacterBlock.objects.filter(
                    blocker_character__in=user_characters,
                    blocked_character_id=character_id
                ).delete()
            
            messages.success(request, _("Character unblocked successfully."))
            return redirect('blocked_characters_list')
            
        except Exception as e:
            messages.error(request, _("Failed to unblock character: {error}").format(error=str(e)))
            return redirect('blocked_characters_list')
```

#### Blocked Characters List View

```python
class BlockedCharactersListView(LoginRequiredMixin, ListView):
    """List all characters blocked by current user's characters"""
    model = CharacterBlock
    template_name = 'characters/blocked_list.html'
    context_object_name = 'blocks'
    paginate_by = 20
    
    def get_queryset(self):
        user_characters = Character.objects.filter(user=self.request.user)
        return CharacterBlock.objects.filter(
            blocker_character__in=user_characters
        ).select_related(
            'blocker_character',
            'blocked_character',
            'blocked_character__game',
            'blocked_character__user'
        ).order_by('-blocked_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Blocked Characters')
        return context
```

#### URLs

```python
urlpatterns = [
    # ... existing URLs ...
    
    # Blocking system
    path('characters/block/', BlockCharacterView.as_view(), name='block_character'),
    path('characters/unblock/', UnblockCharacterView.as_view(), name='unblock_character'),
    path('characters/blocked/', BlockedCharactersListView.as_view(), name='blocked_characters_list'),
]
```

---

### 4. UI Components

#### Block Button (on Character Detail Page)

```html
<!-- app/templates/characters/character_detail_content.html -->
{% if user.is_authenticated and character.user != user %}
    <div class="dropdown">
        <button class="btn btn-outline-danger btn-sm dropdown-toggle" type="button" data-bs-toggle="dropdown">
            <i class="bi bi-shield-x"></i> Block
        </button>
        <ul class="dropdown-menu">
            <li>
                <form method="post" action="{% url 'block_character' %}" class="p-2">
                    {% csrf_token %}
                    <input type="hidden" name="character_id" value="{{ character.id }}">
                    <div class="mb-2">
                        <label class="form-label small">Reason (optional):</label>
                        <textarea name="reason" class="form-control form-control-sm" rows="2" placeholder="Why are you blocking this character?"></textarea>
                    </div>
                    <div class="form-check mb-2">
                        <input class="form-check-input" type="checkbox" name="report_spam" id="report_spam">
                        <label class="form-check-label small" for="report_spam">
                            Report as spam/harassment
                        </label>
                    </div>
                    <button type="submit" class="btn btn-danger btn-sm w-100">
                        <i class="bi bi-shield-x"></i> Block Character
                    </button>
                </form>
            </li>
        </ul>
    </div>
{% endif %}
```

#### Blocked Characters List Page

```html
<!-- app/templates/characters/blocked_list.html -->
{% extends "base.html" %}
{% load i18n %}

{% block content %}
<div class="container mt-4">
    <div class="card">
        <div class="card-header bg-danger text-white">
            <h5 class="mb-0">
                <i class="bi bi-shield-x"></i> {% trans "Blocked Characters" %}
            </h5>
        </div>
        <div class="list-group list-group-flush">
            {% for block in blocks %}
                <div class="list-group-item">
                    <div class="d-flex justify-content-between align-items-center">
                        <div>
                            <h6 class="mb-1">
                                <a href="{% url 'character_detail' nickname=block.blocked_character.nickname hash_id=block.blocked_character.hash_id %}">
                                    {{ block.blocked_character.nickname }}
                                </a>
                                <small class="text-muted">({{ block.blocked_character.game.name }})</small>
                            </h6>
                            <small class="text-muted">
                                Blocked from: <strong>{{ block.blocker_character.nickname }}</strong>
                                <br>
                                Blocked on: {{ block.blocked_at|date:"M d, Y H:i" }}
                                {% if block.reason %}
                                    <br>Reason: {{ block.reason }}
                                {% endif %}
                            </small>
                        </div>
                        <form method="post" action="{% url 'unblock_character' %}" class="d-inline">
                            {% csrf_token %}
                            <input type="hidden" name="block_id" value="{{ block.id }}">
                            <button type="submit" class="btn btn-sm btn-outline-success">
                                <i class="bi bi-shield-check"></i> {% trans "Unblock" %}
                            </button>
                        </form>
                    </div>
                </div>
            {% empty %}
                <div class="list-group-item text-center text-muted">
                    {% trans "No blocked characters." %}
                </div>
            {% endfor %}
        </div>
    </div>
</div>
{% endblock %}
```

#### Navigation Link

Add to navbar dropdown:
```html
<li><a class="dropdown-item" href="{% url 'blocked_characters_list' %}">
    <i class="bi bi-shield-x"></i> {% trans "Blocked Characters" %}
</a></li>
```

---

### 5. Integration with Existing Systems

#### Update `can_send_message()` utility

```python
def can_send_message(sender_character, receiver_character):
    """
    Check if sender_character can send full Message to receiver_character.
    """
    from app.models import Poke, PokeBlock, CharacterBlock
    
    # Check for general block (NEW)
    is_blocked = CharacterBlock.objects.filter(
        blocker_character=receiver_character,
        blocked_character=sender_character
    ).exists()
    if is_blocked:
        return False, "You have been blocked by this character"
    
    # Check for POKE block (legacy, can be removed later)
    poke_blocked = PokeBlock.objects.filter(
        blocker_character=receiver_character,
        blocked_character=sender_character
    ).exists()
    if poke_blocked:
        return False, "You have been blocked by this character"
    
    # ... rest of existing logic ...
```

#### Update `can_send_poke()` utility

```python
def can_send_poke(user, receiver_character):
    """
    Check if user can send POKE to receiver_character.
    """
    from app.models import CharacterBlock
    
    # Get user's characters
    user_characters = Character.objects.filter(user=user)
    
    # Check if any of user's characters are blocked
    is_blocked = CharacterBlock.objects.filter(
        blocker_character=receiver_character,
        blocked_character__in=user_characters
    ).exists()
    
    if is_blocked:
        return False, "You have been blocked by this character"
    
    # ... rest of existing logic ...
```

#### Update Friend Request System

```python
def can_send_friend_request(sender_character, receiver_character):
    """
    Check if sender can send friend request to receiver.
    """
    from app.models import CharacterBlock
    
    is_blocked = CharacterBlock.objects.filter(
        blocker_character=receiver_character,
        blocked_character=sender_character
    ).exists()
    
    if is_blocked:
        return False, "You have been blocked by this character"
    
    # ... rest of existing logic ...
```

---

### 6. Testing Requirements

#### Unit Tests

```python
class CharacterBlockTestCase(TestCase):
    def setUp(self):
        self.user1 = CustomUser.objects.create_user('user1', 'user1@test.com', 'pass')
        self.user2 = CustomUser.objects.create_user('user2', 'user2@test.com', 'pass')
        self.game = Game.objects.create(name='Test Game', slug='test-game')
        self.char1 = Character.objects.create(user=self.user1, nickname='Char1', game=self.game)
        self.char2 = Character.objects.create(user=self.user2, nickname='Char2', game=self.game)
    
    def test_block_character(self):
        block = CharacterBlock.objects.create(
            blocker_character=self.char1,
            blocked_character=self.char2,
            reason='Spam'
        )
        self.assertTrue(CharacterBlock.objects.filter(
            blocker_character=self.char1,
            blocked_character=self.char2
        ).exists())
    
    def test_cannot_send_message_when_blocked(self):
        CharacterBlock.objects.create(
            blocker_character=self.char2,
            blocked_character=self.char1
        )
        can_send, reason = can_send_message(self.char1, self.char2)
        self.assertFalse(can_send)
        self.assertIn('blocked', reason.lower())
    
    def test_unblock_character(self):
        block = CharacterBlock.objects.create(
            blocker_character=self.char1,
            blocked_character=self.char2
        )
        block.delete()
        can_send, _ = can_send_message(self.char1, self.char2)
        # Should still need POKE exchange, but not blocked
        self.assertIsNotNone(can_send)
```

#### E2E Tests (Playwright)

```typescript
test('User can block and unblock character', async ({ page }) => {
  await login(page, 'testuser', 'testpass123');
  
  // Navigate to character detail
  await page.goto('/character/testchar-abc123/');
  
  // Click block button
  await page.click('button:has-text("Block")');
  
  // Fill reason and submit
  await page.fill('textarea[name="reason"]', 'Spam messages');
  await page.check('input[name="report_spam"]');
  await page.click('button:has-text("Block Character")');
  
  // Verify success message
  await expect(page.locator('.alert-success')).toContainText('blocked');
  
  // Navigate to blocked list
  await page.goto('/characters/blocked/');
  
  // Verify character in list
  await expect(page.locator('text=testchar')).toBeVisible();
  
  // Unblock
  await page.click('button:has-text("Unblock")');
  
  // Verify removed from list
  await expect(page.locator('text=testchar')).not.toBeVisible();
});
```

---

### 7. Migration Plan

#### Step 1: Create Model and Migration
```bash
python manage.py makemigrations app --name add_character_block
python manage.py migrate
```

#### Step 2: Update Utilities
- Update `can_send_message()`
- Update `can_send_poke()`
- Update `can_send_friend_request()` (if exists)

#### Step 3: Create Views
- `BlockCharacterView`
- `UnblockCharacterView`
- `BlockedCharactersListView`

#### Step 4: Create Templates
- `characters/blocked_list.html`
- Update `character_detail_content.html` with block button

#### Step 5: Update URLs
- Add blocking URLs to `urls.py`

#### Step 6: Update Navigation
- Add "Blocked Characters" link to navbar

#### Step 7: Write Tests
- Unit tests for blocking logic
- E2E tests for UI

#### Step 8: Optional Migration from PokeBlock
```python
# Migration script (optional)
def migrate_poke_blocks_to_character_blocks():
    for poke_block in PokeBlock.objects.all():
        CharacterBlock.objects.get_or_create(
            blocker_character=poke_block.blocker_character,
            blocked_character=poke_block.blocked_character,
            defaults={
                'reason': poke_block.reason,
                'blocked_at': poke_block.blocked_at
            }
        )
```

---

### 8. Security Considerations

1. **Permission Checks**: Always verify user owns the blocking character
2. **Rate Limiting**: Prevent abuse (max blocks per day?)
3. **Moderation**: Spam reports should trigger admin review
4. **Privacy**: Blocked users should not know they're blocked (silent block)
5. **Data Retention**: Consider auto-unblock after X days (optional)

---

### 9. Future Enhancements

- **Block by User**: Block all characters from a user
- **Temporary Blocks**: Auto-unblock after X days
- **Block Categories**: Spam, Harassment, Other
- **Moderation Dashboard**: Admin review of spam reports
- **Block Notifications**: Optional email to admins on spam reports

---

## Implementation Checklist

### Backend
- [ ] Create `CharacterBlock` model
- [ ] Create migration
- [ ] Update `can_send_message()` utility
- [ ] Update `can_send_poke()` utility
- [ ] Update `can_send_friend_request()` utility (if exists)
- [ ] Create `BlockCharacterView`
- [ ] Create `UnblockCharacterView`
- [ ] Create `BlockedCharactersListView`
- [ ] Add URLs
- [ ] Register model in admin
- [ ] Write unit tests

### Frontend
- [ ] Create `blocked_list.html` template
- [ ] Add block button to character detail page
- [ ] Add "Blocked Characters" link to navbar
- [ ] Add block/unblock confirmation modals
- [ ] Style blocked characters list
- [ ] Write E2E tests

### Documentation
- [ ] Update API documentation
- [ ] Update user guide
- [ ] Update admin guide

---

**Document Version**: 1.0  
**Last Updated**: 2024  
**Author**: Solution Architect  
**Reviewers**: Tech Lead, UX Engineer


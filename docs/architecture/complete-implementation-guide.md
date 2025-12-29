# Complete Implementation Guide - Blocking System & Message Visual Enhancements

**Status**: 📋 Ready for Implementation  
**Priority**: High  
**Target Audience**: Mid-level Developers  
**Estimated Time**: 2-3 days

---

## Overview

This guide provides step-by-step instructions for implementing:
1. **Character Blocking System** - Block characters from messaging, POKEs, and friend requests
2. **Message Visual Enhancements** - Different backgrounds and clearer visual hierarchy for masked/unmasked messages

---

## Prerequisites

Before starting, ensure you have:
- ✅ Django development environment set up
- ✅ Database migrations working
- ✅ Understanding of existing models (`Character`, `Message`, `Poke`)
- ✅ Access to templates and static files
- ✅ Playwright set up for E2E testing

---

## Part 1: Character Blocking System

### Step 1.1: Create CharacterBlock Model

**File**: `app/models.py`

Add after `CharacterIdentityReveal` model:

```python
class CharacterBlock(models.Model):
    """
    General blocking between characters.
    Blocks messages, friend requests, and all interactions.
    """
    blocker_character = models.ForeignKey(
        Character,
        on_delete=models.CASCADE,
        related_name='blocked_characters'
    )
    blocked_character = models.ForeignKey(
        Character,
        on_delete=models.CASCADE,
        related_name='blocked_by_characters'
    )
    blocked_at = models.DateTimeField(auto_now_add=True)
    reason = models.CharField(
        max_length=500,
        blank=True,
        help_text='Optional reason for blocking (not shown to blocked user)'
    )
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

**Action Items**:
- [ ] Add model to `app/models.py`
- [ ] Import in `app/admin.py`
- [ ] Create migration: `python manage.py makemigrations app --name add_character_block`
- [ ] Run migration: `python manage.py migrate`

---

### Step 1.2: Register Model in Admin

**File**: `app/admin.py`

Add to imports:
```python
from .models import (
    # ... existing imports ...
    CharacterBlock
)
```

Add admin class:
```python
class CharacterBlockAdmin(admin.ModelAdmin):
    list_display = ('blocker_character', 'blocked_character', 'reported_as_spam', 'blocked_at')
    list_filter = ('reported_as_spam', 'blocked_at')
    search_fields = ('blocker_character__nickname', 'blocked_character__nickname', 'reason')
    readonly_fields = ('blocked_at', 'reported_at')

admin.site.register(CharacterBlock, CharacterBlockAdmin)
```

**Action Items**:
- [ ] Add import
- [ ] Add admin class
- [ ] Register model

---

### Step 1.3: Update Utility Functions

**File**: `app/utils.py`

Add helper function:
```python
def is_blocked(blocker_character, blocked_character):
    """Check if blocker_character has blocked blocked_character"""
    from .models import CharacterBlock
    return CharacterBlock.objects.filter(
        blocker_character=blocker_character,
        blocked_character=blocked_character
    ).exists()
```

Update `can_send_message()`:
```python
def can_send_message(sender_character, receiver_character):
    """Check if sender_character can send full Message to receiver_character."""
    from .models import Poke, PokeBlock, CharacterBlock
    
    # Check for general block (NEW)
    is_blocked = CharacterBlock.objects.filter(
        blocker_character=receiver_character,
        blocked_character=sender_character
    ).exists()
    if is_blocked:
        return False, "You have been blocked by this character"
    
    # ... rest of existing logic ...
```

Update `can_send_poke()`:
```python
def can_send_poke(user, receiver_character):
    """Check if user can send POKE to receiver_character."""
    from .models import CharacterBlock
    
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

**Action Items**:
- [ ] Add `is_blocked()` helper
- [ ] Update `can_send_message()`
- [ ] Update `can_send_poke()`
- [ ] Write unit tests

---

### Step 1.4: Create Views

**File**: `app/views.py`

Add imports:
```python
from .models import CharacterBlock
from django.utils import timezone
```

Add views (see `docs/architecture/blocking-system-architecture.md` for full code):
- `BlockCharacterView`
- `UnblockCharacterView`
- `BlockedCharactersListView`

**Action Items**:
- [ ] Add imports
- [ ] Create `BlockCharacterView`
- [ ] Create `UnblockCharacterView`
- [ ] Create `BlockedCharactersListView`
- [ ] Write unit tests

---

### Step 1.5: Add URLs

**File**: `game_player_nick_finder/urls.py`

Add to imports:
```python
from app.views import (
    # ... existing imports ...
    BlockCharacterView, UnblockCharacterView, BlockedCharactersListView
)
```

Add URLs:
```python
urlpatterns = [
    # ... existing URLs ...
    
    # Blocking system
    path('characters/block/', BlockCharacterView.as_view(), name='block_character'),
    path('characters/unblock/', UnblockCharacterView.as_view(), name='unblock_character'),
    path('characters/blocked/', BlockedCharactersListView.as_view(), name='blocked_characters_list'),
]
```

**Action Items**:
- [ ] Add imports
- [ ] Add URL patterns

---

### Step 1.6: Create Templates

**File**: `app/templates/characters/blocked_list.html`

Create new template (see `docs/architecture/blocking-system-architecture.md` for full code).

**File**: `app/templates/characters/character_detail_content.html`

Add block button (see architecture doc for code).

**File**: `app/templates/base_navbar.html`

Add navigation link:
```html
<li><a class="dropdown-item" href="{% url 'blocked_characters_list' %}">
    <i class="bi bi-shield-x"></i> {% trans "Blocked Characters" %}
</a></li>
```

**Action Items**:
- [ ] Create `blocked_list.html`
- [ ] Add block button to character detail
- [ ] Add navigation link

---

## Part 2: Message Visual Enhancements

### Step 2.1: Update Message Template

**File**: `app/templates/messages/message_list.html`

The template has already been updated with:
- Different CSS classes for masked/unmasked messages
- User info section for unmasked messages
- Registration date display
- Better visual hierarchy

**Action Items**:
- [ ] Verify template changes are applied
- [ ] Test with masked messages
- [ ] Test with unmasked messages

---

### Step 2.2: Verify CSS Styles

**File**: `app/templates/messages/message_list.html` (in `<style>` section)

Ensure these styles are present:
- `.message-bubble.masked` - Gray background
- `.message-bubble.unmasked` - Blue/teal background
- `.identity-revealed-section` - User info section
- `.badge-real-name` - Green gradient badge
- `.badge-anonymous` - Gray badge

**Action Items**:
- [ ] Verify CSS is in template
- [ ] Test visual appearance
- [ ] Adjust colors if needed

---

## Part 3: Testing

### Step 3.1: Unit Tests

**File**: `app/tests.py` or `tests/unit/`

Create tests for:
- `CharacterBlock` model
- `is_blocked()` helper
- `can_send_message()` with blocks
- `can_send_poke()` with blocks
- Block/unblock views

**Action Items**:
- [ ] Write unit tests
- [ ] Run tests: `python manage.py test`
- [ ] Ensure all pass

---

### Step 3.2: E2E Tests

**File**: `tests/e2e/blocking/`

Create test files:
- `block-character.spec.ts`
- `unblock-character.spec.ts`
- `blocked-list.spec.ts`
- `blocked-interactions.spec.ts`

**Action Items**:
- [ ] Create test files
- [ ] Write E2E tests
- [ ] Run tests: `pnpm test:e2e`
- [ ] Ensure all pass

---

## Part 4: Verification Checklist

### Backend
- [ ] `CharacterBlock` model created
- [ ] Migration applied
- [ ] Model registered in admin
- [ ] `is_blocked()` helper works
- [ ] `can_send_message()` checks blocks
- [ ] `can_send_poke()` checks blocks
- [ ] Block view works
- [ ] Unblock view works
- [ ] List view works
- [ ] Unit tests pass

### Frontend
- [ ] Block button on character detail page
- [ ] Blocked characters list page
- [ ] Navigation link added
- [ ] Masked messages have gray background
- [ ] Unmasked messages have blue background
- [ ] User info displays correctly
- [ ] Registration date shows
- [ ] Social links display
- [ ] E2E tests pass

### Documentation
- [ ] Code comments added
- [ ] README updated (if needed)
- [ ] API docs updated (if needed)

---

## Common Issues and Solutions

### Issue 1: Migration Fails
**Solution**: Check for existing `PokeBlock` conflicts. Consider renaming if needed.

### Issue 2: Block Check Not Working
**Solution**: Verify `is_blocked()` is called in all utility functions. Check database indexes.

### Issue 3: Visual Styles Not Applying
**Solution**: Clear browser cache. Check CSS class names match template. Verify Bootstrap is loaded.

### Issue 4: User Info Not Showing
**Solution**: Check `date_joined`, `first_name`, `last_name` are available in template context.

---

## Next Steps After Implementation

1. **User Testing**: Get feedback on blocking UI and message visuals
2. **Performance**: Monitor query performance with blocks
3. **Analytics**: Track block usage and spam reports
4. **Enhancements**: Consider "Block All from User" feature

---

## References

- **Blocking System Architecture**: `docs/architecture/blocking-system-architecture.md`
- **Blocking System Tasks**: `docs/scrum/blocking-system-tasks.md`
- **Message Visual Enhancements**: `docs/ux/message-visual-enhancements.md`
- **Identity Reveal UX**: `docs/ux/identity-reveal-ux-improvements.md`

---

## Support

If you encounter issues:
1. Check the architecture documents
2. Review existing code patterns
3. Check Django/Playwright documentation
4. Ask for code review

---

**Document Version**: 1.0  
**Last Updated**: 2024  
**Author**: Solution Architect  
**Reviewers**: Tech Lead, UX Engineer



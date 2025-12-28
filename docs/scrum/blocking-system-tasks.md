# Blocking System - Task Breakdown for Social Marketing Team

**Epic**: User Safety and Privacy Controls  
**Priority**: High  
**Story Points**: 13  
**Estimated Time**: 2-3 days

---

## User Story

**As a** user  
**I want to** block characters that send unwanted messages or spam  
**So that** I can control who can contact me and maintain a safe environment

**Acceptance Criteria**:
- User can block any character from sending messages, POKEs, or friend requests
- User can see a list of all blocked characters
- User can unblock characters anytime
- Blocked users cannot see that they are blocked (silent block)
- Blocking prevents all future interactions
- User can optionally report blocked character as spam

---

## Task Breakdown

### Task 1: Data Model Implementation
**Story Points**: 3  
**Priority**: Critical  
**Assigned To**: Backend Developer

**Description**: Create `CharacterBlock` model to store blocking relationships.

**Subtasks**:
1. Create `CharacterBlock` model in `app/models.py`
   - Fields: `blocker_character`, `blocked_character`, `blocked_at`, `reason`, `reported_as_spam`, `reported_at`
   - Add `unique_together` constraint
   - Add database indexes
   - Add `__str__` method

2. Register model in `app/admin.py`
   - Create `CharacterBlockAdmin` class
   - Add list display, filters, search fields

3. Create and run migration
   ```bash
   python manage.py makemigrations app --name add_character_block
   python manage.py migrate
   ```

4. Write unit tests
   - Test model creation
   - Test unique constraint
   - Test relationships

**Definition of Done**:
- [ ] Model created and tested
- [ ] Migration applied successfully
- [ ] Model registered in admin
- [ ] Unit tests pass

**Estimated Time**: 2-3 hours

---

### Task 2: Business Logic Updates
**Story Points**: 3  
**Priority**: Critical  
**Assigned To**: Backend Developer

**Description**: Update utility functions to check for blocks.

**Subtasks**:
1. Update `can_send_message()` in `app/utils.py`
   - Add `CharacterBlock` check
   - Return appropriate error message

2. Update `can_send_poke()` in `app/utils.py`
   - Add `CharacterBlock` check
   - Return appropriate error message

3. Create `can_send_friend_request()` utility (if not exists)
   - Add `CharacterBlock` check
   - Return appropriate error message

4. Create `is_blocked()` helper function
   ```python
   def is_blocked(blocker_character, blocked_character):
       return CharacterBlock.objects.filter(
           blocker_character=blocker_character,
           blocked_character=blocked_character
       ).exists()
   ```

5. Write unit tests for all utilities
   - Test blocking prevents messages
   - Test blocking prevents POKEs
   - Test blocking prevents friend requests
   - Test unblocking restores access

**Definition of Done**:
- [ ] All utility functions updated
- [ ] Blocking logic tested
- [ ] Unit tests pass
- [ ] No regressions in existing functionality

**Estimated Time**: 3-4 hours

---

### Task 3: Block Character View
**Story Points**: 2  
**Priority**: High  
**Assigned To**: Backend Developer

**Description**: Create view to block a character.

**Subtasks**:
1. Create `BlockCharacterView` in `app/views.py`
   - Handle POST requests
   - Validate user permissions
   - Create `CharacterBlock` record
   - Handle optional reason and spam report
   - Show success/error messages

2. Add URL pattern in `game_player_nick_finder/urls.py`
   ```python
   path('characters/block/', BlockCharacterView.as_view(), name='block_character'),
   ```

3. Write unit tests
   - Test successful block
   - Test permission checks
   - Test duplicate block handling
   - Test spam reporting

**Definition of Done**:
- [ ] View created and tested
- [ ] URL configured
- [ ] Unit tests pass
- [ ] Error handling implemented

**Estimated Time**: 2 hours

---

### Task 4: Unblock Character View
**Story Points**: 1  
**Priority**: High  
**Assigned To**: Backend Developer

**Description**: Create view to unblock a character.

**Subtasks**:
1. Create `UnblockCharacterView` in `app/views.py`
   - Handle POST requests
   - Validate user permissions
   - Delete `CharacterBlock` record
   - Show success message

2. Add URL pattern
   ```python
   path('characters/unblock/', UnblockCharacterView.as_view(), name='unblock_character'),
   ```

3. Write unit tests
   - Test successful unblock
   - Test permission checks
   - Test unblocking non-existent block

**Definition of Done**:
- [ ] View created and tested
- [ ] URL configured
- [ ] Unit tests pass

**Estimated Time**: 1 hour

---

### Task 5: Blocked Characters List View
**Story Points**: 2  
**Priority**: High  
**Assigned To**: Backend Developer

**Description**: Create view to list all blocked characters.

**Subtasks**:
1. Create `BlockedCharactersListView` in `app/views.py`
   - Filter blocks by user's characters
   - Include pagination
   - Select related objects for performance

2. Add URL pattern
   ```python
   path('characters/blocked/', BlockedCharactersListView.as_view(), name='blocked_characters_list'),
   ```

3. Write unit tests
   - Test list shows only user's blocks
   - Test pagination
   - Test empty list

**Definition of Done**:
- [ ] View created and tested
- [ ] URL configured
- [ ] Pagination working
- [ ] Unit tests pass

**Estimated Time**: 1-2 hours

---

### Task 6: Block Button UI
**Story Points**: 2  
**Priority**: High  
**Assigned To**: Frontend Developer

**Description**: Add block button to character detail page.

**Subtasks**:
1. Update `app/templates/characters/character_detail_content.html`
   - Add block dropdown button
   - Add form with reason textarea
   - Add spam report checkbox
   - Style with Bootstrap

2. Add confirmation modal (optional but recommended)
   - Warn user about consequences
   - Show what gets blocked

3. Write E2E test
   - Test block button appears
   - Test block form submission
   - Test success message

**Definition of Done**:
- [ ] Block button added
- [ ] Form styled correctly
- [ ] Confirmation modal works (if added)
- [ ] E2E test passes

**Estimated Time**: 2-3 hours

---

### Task 7: Blocked Characters List Page
**Story Points**: 2  
**Priority**: High  
**Assigned To**: Frontend Developer

**Description**: Create UI for viewing and managing blocked characters.

**Subtasks**:
1. Create `app/templates/characters/blocked_list.html`
   - Show list of blocked characters
   - Display block date and reason
   - Add unblock button for each
   - Style with Bootstrap

2. Add "Blocked Characters" link to navbar
   - Add to user dropdown menu
   - Add badge with count (optional)

3. Write E2E test
   - Test list displays correctly
   - Test unblock functionality
   - Test empty state

**Definition of Done**:
- [ ] Template created and styled
- [ ] Navigation link added
- [ ] Unblock functionality works
- [ ] E2E test passes

**Estimated Time**: 2-3 hours

---

### Task 8: Visual Indicators for Blocked Users
**Story Points**: 1  
**Priority**: Medium  
**Assigned To**: Frontend Developer

**Description**: Show visual indicators when viewing blocked users.

**Subtasks**:
1. Update character detail page
   - Show "You have blocked this character" message
   - Disable message/POKE buttons
   - Show unblock option

2. Update message list
   - Show indicator if conversation is with blocked user
   - Disable message sending

3. Write E2E test
   - Test indicators appear correctly
   - Test buttons are disabled

**Definition of Done**:
- [ ] Indicators added
- [ ] Buttons disabled appropriately
- [ ] E2E test passes

**Estimated Time**: 1-2 hours

---

### Task 9: E2E Test Suite
**Story Points**: 2  
**Priority**: High  
**Assigned To**: QA Engineer / Developer

**Description**: Create comprehensive E2E tests for blocking system.

**Subtasks**:
1. Create `tests/e2e/blocking/block-character.spec.ts`
   - Test block from character detail
   - Test block with reason
   - Test spam report

2. Create `tests/e2e/blocking/unblock-character.spec.ts`
   - Test unblock from list
   - Test unblock from detail page

3. Create `tests/e2e/blocking/blocked-list.spec.ts`
   - Test list displays correctly
   - Test pagination
   - Test empty state

4. Create `tests/e2e/blocking/blocked-interactions.spec.ts`
   - Test cannot send message to blocked
   - Test cannot send POKE to blocked
   - Test cannot send friend request to blocked

**Definition of Done**:
- [ ] All E2E tests created
- [ ] All tests pass
- [ ] Tests cover happy path and edge cases

**Estimated Time**: 3-4 hours

---

## Testing Checklist

### Unit Tests
- [ ] Model creation and relationships
- [ ] `is_blocked()` helper function
- [ ] `can_send_message()` with blocks
- [ ] `can_send_poke()` with blocks
- [ ] `can_send_friend_request()` with blocks
- [ ] Block view permissions
- [ ] Unblock view permissions
- [ ] List view filtering

### E2E Tests
- [ ] Block character from detail page
- [ ] Block with reason and spam report
- [ ] View blocked characters list
- [ ] Unblock character
- [ ] Cannot send message to blocked
- [ ] Cannot send POKE to blocked
- [ ] Cannot send friend request to blocked
- [ ] Visual indicators appear correctly

### Manual Testing
- [ ] Block character
- [ ] Unblock character
- [ ] View blocked list
- [ ] Try to message blocked character (should fail)
- [ ] Try to POKE blocked character (should fail)
- [ ] Try to friend request blocked character (should fail)
- [ ] Spam report creates record
- [ ] Admin can see spam reports

---

## Dependencies

- ✅ Existing `Character` model
- ✅ Existing `can_send_message()` utility
- ✅ Existing `can_send_poke()` utility
- ✅ Bootstrap 5 for UI
- ✅ Django authentication system

---

## Risks and Mitigations

### Risk 1: Performance Impact
**Risk**: Blocking checks on every message/POKE could slow down system  
**Mitigation**: Add database indexes, use `select_related()` in queries

### Risk 2: User Confusion
**Risk**: Users might not understand what blocking does  
**Mitigation**: Clear UI messages, help text, confirmation modals

### Risk 3: Abuse of Blocking
**Risk**: Users might block everyone  
**Mitigation**: Monitor block rates, consider rate limiting if needed

---

## Success Metrics

- **Functionality**: All blocking features work correctly
- **Performance**: Blocking checks add <50ms to request time
- **User Satisfaction**: Users can successfully block unwanted contacts
- **Test Coverage**: >80% code coverage for blocking system

---

## Notes for Implementation

1. **Silent Blocking**: Blocked users should NOT know they're blocked. Don't show error messages that reveal blocking status.

2. **One-Way Blocking**: If A blocks B, B can still see A's public profile, but cannot interact.

3. **Spam Reports**: Spam reports should be visible to admins for moderation.

4. **Migration**: Consider migrating existing `PokeBlock` records to `CharacterBlock` for consistency.

5. **Future Enhancement**: Consider "Block All Characters from User" feature.

---

**Document Version**: 1.0  
**Last Updated**: 2024  
**Created By**: Social Marketing Team  
**Reviewed By**: Solution Architect, Tech Lead


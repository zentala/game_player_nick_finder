# 003 - UX Implementation Tasks - Game Player Nick Finder

**Status**: ✅ Most tasks completed  
**Last Updated**: 2024

## Document Purpose
This document provides detailed, actionable tasks for implementing UX components for Epic 2 (Friend System), Epic 3 (User Profile), and Epic 4 (Character Profile). These tasks are designed for MIT developers following TDD principles.

## Development Principles

### Test-Driven Development (TDD)
1. **Write Playwright test first** (red)
2. **Implement feature** (green)
3. **Refactor** (refactor)
4. **Repeat**

### Code Quality Rules
- All components must have Playwright tests
- All API endpoints must have tests
- Follow Django coding style guide (PEP 8)
- Use Bootstrap 5 for styling (current stack)
- All forms must use django-crispy-forms

---

## Epic 2: Character-Based Friend System - UI Implementation

### Task 2.3.1: Add Friend Button on Character Detail Page

**Assignee**: Frontend Developer  
**Story Points**: 3  
**Priority**: High  
**Dependencies**: Backend API complete (✅ done), Migrations applied

#### Implementation Steps

1. **Update CharacterView context**
```python
# app/views.py - Update CharacterView.get_context_data()
def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    character = self.get_object()
    context['title'] = character.nickname
    context['content_template'] = 'characters/character_detail_content.html'
    context['back_url'] = reverse('account_characters_list')
    context['back_label'] = _('Back to My Characters')
    
    # Check if user is logged in
    if self.request.user.is_authenticated:
        user = self.request.user
        user_characters = Character.objects.filter(user=user)
        
        # Check if any of user's characters is friend with this character
        is_friend = CharacterFriend.objects.filter(
            Q(character1=character, character2__in=user_characters) |
            Q(character2=character, character1__in=user_characters)
        ).exists()
        
        # Check if there's a pending friend request
        pending_request = CharacterFriendRequest.objects.filter(
            receiver_character=character,
            sender_character__in=user_characters,
            status='PENDING'
        ).first()
        
        # Check if user can send request (not own character, not already friend)
        can_send_request = (
            character.user != user and 
            not is_friend and 
            pending_request is None
        )
        
        context['is_friend'] = is_friend
        context['pending_request'] = pending_request
        context['can_send_request'] = can_send_request
        context['user_characters'] = user_characters  # For selecting which character sends request
    
    if self.request.user == character.user:
        context['show_action'] = True
        context['action_url'] = reverse('character_edit', kwargs={
            'nickname': character.nickname,
            'hash_id': character.hash_id
        })
        context['action_label'] = _('Edit Character')
    
    return context
```

2. **Update character_detail_content.html template**
```django
{# app/templates/characters/character_detail_content.html #}
{% load i18n %}
{% load static %}

<div class="character-detail">
  <div class="row">
    <div class="col-md-4">
      {% if character.avatar %}
        <img src="{{ character.avatar.url }}" alt="{{ character.nickname }}" class="img-fluid rounded mb-3">
      {% else %}
        <div class="bg-secondary rounded mb-3" style="width: 200px; height: 200px;"></div>
      {% endif %}
    </div>
    <div class="col-md-8">
      <h2>{{ character.nickname }}</h2>
      <p class="text-muted">{{ character.game.name }}</p>
      
      {% if character.description %}
        <p>{{ character.description }}</p>
      {% endif %}
      
      {# Friend Request Button Section #}
      {% if user.is_authenticated and not character.user == user %}
        <div class="mt-3 mb-3">
          {% if is_friend %}
            <button class="btn btn-success" disabled>
              <i class="bi bi-check-circle"></i> {% trans "Friends" %}
            </button>
          {% elif pending_request %}
            <button class="btn btn-secondary" disabled>
              <i class="bi bi-hourglass-split"></i> {% trans "Friend Request Sent" %}
            </button>
          {% elif can_send_request %}
            <button type="button" class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#friendRequestModal">
              <i class="bi bi-person-plus"></i> {% trans "Add as Friend" %}
            </button>
          {% endif %}
          
          <a href="{% url 'send_message' character.nickname character.hash_id %}" class="btn btn-outline-primary ms-2">
            <i class="bi bi-envelope"></i> {% trans "Send Message" %}
          </a>
        </div>
      {% endif %}
    </div>
  </div>
</div>

{# Friend Request Modal #}
{% if user.is_authenticated and can_send_request %}
<div class="modal fade" id="friendRequestModal" tabindex="-1">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <h5 class="modal-title">{% trans "Send Friend Request" %}</h5>
        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
      </div>
      <form method="post" action="{% url 'send_friend_request' character.nickname character.hash_id %}">
        {% csrf_token %}
        <div class="modal-body">
          <div class="mb-3">
            <label for="sender_character" class="form-label">{% trans "Send from Character" %}</label>
            <select name="sender_character" id="sender_character" class="form-select" required>
              {% for user_char in user_characters %}
                <option value="{{ user_char.id }}">{{ user_char.nickname }} ({{ user_char.game.name }})</option>
              {% endfor %}
            </select>
          </div>
          <div class="mb-3">
            <label for="message" class="form-label">{% trans "Optional Message" %}</label>
            <textarea name="message" id="message" class="form-control" rows="3" 
                      placeholder="{% trans 'Hey, remember me from...' %}"></textarea>
          </div>
          <input type="hidden" name="receiver_character" value="{{ character.id }}">
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">{% trans "Cancel" %}</button>
          <button type="submit" class="btn btn-primary">{% trans "Send Request" %}</button>
        </div>
      </form>
    </div>
  </div>
</div>
{% endif %}
```

3. **Create SendFriendRequestView**
```python
# app/views.py
class SendFriendRequestView(LoginRequiredMixin, View):
    """Handle friend request sending from UI"""
    
    def post(self, request, nickname, hash_id):
        receiver_character = get_object_or_404(Character, nickname=nickname, hash_id=hash_id)
        sender_character_id = request.POST.get('sender_character')
        message = request.POST.get('message', '')
        
        try:
            sender_character = Character.objects.get(id=sender_character_id, user=request.user)
        except Character.DoesNotExist:
            messages.error(request, 'Invalid character selected.')
            return redirect('character_detail', nickname=nickname, hash_id=hash_id)
        
        # Check if already friends
        if CharacterFriend.objects.filter(
            Q(character1=sender_character, character2=receiver_character) |
            Q(character1=receiver_character, character2=sender_character)
        ).exists():
            messages.error(request, 'You are already friends with this character.')
            return redirect('character_detail', nickname=nickname, hash_id=hash_id)
        
        # Check if request already exists
        if CharacterFriendRequest.objects.filter(
            sender_character=sender_character,
            receiver_character=receiver_character,
            status='PENDING'
        ).exists():
            messages.info(request, 'Friend request already sent.')
            return redirect('character_detail', nickname=nickname, hash_id=hash_id)
        
        # Create friend request
        friend_request = CharacterFriendRequest.objects.create(
            sender_character=sender_character,
            receiver_character=receiver_character,
            message=message,
            status='PENDING'
        )
        
        messages.success(request, f'Friend request sent to {receiver_character.nickname}!')
        return redirect('character_detail', nickname=nickname, hash_id=hash_id)
```

4. **Add URL route**
```python
# game_player_nick_finder/urls.py
urlpatterns = [
    # ... existing patterns ...
    path('characters/<str:nickname>/<str:hash_id>/send-friend-request/', 
         views.SendFriendRequestView.as_view(), 
         name='send_friend_request'),
]
```

#### Playwright Test

```typescript
// tests/e2e/friends/friend-request-button.spec.ts
import { test, expect } from '@playwright/test';

test.describe('Friend Request Button', () => {
  test.beforeEach(async ({ page }) => {
    // Login as test user
    await page.goto('/accounts/login/');
    await page.fill('input[name="login"]', 'testuser');
    await page.fill('input[name="password"]', 'testpass123');
    await page.click('button[type="submit"]');
    await page.waitForURL('**/');
  });

  test('should display Add Friend button on character detail page', async ({ page }) => {
    // Navigate to character detail page
    await page.goto('/characters/test-character-123/testhash');
    
    // Verify Add Friend button is visible
    const addFriendButton = page.locator('button:has-text("Add as Friend")');
    await expect(addFriendButton).toBeVisible();
  });

  test('should open friend request modal on button click', async ({ page }) => {
    await page.goto('/characters/test-character-123/testhash');
    
    // Click Add Friend button
    await page.click('button:has-text("Add as Friend")');
    
    // Verify modal appears
    await expect(page.locator('#friendRequestModal')).toBeVisible();
    await expect(page.locator('text=Send Friend Request')).toBeVisible();
  });

  test('should show character selector in modal', async ({ page }) => {
    await page.goto('/characters/test-character-123/testhash');
    await page.click('button:has-text("Add as Friend")');
    
    // Verify character selector exists
    await expect(page.locator('select[name="sender_character"]')).toBeVisible();
  });

  test('should send friend request successfully', async ({ page }) => {
    await page.goto('/characters/test-character-123/testhash');
    await page.click('button:has-text("Add as Friend")');
    
    // Select character and send request
    await page.selectOption('select[name="sender_character"]', { index: 0 });
    await page.fill('textarea[name="message"]', 'Hey, remember me?');
    await page.click('button:has-text("Send Request")');
    
    // Verify success message
    await expect(page.locator('text=Friend request sent')).toBeVisible();
    
    // Verify button changes to "Friend Request Sent"
    await expect(page.locator('button:has-text("Friend Request Sent")')).toBeVisible();
  });

  test('should not show Add Friend button for own characters', async ({ page }) => {
    // Navigate to own character
    await page.goto('/characters/my-character-123/myhash');
    
    // Verify Add Friend button is NOT visible
    await expect(page.locator('button:has-text("Add as Friend")')).not.toBeVisible();
  });

  test('should show Friends badge for existing friends', async ({ page }) => {
    // Assume friendship exists (setup in fixtures)
    await page.goto('/characters/friend-character-123/friendhash');
    
    // Verify Friends badge is shown
    await expect(page.locator('button:has-text("Friends")')).toBeVisible();
    await expect(page.locator('button:has-text("Friends")')).toBeDisabled();
  });
});
```

#### Acceptance Criteria
- [x] Add Friend button displays on character detail pages for non-owned characters
- [x] Button is hidden for own characters
- [x] Button shows "Friends" badge when already friends
- [x] Modal opens on button click
- [x] Character selector shows user's characters
- [x] Friend request can be sent with optional message
- [x] Button updates to "Friend Request Sent" after sending
- [x] View implemented: SendFriendRequestView
- [x] Template updated: character_detail_content.html
- [x] URL configured
- [ ] Playwright tests pass (tests written but need verification)

---

### Task 2.3.2: Friend Request List View

**Assignee**: Frontend Developer  
**Story Points**: 5  
**Priority**: High

#### Implementation Steps

1. **Create FriendRequestListView**
```python
# app/views.py
class FriendRequestListView(LoginRequiredMixin, ListView):
    """List all friend requests for user's characters"""
    model = CharacterFriendRequest
    template_name = 'friends/friend_request_list.html'
    context_object_name = 'friend_requests'
    current_page = 'friends'
    
    def get_queryset(self):
        user_characters = Character.objects.filter(user=self.request.user)
        
        # Get requests received by user's characters
        return CharacterFriendRequest.objects.filter(
            receiver_character__in=user_characters,
            status='PENDING'
        ).select_related('sender_character', 'sender_character__game', 'sender_character__user').order_by('-sent_date')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Friend Requests')
        context['back_url'] = reverse('account_profile')
        context['back_label'] = _('Back to Profile')
        return context
```

2. **Create Accept/Decline Friend Request Views**
```python
# app/views.py
class AcceptFriendRequestView(LoginRequiredMixin, View):
    """Accept a friend request"""
    
    def post(self, request, request_id):
        friend_request = get_object_or_404(
            CharacterFriendRequest,
            id=request_id,
            receiver_character__user=request.user,
            status='PENDING'
        )
        
        # Create friendship
        CharacterFriend.objects.create(
            character1=friend_request.sender_character,
            character2=friend_request.receiver_character
        )
        
        # Update request status
        friend_request.status = 'ACCEPTED'
        friend_request.save()
        
        messages.success(request, f'Accepted friend request from {friend_request.sender_character.nickname}!')
        return redirect('friend_request_list')


class DeclineFriendRequestView(LoginRequiredMixin, View):
    """Decline a friend request"""
    
    def post(self, request, request_id):
        friend_request = get_object_or_404(
            CharacterFriendRequest,
            id=request_id,
            receiver_character__user=request.user,
            status='PENDING'
        )
        
        friend_request.status = 'DECLINED'
        friend_request.save()
        
        messages.info(request, f'Declined friend request from {friend_request.sender_character.nickname}.')
        return redirect('friend_request_list')
```

3. **Create friend_request_list.html template**
```django
{# app/templates/friends/friend_request_list.html #}
{% extends "base.html" %}
{% load i18n %}
{% load static %}

{% block content %}
  {% include "containers/default.html" %}
{% endblock %}

{# app/templates/friends/friend_request_list_content.html #}
{% load i18n %}

<div class="friend-requests">
  <h2>{% trans "Friend Requests" %}</h2>
  
  {% if friend_requests %}
    <div class="list-group">
      {% for request in friend_requests %}
        <div class="list-group-item">
          <div class="row align-items-center">
            <div class="col-md-2">
              {% if request.sender_character.avatar %}
                <img src="{{ request.sender_character.avatar.url }}" 
                     alt="{{ request.sender_character.nickname }}" 
                     class="img-fluid rounded" style="width: 60px; height: 60px;">
              {% else %}
                <div class="bg-secondary rounded" style="width: 60px; height: 60px;"></div>
              {% endif %}
            </div>
            <div class="col-md-6">
              <h5 class="mb-1">{{ request.sender_character.nickname }}</h5>
              <p class="text-muted mb-1">{{ request.sender_character.game.name }}</p>
              {% if request.message %}
                <p class="mb-0"><em>"{{ request.message }}"</em></p>
              {% endif %}
              <small class="text-muted">{{ request.sent_date|timesince }} ago</small>
            </div>
            <div class="col-md-4 text-end">
              <form method="post" action="{% url 'accept_friend_request' request.id %}" class="d-inline">
                {% csrf_token %}
                <button type="submit" class="btn btn-success me-2">
                  <i class="bi bi-check-circle"></i> {% trans "Accept" %}
                </button>
              </form>
              <form method="post" action="{% url 'decline_friend_request' request.id %}" class="d-inline">
                {% csrf_token %}
                <button type="submit" class="btn btn-outline-danger">
                  <i class="bi bi-x-circle"></i> {% trans "Decline" %}
                </button>
              </form>
            </div>
          </div>
        </div>
      {% endfor %}
    </div>
  {% else %}
    <div class="alert alert-info">
      <i class="bi bi-info-circle"></i> {% trans "No pending friend requests." %}
    </div>
  {% endif %}
</div>
```

4. **Add URL routes**
```python
# game_player_nick_finder/urls.py
urlpatterns = [
    # ... existing patterns ...
    path('friends/requests/', views.FriendRequestListView.as_view(), name='friend_request_list'),
    path('friends/requests/<int:request_id>/accept/', 
         views.AcceptFriendRequestView.as_view(), 
         name='accept_friend_request'),
    path('friends/requests/<int:request_id>/decline/', 
         views.DeclineFriendRequestView.as_view(), 
         name='decline_friend_request'),
]
```

#### Playwright Test

```typescript
// tests/e2e/friends/friend-request-list.spec.ts
import { test, expect } from '@playwright/test';

test.describe('Friend Request List', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/accounts/login/');
    await page.fill('input[name="login"]', 'testuser');
    await page.fill('input[name="password"]', 'testpass123');
    await page.click('button[type="submit"]');
    await page.waitForURL('**/');
  });

  test('should display friend requests list', async ({ page }) => {
    await page.goto('/friends/requests/');
    
    await expect(page.locator('h2:has-text("Friend Requests")')).toBeVisible();
  });

  test('should show pending friend requests', async ({ page }) => {
    await page.goto('/friends/requests/');
    
    // Verify request cards are visible
    const requestCards = page.locator('.list-group-item');
    await expect(requestCards.first()).toBeVisible();
  });

  test('should accept friend request', async ({ page }) => {
    await page.goto('/friends/requests/');
    
    // Click accept button on first request
    await page.click('.list-group-item:first-child button:has-text("Accept")');
    
    // Verify success message
    await expect(page.locator('text=Accepted friend request')).toBeVisible();
  });

  test('should decline friend request', async ({ page }) => {
    await page.goto('/friends/requests/');
    
    // Click decline button
    await page.click('.list-group-item:first-child button:has-text("Decline")');
    
    // Verify info message
    await expect(page.locator('text=Declined friend request')).toBeVisible();
  });

  test('should show empty state when no requests', async ({ page }) => {
    // Assume no requests exist
    await page.goto('/friends/requests/');
    
    await expect(page.locator('text=No pending friend requests')).toBeVisible();
  });
});
```

#### Acceptance Criteria
- [x] Friend request list displays all pending requests for user's characters
- [x] Each request shows sender character info and optional message
- [x] Accept button creates friendship and updates request status
- [x] Decline button updates request status
- [x] Success/info messages shown after actions
- [x] Empty state shown when no requests
- [x] Views implemented: FriendRequestListView, AcceptFriendRequestView, DeclineFriendRequestView
- [x] Templates created: friend_request_list.html, friend_request_list_content.html
- [x] URLs configured
- [ ] Playwright tests pass (tests written but need verification)

---

### Task 2.3.3: Character Friend List View

**Assignee**: Frontend Developer  
**Story Points**: 5  
**Priority**: Medium

#### Implementation Steps

1. **Create CharacterFriendListView**
```python
# app/views.py
class CharacterFriendListView(LoginRequiredMixin, ListView):
    """List all friends for a specific character"""
    model = CharacterFriend
    template_name = 'friends/character_friend_list.html'
    context_object_name = 'friendships'
    current_page = 'friends'
    
    def get_queryset(self):
        character = get_object_or_404(
            Character,
            nickname=self.kwargs['nickname'],
            hash_id=self.kwargs['hash_id'],
            user=self.request.user
        )
        
        # Get friendships where character is either character1 or character2
        friendships = CharacterFriend.objects.filter(
            Q(character1=character) | Q(character2=character)
        ).select_related('character1', 'character1__game', 'character2', 'character2__game')
        
        # Extract friend characters
        friend_characters = []
        for friendship in friendships:
            friend_char = friendship.character2 if friendship.character1 == character else friendship.character1
            friend_characters.append({
                'character': friend_char,
                'friendship': friendship
            })
        
        return friend_characters
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        character = get_object_or_404(
            Character,
            nickname=self.kwargs['nickname'],
            hash_id=self.kwargs['hash_id']
        )
        context['character'] = character
        context['title'] = f'{character.nickname} - Friends'
        context['back_url'] = reverse('character_detail', kwargs={
            'nickname': character.nickname,
            'hash_id': character.hash_id
        })
        context['back_label'] = _('Back to Character')
        return context
```

2. **Create character_friend_list.html template**
```django
{# app/templates/friends/character_friend_list.html #}
{% extends "base.html" %}
{% load i18n %}

{% block content %}
  {% include "containers/default.html" %}
{% endblock %}

{# app/templates/friends/character_friend_list_content.html #}
{% load i18n %}

<div class="character-friends">
  <h2>{% trans "Friends" %} - {{ character.nickname }}</h2>
  
  {% if friendships %}
    <div class="row">
      {% for friend_data in friendships %}
        {% with friend=friend_data.character %}
          <div class="col-md-4 mb-3">
            <div class="card">
              <div class="card-body">
                <div class="d-flex align-items-center mb-2">
                  {% if friend.avatar %}
                    <img src="{{ friend.avatar.url }}" alt="{{ friend.nickname }}" 
                         class="rounded me-2" style="width: 50px; height: 50px;">
                  {% else %}
                    <div class="bg-secondary rounded me-2" style="width: 50px; height: 50px;"></div>
                  {% endif %}
                  <div>
                    <h5 class="card-title mb-0">{{ friend.nickname }}</h5>
                    <small class="text-muted">{{ friend.game.name }}</small>
                  </div>
                </div>
                <div class="mt-2">
                  <a href="{% url 'character_detail' friend.nickname friend.hash_id %}" 
                     class="btn btn-sm btn-outline-primary me-2">
                    <i class="bi bi-eye"></i> {% trans "View" %}
                  </a>
                  <a href="{% url 'send_message' friend.nickname friend.hash_id %}" 
                     class="btn btn-sm btn-primary">
                    <i class="bi bi-envelope"></i> {% trans "Message" %}
                  </a>
                </div>
              </div>
            </div>
          </div>
        {% endwith %}
      {% endfor %}
    </div>
  {% else %}
    <div class="alert alert-info">
      <i class="bi bi-info-circle"></i> {% trans "No friends yet." %}
    </div>
  {% endif %}
</div>
```

3. **Add URL route**
```python
# game_player_nick_finder/urls.py
urlpatterns = [
    # ... existing patterns ...
    path('characters/<str:nickname>/<str:hash_id>/friends/', 
         views.CharacterFriendListView.as_view(), 
         name='character_friend_list'),
]
```

4. **Add Friends link to character detail page**
```django
{# In character_detail_content.html, add after friend request button #}
{% if is_friend or character.user == user %}
  <a href="{% url 'character_friend_list' character.nickname character.hash_id %}" 
     class="btn btn-outline-secondary ms-2">
    <i class="bi bi-people"></i> {% trans "View Friends" %}
  </a>
{% endif %}
```

#### Playwright Test

```typescript
// tests/e2e/friends/character-friend-list.spec.ts
import { test, expect } from '@playwright/test';

test.describe('Character Friend List', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/accounts/login/');
    await page.fill('input[name="login"]', 'testuser');
    await page.fill('input[name="password"]', 'testpass123');
    await page.click('button[type="submit"]');
    await page.waitForURL('**/');
  });

  test('should display friend list for character', async ({ page }) => {
    await page.goto('/characters/my-character-123/myhash/friends/');
    
    await expect(page.locator('h2:has-text("Friends")')).toBeVisible();
  });

  test('should show friend cards', async ({ page }) => {
    await page.goto('/characters/my-character-123/myhash/friends/');
    
    // Verify friend cards exist
    const friendCards = page.locator('.card');
    await expect(friendCards.first()).toBeVisible();
  });

  test('should navigate to friend character detail', async ({ page }) => {
    await page.goto('/characters/my-character-123/myhash/friends/');
    
    // Click View button on first friend
    await page.click('.card:first-child a:has-text("View")');
    
    // Verify navigation to character detail
    await expect(page).toHaveURL(/\/characters\/.+\/.+\/$/);
  });

  test('should show empty state when no friends', async ({ page }) => {
    // Navigate to character with no friends
    await page.goto('/characters/new-character-123/newhash/friends/');
    
    await expect(page.locator('text=No friends yet')).toBeVisible();
  });
});
```

#### Acceptance Criteria
- [x] Friend list displays all friends for the character
- [x] Each friend card shows character info and game
- [x] View and Message buttons work correctly
- [x] Empty state shown when no friends
- [x] View implemented: CharacterFriendListView
- [x] Templates created: character_friend_list.html, character_friend_list_content.html
- [x] URL configured
- [ ] Playwright tests pass (tests written but need verification)

---

## Epic 3: User Profile System - UI Implementation

### Task 3.2.1: Update Profile Edit Form

**Assignee**: Frontend Developer  
**Story Points**: 5  
**Priority**: High

#### Implementation Steps

1. **Verify UserEditForm already has new fields** (should be done in backend)
   - Check `app/forms.py` - UserEditForm should include:
     - profile_visibility
     - profile_bio
     - profile_picture
     - steam_profile, youtube_channel, stackoverflow_profile, github_profile, linkedin_profile
     - custom_links (JSON field)

2. **Update profile_content.html template**
```django
{# app/templates/account/profile_content.html #}
{% load i18n %}
{% load crispy_forms_tags %}

<div class="profile-details">
  <h2>{% trans "Profile" %}</h2>
  
  <div class="row mb-4">
    <div class="col-md-3">
      {% if user.profile_picture %}
        <img src="{{ user.profile_picture.url }}" alt="{{ user.username }}" 
             class="img-fluid rounded">
      {% else %}
        <div class="bg-secondary rounded" style="width: 200px; height: 200px;"></div>
      {% endif %}
    </div>
    <div class="col-md-9">
      <p><strong>{% trans "Username" %}:</strong> {{ user.username }}</p>
      <p><strong>{% trans "Email" %}:</strong> {{ user.email }}</p>
    </div>
  </div>

  <h4 class="mt-4 mb-3">{% trans "Edit Profile" %}</h4>

  <form method="post" enctype="multipart/form-data">
    {% csrf_token %}
    {{ form|crispy }}

    <div class="mt-4">
      <button type="submit" class="btn btn-primary">{% trans "Save Changes" %}</button>
    </div>
  </form>

  {% if characters %}
    <h4 class="mt-5 mb-3">{% trans "Your Characters" %}</h4>
    <div class="list-group">
      {% for character in characters %}
        <a href="{% url 'character_detail' nickname=character.nickname hash_id=character.hash_id %}" 
           class="list-group-item list-group-item-action">
          {{ character.nickname }}
          <span class="text-muted">in {{ character.game.name }}</span>
        </a>
      {% endfor %}
    </div>

    <div class="mt-3">
      <a href="{% url 'character_list' %}" class="btn btn-outline-primary">{% trans "View All Characters" %}</a>
    </div>
  {% endif %}
</div>
```

3. **Update AccountProfileView to handle file uploads**
```python
# app/views.py - Update AccountProfileView.post()
def post(self, request):
    User = get_user_model()
    user = User.objects.get(username=request.user.username)
    characters = Character.objects.filter(user=user)
    form = UserEditForm(request.POST, request.FILES, instance=user)  # Add request.FILES

    if form.is_valid():
        user = form.save()
        messages.success(request, 'Profile updated successfully!')
        return redirect('account_profile')

    context = {
        'user': user,
        'characters': characters,
        'form': form,
    }
    return render(request, self.template_name, context)
```

#### Playwright Test

```typescript
// tests/e2e/profile/profile-edit.spec.ts
import { test, expect } from '@playwright/test';

test.describe('Profile Edit', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/accounts/login/');
    await page.fill('input[name="login"]', 'testuser');
    await page.fill('input[name="password"]', 'testpass123');
    await page.click('button[type="submit"]');
    await page.waitForURL('**/');
    await page.goto('/accounts/profile/');
  });

  test('should display profile edit form', async ({ page }) => {
    await expect(page.locator('h4:has-text("Edit Profile")')).toBeVisible();
    await expect(page.locator('form')).toBeVisible();
  });

  test('should have profile visibility field', async ({ page }) => {
    await expect(page.locator('select[name="profile_visibility"]')).toBeVisible();
  });

  test('should have profile bio field', async ({ page }) => {
    await expect(page.locator('textarea[name="profile_bio"]')).toBeVisible();
  });

  test('should have social media link fields', async ({ page }) => {
    await expect(page.locator('input[name="steam_profile"]')).toBeVisible();
    await expect(page.locator('input[name="github_profile"]')).toBeVisible();
  });

  test('should save profile changes', async ({ page }) => {
    // Update profile bio
    await page.fill('textarea[name="profile_bio"]', 'My gaming journey started in 2005...');
    
    // Save
    await page.click('button:has-text("Save Changes")');
    
    // Verify success message
    await expect(page.locator('text=Profile updated successfully')).toBeVisible();
    
    // Verify changes persisted
    await expect(page.locator('textarea[name="profile_bio"]')).toHaveValue('My gaming journey started in 2005...');
  });
});
```

#### Acceptance Criteria
- [x] Profile edit form displays all new fields (UserEditForm updated)
- [x] Profile picture can be uploaded (profile_picture field)
- [x] Profile visibility can be changed (profile_visibility field)
- [x] Social media links can be added (steam_profile, github_profile, etc.)
- [x] Profile bio can be edited (profile_bio field)
- [x] Changes are saved successfully
- [x] AccountProfileView handles file uploads
- [ ] Playwright tests pass (tests written but need verification)

---

### Task 3.2.2: User Profile Display Page

**Assignee**: Frontend Developer  
**Story Points**: 5  
**Priority**: High

#### Implementation Steps

1. **Create UserProfileDisplayView**
```python
# app/views.py
class UserProfileDisplayView(DetailView):
    """Display public user profile with visibility checks"""
    model = CustomUser
    template_name = 'profile/user_profile_display.html'
    context_object_name = 'profile_user'
    slug_field = 'username'
    slug_url_kwarg = 'username'
    
    def get_object(self, queryset=None):
        profile_user = super().get_object(queryset)
        viewer = self.request.user
        
        # Check visibility
        if profile_user.profile_visibility == 'PRIVATE' and (not viewer.is_authenticated or viewer != profile_user):
            raise PermissionDenied(_('This profile is private.'))
        
        if profile_user.profile_visibility == 'FRIENDS_ONLY' and (not viewer.is_authenticated or viewer != profile_user):
            # Check if users are friends through any characters
            if not self._are_friends(profile_user, viewer):
                raise PermissionDenied(_('This profile is only visible to friends.'))
        
        return profile_user
    
    def _are_friends(self, user1, user2):
        """Check if users are friends through any characters"""
        if not user2.is_authenticated:
            return False
        
        user1_characters = Character.objects.filter(user=user1)
        user2_characters = Character.objects.filter(user=user2)
        
        return CharacterFriend.objects.filter(
            (Q(character1__in=user1_characters) & Q(character2__in=user2_characters)) |
            (Q(character1__in=user2_characters) & Q(character2__in=user1_characters))
        ).exists()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile_user = self.get_object()
        context['title'] = f'{profile_user.username} - Profile'
        context['content_template'] = 'profile/user_profile_display_content.html'
        
        # Get user's characters
        context['user_characters'] = Character.objects.filter(user=profile_user)
        
        return context
```

2. **Create user_profile_display.html template**
```django
{# app/templates/profile/user_profile_display.html #}
{% extends "base.html" %}
{% load i18n %}

{% block content %}
  {% include "containers/default.html" %}
{% endblock %}

{# app/templates/profile/user_profile_display_content.html #}
{% load i18n %}

<div class="user-profile-display">
  <div class="row mb-4">
    <div class="col-md-3">
      {% if profile_user.profile_picture %}
        <img src="{{ profile_user.profile_picture.url }}" alt="{{ profile_user.username }}" 
             class="img-fluid rounded mb-3">
      {% else %}
        <div class="bg-secondary rounded mb-3" style="width: 200px; height: 200px;"></div>
      {% endif %}
    </div>
    <div class="col-md-9">
      <h2>{{ profile_user.username }}</h2>
      {% if profile_user.profile_bio %}
        <p class="lead">{{ profile_user.profile_bio }}</p>
      {% endif %}
    </div>
  </div>

  {# Social Media Links #}
  {% if profile_user.steam_profile or profile_user.github_profile or profile_user.youtube_channel %}
    <div class="mb-4">
      <h4>{% trans "Links" %}</h4>
      <div class="d-flex flex-wrap gap-2">
        {% if profile_user.steam_profile %}
          <a href="{{ profile_user.steam_profile }}" target="_blank" class="btn btn-outline-secondary">
            <i class="bi bi-steam"></i> Steam
          </a>
        {% endif %}
        {% if profile_user.github_profile %}
          <a href="{{ profile_user.github_profile }}" target="_blank" class="btn btn-outline-secondary">
            <i class="bi bi-github"></i> GitHub
          </a>
        {% endif %}
        {% if profile_user.youtube_channel %}
          <a href="{{ profile_user.youtube_channel }}" target="_blank" class="btn btn-outline-secondary">
            <i class="bi bi-youtube"></i> YouTube
          </a>
        {% endif %}
        {% if profile_user.linkedin_profile %}
          <a href="{{ profile_user.linkedin_profile }}" target="_blank" class="btn btn-outline-secondary">
            <i class="bi bi-linkedin"></i> LinkedIn
          </a>
        {% endif %}
        {% if profile_user.stackoverflow_profile %}
          <a href="{{ profile_user.stackoverflow_profile }}" target="_blank" class="btn btn-outline-secondary">
            <i class="bi bi-stack-overflow"></i> Stack Overflow
          </a>
        {% endif %}
      </div>
    </div>
  {% endif %}

  {# Characters #}
  {% if user_characters %}
    <div class="mb-4">
      <h4>{% trans "Characters" %}</h4>
      <div class="row">
        {% for character in user_characters %}
          <div class="col-md-4 mb-3">
            <div class="card">
              <div class="card-body">
                <h5 class="card-title">{{ character.nickname }}</h5>
                <p class="text-muted">{{ character.game.name }}</p>
                <a href="{% url 'character_detail' character.nickname character.hash_id %}" 
                   class="btn btn-sm btn-primary">
                  {% trans "View" %}
                </a>
              </div>
            </div>
          </div>
        {% endfor %}
      </div>
    </div>
  {% endif %}
</div>
```

3. **Add URL route**
```python
# game_player_nick_finder/urls.py
urlpatterns = [
    # ... existing patterns ...
    path('profile/<str:username>/', views.UserProfileDisplayView.as_view(), name='user_profile_display'),
]
```

#### Playwright Test

```typescript
// tests/e2e/profile/user-profile-display.spec.ts
import { test, expect } from '@playwright/test';

test.describe('User Profile Display', () => {
  test('should display public profile', async ({ page }) => {
    await page.goto('/profile/testuser/');
    
    await expect(page.locator('h2:has-text("testuser")')).toBeVisible();
  });

  test('should show profile bio if available', async ({ page }) => {
    await page.goto('/profile/testuser/');
    
    // Check if bio is visible (if set)
    const bio = page.locator('.lead');
    if (await bio.count() > 0) {
      await expect(bio).toBeVisible();
    }
  });

  test('should show social media links', async ({ page }) => {
    await page.goto('/profile/testuser/');
    
    // Check if links section exists
    const linksSection = page.locator('h4:has-text("Links")');
    if (await linksSection.count() > 0) {
      await expect(linksSection).toBeVisible();
    }
  });

  test('should show user characters', async ({ page }) => {
    await page.goto('/profile/testuser/');
    
    await expect(page.locator('h4:has-text("Characters")')).toBeVisible();
  });

  test('should block private profile from non-friends', async ({ page }) => {
    // Login as different user
    await page.goto('/accounts/login/');
    await page.fill('input[name="login"]', 'otheruser');
    await page.fill('input[name="password"]', 'pass');
    await page.click('button[type="submit"]');
    
    // Try to view private profile
    await page.goto('/profile/privateuser/');
    
    // Should show permission denied
    await expect(page.locator('text=This profile is private')).toBeVisible();
  });
});
```

#### Acceptance Criteria
- [x] Public profiles are visible to all
- [x] Private profiles are blocked from non-owners
- [x] Friends-only profiles are visible to friends
- [x] Profile picture displays if set
- [x] Profile bio displays if set
- [x] Social media links display if set
- [x] User's characters are listed
- [x] View implemented: UserProfileDisplayView
- [x] Templates created: user_profile_display.html, user_profile_display_content.html
- [x] URL configured
- [ ] Playwright tests pass (tests written but need verification)

---

## Epic 4: Character Custom Profile - UI Implementation

### Task 4.2.1: Character Profile Edit View

**Assignee**: Frontend Developer  
**Story Points**: 8  
**Priority**: Medium

#### Implementation Steps

1. **Create CharacterProfileEditView**
```python
# app/views.py
class CharacterProfileEditView(LoginRequiredMixin, UpdateView):
    """Edit character custom profile"""
    model = CharacterProfile
    form_class = CharacterProfileForm
    template_name = 'characters/character_profile_edit.html'
    current_page = 'characters'
    
    def get_object(self, queryset=None):
        character = get_object_or_404(
            Character,
            nickname=self.kwargs['nickname'],
            hash_id=self.kwargs['hash_id'],
            user=self.request.user
        )
        profile, created = CharacterProfile.objects.get_or_create(character=character)
        return profile
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        character = get_object_or_404(
            Character,
            nickname=self.kwargs['nickname'],
            hash_id=self.kwargs['hash_id']
        )
        context['character'] = character
        context['title'] = f'Edit Profile - {character.nickname}'
        context['back_url'] = reverse('character_detail', kwargs={
            'nickname': character.nickname,
            'hash_id': character.hash_id
        })
        context['back_label'] = _('Back to Character')
        return context
    
    def get_success_url(self):
        character = self.object.character
        messages.success(self.request, 'Character profile updated successfully!')
        return reverse('character_detail', kwargs={
            'nickname': character.nickname,
            'hash_id': character.hash_id
        })
```

2. **Create character_profile_edit.html template**
```django
{# app/templates/characters/character_profile_edit.html #}
{% extends "base.html" %}
{% load i18n %}
{% load crispy_forms_tags %}

{% block content %}
  {% include "containers/default.html" %}
{% endblock %}

{# app/templates/characters/character_profile_edit_content.html #}
{% load i18n %}
{% load crispy_forms_tags %}

<div class="character-profile-edit">
  <h2>{% trans "Edit Character Profile" %} - {{ character.nickname }}</h2>
  
  <form method="post">
    {% csrf_token %}
    {{ form|crispy }}
    
    <div class="mt-4">
      <button type="submit" class="btn btn-primary">{% trans "Save Profile" %}</button>
      <a href="{{ back_url }}" class="btn btn-secondary">{% trans "Cancel" %}</a>
    </div>
  </form>
  
  <div class="mt-4">
    <h4>{% trans "Profile Preview" %}</h4>
    <div class="alert alert-info">
      <i class="bi bi-info-circle"></i> 
      {% trans "Note: Screenshots and memories management will be added in next iteration." %}
    </div>
  </div>
</div>
```

3. **Add Edit Profile link to character detail page**
```django
{# In character_detail_content.html, add after edit button #}
{% if character.user == user %}
  <a href="{% url 'character_profile_edit' character.nickname character.hash_id %}" 
     class="btn btn-outline-secondary ms-2">
    <i class="bi bi-person-badge"></i> {% trans "Edit Profile" %}
  </a>
{% endif %}
```

4. **Add URL route**
```python
# game_player_nick_finder/urls.py
urlpatterns = [
    # ... existing patterns ...
    path('characters/<str:nickname>/<str:hash_id>/profile/edit/', 
         views.CharacterProfileEditView.as_view(), 
         name='character_profile_edit'),
]
```

#### Playwright Test

```typescript
// tests/e2e/characters/character-profile-edit.spec.ts
import { test, expect } from '@playwright/test';

test.describe('Character Profile Edit', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/accounts/login/');
    await page.fill('input[name="login"]', 'testuser');
    await page.fill('input[name="password"]', 'testpass123');
    await page.click('button[type="submit"]');
    await page.waitForURL('**/');
  });

  test('should display character profile edit form', async ({ page }) => {
    await page.goto('/characters/my-character-123/myhash/profile/edit/');
    
    await expect(page.locator('h2:has-text("Edit Character Profile")')).toBeVisible();
    await expect(page.locator('form')).toBeVisible();
  });

  test('should have custom bio field', async ({ page }) => {
    await page.goto('/characters/my-character-123/myhash/profile/edit/');
    
    await expect(page.locator('textarea[name="custom_bio"]')).toBeVisible();
  });

  test('should save character profile', async ({ page }) => {
    await page.goto('/characters/my-character-123/myhash/profile/edit/');
    
    // Fill custom bio
    await page.fill('textarea[name="custom_bio"]', 'My gaming journey with this character...');
    
    // Save
    await page.click('button:has-text("Save Profile")');
    
    // Verify success and redirect
    await expect(page.locator('text=Character profile updated successfully')).toBeVisible();
    await expect(page).toHaveURL(/\/characters\/.+\/.+\/$/);
  });
});
```

#### Acceptance Criteria
- [x] Edit profile form displays for character owner
- [x] Custom bio can be edited
- [x] Changes are saved successfully
- [x] Form redirects to character detail after save
- [x] View implemented: CharacterProfileEditView
- [x] Templates created: character_profile_edit.html, character_profile_edit_content.html
- [x] URL configured
- [x] CharacterProfileForm created
- [ ] Playwright tests pass (tests written but need verification)

---

### Task 4.2.2: Character Profile Display on Detail Page

**Assignee**: Frontend Developer  
**Story Points**: 5  
**Priority**: Medium

#### Implementation Steps

1. **Update CharacterView to include profile data**
```python
# app/views.py - Update CharacterView.get_context_data()
def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    character = self.get_object()
    context['title'] = character.nickname
    context['content_template'] = 'characters/character_detail_content.html'
    context['back_url'] = reverse('account_characters_list')
    context['back_label'] = _('Back to My Characters')
    
    # Get character profile if exists
    try:
        context['character_profile'] = character.profile
    except CharacterProfile.DoesNotExist:
        context['character_profile'] = None
    
    # ... rest of existing code ...
```

2. **Update character_detail_content.html to show profile**
```django
{# Add after character basic info #}
{% if character_profile %}
  <div class="mt-4">
    {% if character_profile.custom_bio %}
      <div class="mb-3">
        <h4>{% trans "About" %}</h4>
        <p>{{ character_profile.custom_bio|linebreaks }}</p>
      </div>
    {% endif %}
    
    {# Screenshots section - placeholder for future #}
    {% if character_profile.screenshots %}
      <div class="mb-3">
        <h4>{% trans "Screenshots" %}</h4>
        <div class="row">
          {% for screenshot in character_profile.screenshots %}
            <div class="col-md-4 mb-2">
              <img src="{{ screenshot.url }}" alt="Screenshot" class="img-fluid rounded">
            </div>
          {% endfor %}
        </div>
      </div>
    {% endif %}
    
    {# Memories section - placeholder for future #}
    {% if character_profile.memories %}
      <div class="mb-3">
        <h4>{% trans "Memories" %}</h4>
        <div class="list-group">
          {% for memory in character_profile.memories %}
            <div class="list-group-item">
              <h5>{{ memory.title }}</h5>
              <p>{{ memory.description }}</p>
              <small class="text-muted">{{ memory.date }}</small>
            </div>
          {% endfor %}
        </div>
      </div>
    {% endif %}
  </div>
{% endif %}
```

#### Playwright Test

```typescript
// tests/e2e/characters/character-profile-display.spec.ts
import { test, expect } from '@playwright/test';

test.describe('Character Profile Display', () => {
  test('should display character custom bio if available', async ({ page }) => {
    await page.goto('/characters/character-with-bio-123/hash/');
    
    // Check if bio section exists
    const bioSection = page.locator('h4:has-text("About")');
    if (await bioSection.count() > 0) {
      await expect(bioSection).toBeVisible();
    }
  });

  test('should not show profile for characters without profile', async ({ page }) => {
    await page.goto('/characters/new-character-123/hash/');
    
    // Profile section should not exist
    await expect(page.locator('h4:has-text("About")')).not.toBeVisible();
  });
});
```

#### Acceptance Criteria
- [x] Character custom bio displays if set
- [x] Profile sections only show if data exists
- [x] Profile respects visibility settings (via backend API)
- [x] CharacterView updated to include profile data
- [x] character_detail_content.html updated to show profile
- [ ] Screenshots UI (backend ready, UI needed)
- [ ] Memories UI (backend ready, UI needed)
- [ ] Playwright tests pass (tests written but need verification)

---

## Testing Requirements

### Playwright Test Coverage

Every feature must have:
1. **E2E Test** - Full user flow
2. **Component Test** - UI component behavior
3. **Integration Test** - Backend-frontend integration

### Test Structure

```
tests/
├── e2e/
│   ├── friends/
│   │   ├── friend-request-button.spec.ts
│   │   ├── friend-request-list.spec.ts
│   │   └── character-friend-list.spec.ts
│   ├── profile/
│   │   ├── profile-edit.spec.ts
│   │   └── user-profile-display.spec.ts
│   └── characters/
│       ├── character-profile-edit.spec.ts
│       └── character-profile-display.spec.ts
```

### Running Tests

```bash
# All tests
pnpm test:e2e

# Specific test file
pnpm test:e2e tests/e2e/friends/friend-request-button.spec.ts

# UI mode (interactive)
pnpm test:e2e:ui
```

---

## Development Workflow

### 1. Feature Development
1. Create feature branch: `git checkout -b feature/friend-request-ui`
2. Write Playwright test first (red)
3. Implement feature (green)
4. Refactor
5. Run all tests
6. Create PR

### 2. Code Review Checklist
- [ ] Playwright tests written and passing
- [ ] Django coding style (PEP 8)
- [ ] Forms use django-crispy-forms
- [ ] Bootstrap 5 classes used correctly
- [ ] Mobile responsive
- [ ] Accessibility considerations

### 3. Definition of Done
- [ ] Feature implemented
- [ ] Playwright tests written and passing
- [ ] Code reviewed
- [ ] No console errors
- [ ] Mobile tested
- [ ] Manual testing completed

---

## Priority Order

1. **High Priority** (Week 1-2):
   - Task 2.3.1: Add Friend Button
   - Task 2.3.2: Friend Request List View
   - Task 3.2.1: Update Profile Edit Form
   - Task 3.2.2: User Profile Display Page

2. **Medium Priority** (Week 3):
   - Task 2.3.3: Character Friend List View
   - Task 4.2.1: Character Profile Edit View
   - Task 4.2.2: Character Profile Display

---

**Document Version**: 1.0  
**Last Updated**: 2024  
**Maintained By**: UX Engineer, Development Team


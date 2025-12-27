# 005 - Pending Tasks Implementation Guide

**Status**: 📋 Ready for implementation  
**Last Updated**: 2024  
**Priority**: Based on STATUS_REPORT.md priorities

## Document Purpose

This document provides detailed, actionable implementation tasks for all pending work identified in `STATUS_REPORT.md`. Each task includes:
- Detailed implementation steps
- Technical specifications
- Acceptance criteria
- Playwright test requirements
- Implementation guidance for software engineers

All tasks follow TDD principles: Write tests first, implement feature, refactor.

---

## High Priority Tasks

### Task 1: Playwright Tests Verification and Fixes

**Assignee**: QA Engineer / Developer  
**Story Points**: 8  
**Priority**: High  
**Dependencies**: Existing test files in `tests/e2e/`

#### Overview

All Playwright tests have been written but require verification. Tests need to be run, failures fixed, and all tests must pass before deployment.

#### Implementation Steps

1. **Setup Test Environment**
   ```bash
   # Ensure fixtures are loaded
   pipenv run python manage.py loaddata app/fixtures/categories_fixtures.json app/fixtures/games_fixtures.json app/fixtures/users_and_characters.json
   
   # Or use script
   .\load_fixtures.ps1  # Windows
   ./load_fixtures.sh   # Unix
   ```

2. **Run All Playwright Tests**
   ```bash
   pnpm test:e2e
   ```

3. **Identify Failing Tests**
   - Document all failing tests
   - Categorize failures:
     - Selector issues (wrong CSS selectors)
     - Authentication issues (fixture data problems)
     - Timing issues (needs wait conditions)
     - Feature not implemented (test ahead of implementation)

4. **Fix Test Issues**
   
   **Common Issues and Fixes:**
   
   a. **Selector Problems**
   - Check actual HTML structure in templates
   - Update selectors to match current DOM
   - Use more specific selectors (data-testid recommended)
   
   b. **Authentication/Fixtures**
   - Verify test users exist in fixtures
   - Ensure correct credentials: `testuser`/`testpass123`, `otheruser`/`pass`
   - Check user permissions
   
   c. **Timing Issues**
   - Add explicit waits: `await page.waitForSelector(...)`
   - Wait for navigation: `await page.waitForURL(...)`
   - Wait for API calls: `await page.waitForResponse(...)`

5. **Update Test Files**

   Example fix pattern:
   ```typescript
   // Before (might fail)
   await page.click('button:has-text("Send Message")');
   await expect(page.locator('.message-bubble')).toBeVisible();
   
   // After (more robust)
   await page.click('button:has-text("Send Message")');
   await page.waitForSelector('.message-bubble', { state: 'visible' });
   await expect(page.locator('.message-bubble')).toBeVisible();
   ```

6. **Run Tests in CI Mode**
   ```bash
   pnpm test:e2e --reporter=html
   ```

7. **Document Test Coverage**
   - List all passing tests
   - Document any known limitations
   - Ensure >80% E2E coverage

#### Test Files to Verify

Located in `tests/e2e/`:
- `characters/character-profile-display.spec.ts`
- `characters/character-profile-edit.spec.ts`
- `friends/character-friend-list.spec.ts`
- `friends/friend-request-button.spec.ts`
- `friends/friend-request-list.spec.ts`
- `profile/profile-edit.spec.ts`
- `profile/user-profile-display.spec.ts`

#### Acceptance Criteria

- [ ] All existing Playwright tests pass
- [ ] Test fixtures loaded correctly
- [ ] No flaky tests (run 3 times, all pass)
- [ ] Tests run in headless mode successfully
- [ ] Test coverage report generated
- [ ] Documentation updated with test status

#### Files to Modify

- Individual test files in `tests/e2e/` (as needed)
- `playwright.config.ts` (if configuration changes needed)
- `docs/TEST_FIXTURES.md` (update if fixtures change)

---

### Task 2: Conversation Management UI

**Assignee**: Frontend Developer  
**Story Points**: 13  
**Priority**: High  
**Dependencies**: Message model (thread_id exists ✅), MessageListView (basic implementation ✅)

#### Overview

Implement a conversation list UI that allows users to:
- See all their conversations grouped by thread_id
- Switch between conversations easily
- See unread message indicators
- See last message preview and timestamp

#### Technical Context

**Current State:**
- `Message` model has `thread_id` field (UUID)
- `MessageListView` already groups messages by thread_id in queryset
- Basic message list template exists at `app/templates/messages/message_list.html`

**What's Missing:**
- Conversation list sidebar/view
- Easy conversation switching UI
- Unread message count indicators
- Last message preview per conversation

#### Implementation Steps

1. **Update MessageListView to Provide Conversation List**

   ```python
   # app/views.py - Update MessageListView.get_context_data()
   
   def get_context_data(self, **kwargs):
       context = super().get_context_data(**kwargs)
       user = self.request.user
       user_characters = Character.objects.filter(user=user)
       
       # Get all unique thread_ids for this user
       user_threads = Message.objects.filter(
           models.Q(sender_character__in=user_characters) |
           models.Q(receiver_character__in=user_characters)
       ).values_list('thread_id', flat=True).distinct()
       
       # Build conversation list
       conversations = []
       for thread_id in user_threads:
           # Get messages in this thread
           thread_messages = Message.objects.filter(thread_id=thread_id).order_by('-sent_date')
           
           if thread_messages.exists():
               latest_message = thread_messages.first()
               
               # Determine other character (not user's character)
               if latest_message.sender_character in user_characters:
                   other_character = latest_message.receiver_character
               else:
                   other_character = latest_message.sender_character
               
               # Count unread messages for this thread
               unread_count = Message.objects.filter(
                   thread_id=thread_id,
                   receiver_character__in=user_characters,
                   is_read=False
               ).count()
               
               conversations.append({
                   'thread_id': thread_id,
                   'other_character': other_character,
                   'latest_message': latest_message,
                   'unread_count': unread_count,
                   'message_preview': latest_message.content[:100],  # First 100 chars
               })
       
       # Sort by latest message date (newest first)
       conversations.sort(key=lambda x: x['latest_message'].sent_date, reverse=True)
       
       context['conversations'] = conversations
       
       # Get current thread_id from URL
       context['current_thread_id'] = self.request.GET.get('thread_id')
       context['current_character_id'] = self.request.GET.get('character')
       
       # ... rest of existing context ...
       return context
   ```

2. **Create Conversation List Template Component**

   ```django
   {# app/templates/messages/conversation_list.html #}
   {% load i18n %}
   {% load static %}
   
   <div class="conversation-list">
     <div class="list-group">
       {% for conversation in conversations %}
         <a href="{% url 'message_list' %}?thread_id={{ conversation.thread_id }}&character={{ conversation.other_character.id }}"
            class="list-group-item list-group-item-action {% if conversation.thread_id == current_thread_id %}active{% endif %}">
           <div class="d-flex w-100 justify-content-between align-items-start">
             <div class="flex-grow-1">
               <div class="d-flex align-items-center mb-1">
                 <img src="{{ conversation.other_character.avatar.url|default:'/static/images/default-avatar.png' }}" 
                      alt="{{ conversation.other_character.nickname }}"
                      class="rounded-circle me-2" 
                      style="width: 40px; height: 40px;">
                 <h6 class="mb-0">{{ conversation.other_character.nickname }}</h6>
                 {% if conversation.unread_count > 0 %}
                   <span class="badge bg-primary rounded-pill ms-2">{{ conversation.unread_count }}</span>
                 {% endif %}
               </div>
               <p class="mb-1 text-muted small">
                 {{ conversation.message_preview }}{% if conversation.message_preview|length >= 100 %}...{% endif %}
               </p>
               <small class="text-muted">
                 {{ conversation.latest_message.sent_date|timesince }} ago
               </small>
             </div>
           </div>
         </a>
       {% empty %}
         <div class="list-group-item text-muted text-center">
           {% trans "No conversations yet. Start messaging someone!" %}
         </div>
       {% endfor %}
     </div>
   </div>
   ```

3. **Update Message List Template to Include Conversation List**

   ```django
   {# app/templates/messages/message_list.html #}
   {% extends "base.html" %}
   {% load i18n %}
   
   {% block content %}
   <div class="container-fluid">
     <div class="row">
       <!-- Conversation List Sidebar -->
       <div class="col-md-3 border-end">
         <div class="sticky-top" style="top: 20px;">
           <h5 class="mb-3">{% trans "Conversations" %}</h5>
           {% include 'messages/conversation_list.html' %}
         </div>
       </div>
       
       <!-- Message Thread Area -->
       <div class="col-md-9">
         {% if thread_id or receiver_character %}
           {# Existing message thread display #}
           {% for message in messages %}
             {# ... existing message display code ... #}
           {% endfor %}
           
           {# Message form #}
           {% if form %}
             <form method="post" class="mt-4">
               {% csrf_token %}
               {{ form.as_p }}
               <button type="submit" class="btn btn-primary">{% trans "Send Message" %}</button>
             </form>
           {% endif %}
         {% else %}
           <div class="text-center text-muted mt-5">
             <p>{% trans "Select a conversation from the list to view messages" %}</p>
           </div>
         {% endif %}
       </div>
     </div>
   </div>
   {% endblock %}
   ```

4. **Add Unread Message Indicator Helper Method**

   ```python
   # app/models.py - Add to Message model or create utility function
   
   @staticmethod
   def get_unread_count_for_user(user, thread_id=None):
       """Get unread message count for a user in a specific thread or all threads"""
       user_characters = Character.objects.filter(user=user)
       
       queryset = Message.objects.filter(
           receiver_character__in=user_characters,
           is_read=False
       )
       
       if thread_id:
           queryset = queryset.filter(thread_id=thread_id)
       
       return queryset.count()
   ```

5. **Create Helper Method to Mark Messages as Read**

   ```python
   # app/views.py - Add to MessageListView
   
   def get(self, request, *args, **kwargs):
       response = super().get(request, *args, **kwargs)
       
       # Mark messages as read when viewing a thread
       thread_id = request.GET.get('thread_id')
       if thread_id:
           user_characters = Character.objects.filter(user=request.user)
           Message.objects.filter(
               thread_id=thread_id,
               receiver_character__in=user_characters,
               is_read=False
           ).update(is_read=True, read_at=timezone.now())
       
       return response
   ```

6. **Add Mobile-Responsive Layout**

   Update template for mobile (collapsible sidebar):
   ```django
   <div class="container-fluid">
     <div class="row">
       <!-- Mobile: Collapsible button -->
       <div class="col-12 d-md-none mb-2">
         <button class="btn btn-outline-primary" type="button" data-bs-toggle="collapse" data-bs-target="#conversationSidebar">
           {% trans "Conversations" %}
         </button>
       </div>
       
       <!-- Sidebar: Hidden on mobile, visible on desktop -->
       <div class="col-md-3 border-end collapse d-md-block" id="conversationSidebar">
         <!-- ... conversation list ... -->
       </div>
       
       <!-- Message area -->
       <div class="col-12 col-md-9">
         <!-- ... message thread ... -->
       </div>
     </div>
   </div>
   ```

#### Playwright Test

```typescript
// tests/e2e/messaging/conversation-list.spec.ts
import { test, expect } from '@playwright/test';

test.describe('Conversation List', () => {
  test.beforeEach(async ({ page }) => {
    // Load fixtures
    // Login as testuser
    await page.goto('/login');
    await page.fill('input[name="login"]', 'testuser');
    await page.fill('input[name="password"]', 'testpass123');
    await page.click('button[type="submit"]');
    await page.waitForURL('**/');
  });

  test('should display conversation list', async ({ page }) => {
    await page.goto('/messages/');
    
    // Verify conversation list is visible
    await expect(page.locator('.conversation-list')).toBeVisible();
    
    // Verify at least one conversation appears (assuming fixtures have messages)
    const conversations = page.locator('.list-group-item');
    await expect(conversations.first()).toBeVisible();
  });

  test('should show unread message count', async ({ page }) => {
    await page.goto('/messages/');
    
    // Find conversation with unread messages
    const unreadBadge = page.locator('.badge').first();
    
    // If unread messages exist, badge should be visible
    if (await unreadBadge.isVisible()) {
      const count = await unreadBadge.textContent();
      expect(parseInt(count || '0')).toBeGreaterThan(0);
    }
  });

  test('should switch between conversations', async ({ page }) => {
    await page.goto('/messages/');
    
    // Click first conversation
    const firstConversation = page.locator('.list-group-item').first();
    const conversationText = await firstConversation.textContent();
    await firstConversation.click();
    
    // Verify URL contains thread_id
    await page.waitForURL(/\?thread_id=.*/);
    
    // Verify messages are displayed
    await expect(page.locator('.message-bubble, .message-item')).toBeVisible({ timeout: 5000 });
  });

  test('should highlight active conversation', async ({ page }) => {
    await page.goto('/messages/');
    
    // Click first conversation
    const firstConversation = page.locator('.list-group-item').first();
    await firstConversation.click();
    
    // Verify it has active class
    await expect(firstConversation).toHaveClass(/active/);
  });

  test('should show last message preview', async ({ page }) => {
    await page.goto('/messages/');
    
    const conversation = page.locator('.list-group-item').first();
    
    // Verify message preview text exists
    const preview = conversation.locator('.text-muted.small');
    await expect(preview).toBeVisible();
    
    const previewText = await preview.textContent();
    expect(previewText?.trim().length).toBeGreaterThan(0);
  });

  test('should show timestamp for last message', async ({ page }) => {
    await page.goto('/messages/');
    
    const conversation = page.locator('.list-group-item').first();
    const timestamp = conversation.locator('small.text-muted');
    
    await expect(timestamp).toBeVisible();
    const timeText = await timestamp.textContent();
    expect(timeText).toMatch(/ago|minute|hour|day/i);
  });
});
```

#### Acceptance Criteria

- [ ] Conversation list displays all user's conversations
- [ ] Each conversation shows other character's avatar and nickname
- [ ] Unread message count badge displays correctly
- [ ] Last message preview shows (first 100 chars)
- [ ] Timestamp shows relative time (e.g., "2 hours ago")
- [ ] Clicking conversation switches to that thread
- [ ] Active conversation is highlighted
- [ ] Messages marked as read when viewing thread
- [ ] Mobile-responsive (collapsible sidebar on mobile)
- [ ] Playwright tests pass

#### Files to Create/Modify

**Create:**
- `app/templates/messages/conversation_list.html`

**Modify:**
- `app/views.py` - Update `MessageListView.get_context_data()` and `get()` method
- `app/templates/messages/message_list.html` - Add conversation list sidebar
- `app/models.py` - Optionally add helper method for unread count

**Test:**
- `tests/e2e/messaging/conversation-list.spec.ts` (new file)

---

## Medium Priority Tasks

### Task 3: Character Profile Screenshots & Memories UI

**Assignee**: Frontend Developer  
**Story Points**: 13  
**Priority**: Medium  
**Dependencies**: CharacterProfile model (screenshots, memories JSONField exist ✅)

#### Overview

Implement UI for uploading screenshots and managing memories for character profiles. Backend fields exist (JSONField), but UI is missing.

#### Technical Context

**Current State:**
- `CharacterProfile` model has:
  - `screenshots`: JSONField (default=list) - Array of screenshot URLs
  - `memories`: JSONField (default=list) - Array of memory objects
- `CharacterProfileForm` exists but likely doesn't include these fields
- `CharacterProfileEditView` exists

**What's Needed:**
- Screenshot upload UI (file upload, display, delete)
- Memory management UI (add, edit, delete memories)
- Display screenshots and memories on character profile

#### Implementation Steps

1. **Update CharacterProfileForm to Include Screenshots**

   ```python
   # app/forms.py - Update CharacterProfileForm
   
   class CharacterProfileForm(forms.ModelForm):
       screenshots = forms.FileField(
           required=False,
           widget=forms.ClearableFileInput(attrs={'multiple': True}),
           help_text="Upload multiple screenshots (images only)"
       )
       
       class Meta:
           model = CharacterProfile
           fields = ['custom_bio', 'is_public', 'screenshots']  # Add screenshots
           
       def __init__(self, *args, **kwargs):
           super().__init__(*args, **kwargs)
           # Don't include screenshots in default field rendering
           # We'll handle it separately in template
           
       def save(self, commit=True):
           profile = super().save(commit=False)
           
           if commit:
               profile.save()
               
               # Handle screenshot uploads
               screenshots = self.cleaned_data.get('screenshots')
               if screenshots:
                   # Process multiple files
                   uploaded_files = self.files.getlist('screenshots')
                   screenshot_urls = list(profile.screenshots) if profile.screenshots else []
                   
                   for uploaded_file in uploaded_files:
                       # Save file to media/screenshots/
                       from django.core.files.storage import default_storage
                       from django.conf import settings
                       import os
                       
                       filename = default_storage.save(
                           f'screenshots/{profile.character.id}/{uploaded_file.name}',
                           uploaded_file
                       )
                       screenshot_url = default_storage.url(filename)
                       screenshot_urls.append(screenshot_url)
                   
                   profile.screenshots = screenshot_urls
                   profile.save()
           
           return profile
   ```

2. **Create Screenshot Upload Widget Template**

   ```django
   {# app/templates/characters/screenshot_upload.html #}
   {% load i18n %}
   
   <div class="screenshot-upload-section mb-4">
     <h5>{% trans "Screenshots" %}</h5>
     
     <!-- Existing Screenshots -->
     <div class="row mb-3" id="existing-screenshots">
       {% for screenshot_url in profile.screenshots %}
         <div class="col-md-3 mb-3 screenshot-item" data-url="{{ screenshot_url }}">
           <div class="card">
             <img src="{{ screenshot_url }}" class="card-img-top" alt="Screenshot" style="height: 150px; object-fit: cover;">
             <div class="card-body p-2">
               <button type="button" class="btn btn-sm btn-danger delete-screenshot" data-url="{{ screenshot_url }}">
                 {% trans "Delete" %}
               </button>
             </div>
           </div>
         </div>
       {% endfor %}
     </div>
     
     <!-- Upload New Screenshots -->
     <div class="mb-3">
       <label for="id_screenshots" class="form-label">{% trans "Upload Screenshots" %}</label>
       <input type="file" 
              class="form-control" 
              id="id_screenshots" 
              name="screenshots" 
              multiple 
              accept="image/*">
       <small class="form-text text-muted">{% trans "You can select multiple images" %}</small>
     </div>
   </div>
   ```

3. **Add JavaScript for Screenshot Management**

   ```javascript
   // app/static/app/screenshot-manager.js
   
   document.addEventListener('DOMContentLoaded', function() {
     // Delete screenshot handler
     document.querySelectorAll('.delete-screenshot').forEach(button => {
       button.addEventListener('click', function() {
         const screenshotUrl = this.dataset.url;
         const screenshotItem = this.closest('.screenshot-item');
         
         if (confirm('Are you sure you want to delete this screenshot?')) {
           // Remove from DOM
           screenshotItem.remove();
           
           // Add hidden input to mark for deletion
           const form = document.querySelector('form');
           const hiddenInput = document.createElement('input');
           hiddenInput.type = 'hidden';
           hiddenInput.name = 'delete_screenshots';
           hiddenInput.value = screenshotUrl;
           form.appendChild(hiddenInput);
         }
       });
     });
     
     // Preview uploaded images before submit
     const fileInput = document.getElementById('id_screenshots');
     if (fileInput) {
       fileInput.addEventListener('change', function(e) {
         const files = e.target.files;
         // Could add image preview here
       });
     }
   });
   ```

4. **Update CharacterProfileEditView to Handle Screenshot Deletion**

   ```python
   # app/views.py - Update CharacterProfileEditView.form_valid()
   
   def form_valid(self, form):
       profile = form.save(commit=False)
       
       # Handle screenshot deletions
       delete_screenshots = self.request.POST.getlist('delete_screenshots')
       if delete_screenshots:
           current_screenshots = list(profile.screenshots) if profile.screenshots else []
           profile.screenshots = [
               url for url in current_screenshots 
               if url not in delete_screenshots
           ]
       
       profile.save()
       return redirect('character_detail', ...)
   ```

5. **Create Memory Management Form Field**

   ```python
   # app/forms.py - Add memory management
   
   class MemoryForm(forms.Form):
       title = forms.CharField(max_length=200, required=True)
       description = forms.TextField(required=True)
       date = forms.DateField(required=False, help_text="Optional: When did this happen?")
   
   # Or handle in CharacterProfileForm as JSON
   class CharacterProfileForm(forms.ModelForm):
       # ... existing fields ...
       
       # Memories as JSON (handled via JavaScript in template)
       memories_json = forms.CharField(
           required=False,
           widget=forms.HiddenInput()
       )
       
       def save(self, commit=True):
           profile = super().save(commit=False)
           
           # Parse memories JSON
           memories_json = self.cleaned_data.get('memories_json')
           if memories_json:
               import json
               try:
                   profile.memories = json.loads(memories_json)
               except json.JSONDecodeError:
                   pass
           
           if commit:
               profile.save()
           
           return profile
   ```

6. **Create Memory Management UI Template**

   ```django
   {# app/templates/characters/memory_management.html #}
   {% load i18n %}
   
   <div class="memory-management-section mb-4">
     <h5>{% trans "Memories" %}</h5>
     
     <!-- Existing Memories -->
     <div id="existing-memories" class="mb-3">
       {% for memory in profile.memories %}
         <div class="card mb-2 memory-item" data-index="{{ forloop.counter0 }}">
           <div class="card-body">
             <div class="d-flex justify-content-between align-items-start">
               <div class="flex-grow-1">
                 <h6 class="memory-title">{{ memory.title }}</h6>
                 <p class="memory-description">{{ memory.description }}</p>
                 {% if memory.date %}
                   <small class="text-muted">{{ memory.date }}</small>
                 {% endif %}
               </div>
               <button type="button" class="btn btn-sm btn-danger delete-memory">{% trans "Delete" %}</button>
             </div>
           </div>
         </div>
       {% endfor %}
     </div>
     
     <!-- Add New Memory Form -->
     <div class="card">
       <div class="card-body">
         <h6>{% trans "Add New Memory" %}</h6>
         <form id="add-memory-form">
           <div class="mb-2">
             <input type="text" class="form-control" id="memory-title" placeholder="{% trans 'Memory title' %}" required>
           </div>
           <div class="mb-2">
             <textarea class="form-control" id="memory-description" rows="3" placeholder="{% trans 'Describe this memory...' %}" required></textarea>
           </div>
           <div class="mb-2">
             <input type="date" class="form-control" id="memory-date" placeholder="{% trans 'Date (optional)' %}">
           </div>
           <button type="submit" class="btn btn-primary btn-sm">{% trans "Add Memory" %}</button>
         </form>
       </div>
     </div>
     
     <!-- Hidden input to store memories JSON -->
     <input type="hidden" name="memories_json" id="memories-json" value="">
   </div>
   ```

7. **Add JavaScript for Memory Management**

   ```javascript
   // app/static/app/memory-manager.js
   
   document.addEventListener('DOMContentLoaded', function() {
     let memories = [];
     
     // Load existing memories from DOM
     document.querySelectorAll('.memory-item').forEach(item => {
       const title = item.querySelector('.memory-title').textContent;
       const description = item.querySelector('.memory-description').textContent;
       const date = item.querySelector('.text-muted')?.textContent || null;
       
       memories.push({ title, description, date });
     });
     
     // Update hidden input
     function updateMemoriesJson() {
       document.getElementById('memories-json').value = JSON.stringify(memories);
     }
     
     // Add memory
     document.getElementById('add-memory-form').addEventListener('submit', function(e) {
       e.preventDefault();
       
       const title = document.getElementById('memory-title').value;
       const description = document.getElementById('memory-description').value;
       const date = document.getElementById('memory-date').value || null;
       
       memories.push({ title, description, date });
       updateMemoriesJson();
       
       // Add to DOM
       const memoriesContainer = document.getElementById('existing-memories');
       const memoryHtml = `
         <div class="card mb-2 memory-item">
           <div class="card-body">
             <div class="d-flex justify-content-between align-items-start">
               <div class="flex-grow-1">
                 <h6 class="memory-title">${title}</h6>
                 <p class="memory-description">${description}</p>
                 ${date ? `<small class="text-muted">${date}</small>` : ''}
               </div>
               <button type="button" class="btn btn-sm btn-danger delete-memory">Delete</button>
             </div>
           </div>
         </div>
       `;
       memoriesContainer.insertAdjacentHTML('beforeend', memoryHtml);
       
       // Clear form
       this.reset();
       
       // Re-attach delete handlers
       attachDeleteHandlers();
     });
     
     // Delete memory
     function attachDeleteHandlers() {
       document.querySelectorAll('.delete-memory').forEach(button => {
         button.addEventListener('click', function() {
           const memoryItem = this.closest('.memory-item');
           const index = Array.from(memoryItem.parentNode.children).indexOf(memoryItem);
           
           memories.splice(index, 1);
           updateMemoriesJson();
           memoryItem.remove();
         });
       });
     }
     
     attachDeleteHandlers();
     updateMemoriesJson();
   });
   ```

8. **Update Character Profile Display Template**

   ```django
   {# app/templates/characters/character_detail_content.html #}
   {# Add screenshots section #}
   
   {% if character.profile.screenshots %}
     <div class="screenshots-section mt-4">
       <h5>{% trans "Screenshots" %}</h5>
       <div class="row">
         {% for screenshot_url in character.profile.screenshots %}
           <div class="col-md-4 mb-3">
             <img src="{{ screenshot_url }}" class="img-fluid rounded" alt="Screenshot" style="max-height: 200px; width: 100%; object-fit: cover;">
           </div>
         {% endfor %}
       </div>
     </div>
   {% endif %}
   
   {# Add memories section #}
   {% if character.profile.memories %}
     <div class="memories-section mt-4">
       <h5>{% trans "Memories" %}</h5>
       <div class="row">
         {% for memory in character.profile.memories %}
           <div class="col-md-6 mb-3">
             <div class="card">
               <div class="card-body">
                 <h6>{{ memory.title }}</h6>
                 <p>{{ memory.description }}</p>
                 {% if memory.date %}
                   <small class="text-muted">{{ memory.date }}</small>
                 {% endif %}
               </div>
             </div>
           </div>
         {% endfor %}
       </div>
     </div>
   {% endif %}
   ```

9. **Update Character Profile Edit Template**

   ```django
   {# app/templates/characters/character_profile_edit.html #}
   {# Include screenshot and memory sections #}
   
   {% extends "base.html" %}
   {% load crispy_forms_tags %}
   
   {% block content %}
   <form method="post" enctype="multipart/form-data">
     {% csrf_token %}
     
     {{ form|crispy }}
     
     {% include 'characters/screenshot_upload.html' with profile=object %}
     {% include 'characters/memory_management.html' with profile=object %}
     
     <button type="submit" class="btn btn-primary">{% trans "Save Profile" %}</button>
   </form>
   
   <script src="{% static 'app/screenshot-manager.js' %}"></script>
   <script src="{% static 'app/memory-manager.js' %}"></script>
   {% endblock %}
   ```

#### Playwright Test

```typescript
// tests/e2e/characters/character-profile-screenshots-memories.spec.ts
import { test, expect } from '@playwright/test';

test.describe('Character Profile Screenshots and Memories', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/login');
    await page.fill('input[name="login"]', 'testuser');
    await page.fill('input[name="password"]', 'testpass123');
    await page.click('button[type="submit"]');
    await page.waitForURL('**/');
  });

  test('should upload screenshots', async ({ page }) => {
    // Navigate to character profile edit
    await page.goto('/characters/my-character/edit-profile/');
    
    // Upload screenshot file
    const fileInput = page.locator('input[type="file"][name="screenshots"]');
    await fileInput.setInputFiles({
      name: 'test-screenshot.png',
      mimeType: 'image/png',
      buffer: Buffer.from('fake-image-data')
    });
    
    // Submit form
    await page.click('button[type="submit"]');
    await page.waitForURL(/\//);
    
    // Verify screenshot appears on profile
    await page.goto('/characters/my-character/');
    await expect(page.locator('.screenshots-section img')).toBeVisible();
  });

  test('should delete screenshot', async ({ page }) => {
    await page.goto('/characters/my-character/edit-profile/');
    
    // Click delete button on first screenshot
    const deleteButton = page.locator('.delete-screenshot').first();
    if (await deleteButton.isVisible()) {
      await deleteButton.click();
      
      // Confirm deletion
      page.on('dialog', dialog => dialog.accept());
      
      // Submit form
      await page.click('button[type="submit"]');
      
      // Verify screenshot removed
      await expect(deleteButton).not.toBeVisible();
    }
  });

  test('should add memory', async ({ page }) => {
    await page.goto('/characters/my-character/edit-profile/');
    
    // Fill memory form
    await page.fill('#memory-title', 'Epic Win');
    await page.fill('#memory-description', 'We won the championship!');
    await page.fill('#memory-date', '2024-01-15');
    
    // Submit memory form
    await page.click('#add-memory-form button[type="submit"]');
    
    // Verify memory appears in list
    await expect(page.locator('.memory-item')).toContainText('Epic Win');
    
    // Submit main form
    await page.click('button[type="submit"]');
    await page.waitForURL(/\//);
    
    // Verify memory appears on profile
    await page.goto('/characters/my-character/');
    await expect(page.locator('.memories-section')).toContainText('Epic Win');
  });

  test('should delete memory', async ({ page }) => {
    await page.goto('/characters/my-character/edit-profile/');
    
    const deleteButton = page.locator('.delete-memory').first();
    if (await deleteButton.isVisible()) {
      const memoryCount = await page.locator('.memory-item').count();
      
      await deleteButton.click();
      
      // Verify memory removed from DOM
      await expect(page.locator('.memory-item')).toHaveCount(memoryCount - 1);
    }
  });
});
```

#### Acceptance Criteria

- [ ] Screenshots can be uploaded (multiple files)
- [ ] Existing screenshots display in edit form
- [ ] Screenshots can be deleted
- [ ] Screenshots display on character profile page
- [ ] Memories can be added (title, description, optional date)
- [ ] Existing memories display in edit form
- [ ] Memories can be edited and deleted
- [ ] Memories display on character profile page
- [ ] File upload validation (images only)
- [ ] Playwright tests pass

#### Files to Create/Modify

**Create:**
- `app/templates/characters/screenshot_upload.html`
- `app/templates/characters/memory_management.html`
- `app/static/app/screenshot-manager.js`
- `app/static/app/memory-manager.js`
- `tests/e2e/characters/character-profile-screenshots-memories.spec.ts`

**Modify:**
- `app/forms.py` - Update `CharacterProfileForm`
- `app/views.py` - Update `CharacterProfileEditView`
- `app/templates/characters/character_profile_edit.html` - Include new sections
- `app/templates/characters/character_detail_content.html` - Display screenshots/memories

---

### Task 4: Mobile Responsiveness Testing and Improvements

**Assignee**: Frontend Developer / QA Engineer  
**Story Points**: 8  
**Priority**: Medium  
**Dependencies**: Bootstrap 5 (already in use ✅)

#### Overview

Test and improve mobile responsiveness across all pages. Bootstrap 5 is used, but needs verification and fixes for mobile devices.

#### Implementation Steps

1. **Audit Current Mobile Responsiveness**

   Create checklist of all pages:
   - [ ] Login/Signup pages
   - [ ] Character list/detail pages
   - [ ] Message list/conversation pages
   - [ ] Friend request/list pages
   - [ ] User profile pages
   - [ ] Game list/detail pages
   - [ ] Navigation bar
   - [ ] Forms

2. **Test on Multiple Devices (Browser DevTools)**

   Test viewports:
   - iPhone SE (375x667)
   - iPhone 12 Pro (390x844)
   - iPad (768x1024)
   - Android (412x915)

3. **Identify Issues**

   Common mobile issues to check:
   - Text too small
   - Buttons too small/tight
   - Forms overflow
   - Tables not scrollable
   - Images too large
   - Navigation not mobile-friendly
   - Modals/dialogs don't fit

4. **Fix Navigation Bar for Mobile**

   ```django
   {# app/templates/base_navbar.html #}
   {# Ensure Bootstrap 5 navbar is mobile-responsive #}
   
   <nav class="navbar navbar-expand-lg navbar-dark bg-primary">
     <div class="container-fluid">
       <a class="navbar-brand" href="/">Game Player Nick Finder</a>
       
       <!-- Mobile toggle button -->
       <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
         <span class="navbar-toggler-icon"></span>
       </button>
       
       <!-- Collapsible menu -->
       <div class="collapse navbar-collapse" id="navbarNav">
         <ul class="navbar-nav ms-auto">
           <!-- ... menu items ... -->
         </ul>
       </div>
     </div>
   </nav>
   ```

5. **Fix Forms for Mobile**

   Ensure all forms use Bootstrap responsive classes:
   ```django
   <form class="container">
     <div class="row">
       <div class="col-12 col-md-6">
         {# Form fields #}
       </div>
     </div>
   </form>
   ```

6. **Fix Tables for Mobile (Make Scrollable)**

   ```django
   <div class="table-responsive">
     <table class="table table-striped">
       {# Table content #}
     </table>
   </div>
   ```

7. **Fix Images for Mobile**

   Ensure all images are responsive:
   ```django
   <img src="..." class="img-fluid" alt="...">
   ```

8. **Add Touch-Friendly Button Sizes**

   Ensure minimum touch target size (44x44px):
   ```css
   /* app/static/app/style.css */
   .btn {
     min-height: 44px;
     min-width: 44px;
   }
   
   .btn-sm {
     min-height: 36px;
   }
   ```

9. **Test Conversation List on Mobile**

   Ensure conversation list is collapsible on mobile (already planned in Task 2).

10. **Create Mobile-Specific CSS Overrides**

    ```css
    /* app/static/app/mobile.css */
    
    @media (max-width: 768px) {
      /* Adjust font sizes */
      body {
        font-size: 16px; /* Prevent zoom on iOS */
      }
      
      /* Ensure inputs are large enough */
      input, textarea, select {
        font-size: 16px;
      }
      
      /* Adjust spacing */
      .container {
        padding-left: 15px;
        padding-right: 15px;
      }
      
      /* Make cards stack better */
      .card {
        margin-bottom: 1rem;
      }
    }
    ```

#### Playwright Test for Mobile

```typescript
// tests/e2e/mobile/mobile-responsiveness.spec.ts
import { test, expect } from '@playwright/test';

test.describe('Mobile Responsiveness', () => {
  // Test iPhone viewport
  test.use({ viewport: { width: 375, height: 667 } });

  test.beforeEach(async ({ page }) => {
    await page.goto('/login');
    await page.fill('input[name="login"]', 'testuser');
    await page.fill('input[name="password"]', 'testpass123');
    await page.click('button[type="submit"]');
    await page.waitForURL('**/');
  });

  test('navigation should be mobile-friendly', async ({ page }) => {
    await page.goto('/');
    
    // Verify hamburger menu exists
    const toggleButton = page.locator('.navbar-toggler');
    await expect(toggleButton).toBeVisible();
    
    // Click to open menu
    await toggleButton.click();
    
    // Verify menu items are visible
    await expect(page.locator('.navbar-nav')).toBeVisible();
  });

  test('forms should be readable on mobile', async ({ page }) => {
    await page.goto('/characters/add/');
    
    // Verify inputs are visible and usable
    const inputs = page.locator('input, textarea, select');
    const count = await inputs.count();
    
    for (let i = 0; i < count; i++) {
      const input = inputs.nth(i);
      await expect(input).toBeVisible();
      
      // Verify minimum size (touch-friendly)
      const box = await input.boundingBox();
      if (box) {
        expect(box.height).toBeGreaterThanOrEqual(36);
      }
    }
  });

  test('images should be responsive', async ({ page }) => {
    await page.goto('/characters/my-character/');
    
    const images = page.locator('img');
    const count = await images.count();
    
    for (let i = 0; i < count; i++) {
      const img = images.nth(i);
      const classes = await img.getAttribute('class');
      
      // Images should have img-fluid class or inline responsive styles
      if (classes) {
        expect(classes).toContain('img-fluid');
      }
    }
  });

  test('tables should be scrollable on mobile', async ({ page }) => {
    // Navigate to page with table
    await page.goto('/games/');
    
    const tables = page.locator('table');
    if (await tables.count() > 0) {
      const table = tables.first();
      const parent = table.locator('..');
      
      // Table should be in table-responsive container
      const parentClass = await parent.getAttribute('class');
      expect(parentClass).toContain('table-responsive');
    }
  });
});
```

#### Acceptance Criteria

- [ ] All pages tested on mobile viewports (iPhone, iPad, Android)
- [ ] Navigation bar works on mobile (hamburger menu)
- [ ] All forms are readable and usable on mobile
- [ ] Images are responsive
- [ ] Tables are scrollable
- [ ] Touch targets are minimum 44x44px
- [ ] Text is readable (minimum 16px to prevent zoom)
- [ ] No horizontal scrolling on any page
- [ ] Playwright mobile tests pass

#### Files to Create/Modify

**Create:**
- `app/static/app/mobile.css`
- `tests/e2e/mobile/mobile-responsiveness.spec.ts`

**Modify:**
- `app/templates/base_navbar.html` - Ensure mobile menu works
- `app/templates/base.html` - Include mobile.css
- All form templates - Ensure responsive classes
- All table templates - Wrap in table-responsive
- All image tags - Add img-fluid class

---

## Low Priority Tasks (Future Enhancements)

### Task 5: Real-time Messaging

**Priority**: Low  
**Status**: Future Enhancement  
**Story Points**: 21

#### Overview

Implement WebSocket or Server-Sent Events for real-time message delivery. Currently messages require page refresh.

#### Implementation Approach

**Option 1: Server-Sent Events (Simpler)**
- Use Django's streaming response
- Client uses EventSource API
- Easier to implement, one-way communication

**Option 2: WebSocket (More Complex)**
- Use Django Channels or similar
- Bidirectional communication
- More setup required

**Recommendation**: Start with Server-Sent Events for MVP, upgrade to WebSocket later if needed.

#### Note

This is a larger task and should be planned separately. Detailed implementation will be created when this becomes a priority.

---

### Task 6: Additional UX Features

**Priority**: Low  
**Status**: Future Enhancement

Features from `docs/features/additional-ux-features.md`:
- Quick Actions & Shortcuts
- Notification Center
- Enhanced Search & Discovery
- Activity Feed

These should be planned as separate epics when ready.

---

## Implementation Order

1. **Week 1**: Task 1 (Playwright Tests Verification) + Task 2 (Conversation UI) - Start
2. **Week 2**: Task 2 (Conversation UI) - Complete + Task 3 (Screenshots/Memories) - Start
3. **Week 3**: Task 3 (Screenshots/Memories) - Complete + Task 4 (Mobile) - Start
4. **Week 4**: Task 4 (Mobile) - Complete + Polish

---

## Testing Checklist

Before considering any task complete:

- [ ] Playwright tests written
- [ ] Playwright tests pass
- [ ] Manual testing completed
- [ ] Code reviewed
- [ ] No console errors
- [ ] Mobile tested (for UI tasks)
- [ ] Documentation updated

---

**Document Version**: 1.0  
**Last Updated**: 2024  
**Maintained By**: Software Engineer, Development Team


# Implementation Guide for Mid-Level Developers

**Status**: ✅ Ready for use  
**Last Updated**: 2024-12-19  
**Audience**: Mid-level Developers, Tech Leads

## Document Purpose

This guide provides step-by-step instructions for mid-level developers to implement pending features in the Game Player Nick Finder application. It focuses on practical implementation steps, code examples, and best practices.

## Prerequisites

Before starting implementation:

1. **Read Project Status**:
   - [Project Status Summary](../PROJECT_STATUS_SUMMARY.md) - Understand what's done and what's pending
   - [Status Report](../STATUS_REPORT.md) - Check current implementation status

2. **Understand the Stack**:
   - Django 5.1.4 + Django REST Framework
   - Django Templates + Bootstrap 5
   - SQLite (dev) / PostgreSQL (prod)
   - Playwright for E2E testing

3. **Setup Development Environment**:
   ```bash
   # Install dependencies
   pipenv install
   pipenv shell
   
   # Load fixtures (required for tests)
   pnpm load:fixtures  # or .\load_fixtures.ps1 (Windows) / ./load_fixtures.sh (Unix)
   
   # Run migrations
   python manage.py migrate
   ```

## Implementation Workflow

### 1. Always Follow TDD (Test-Driven Development)

**CRITICAL**: Write Playwright tests FIRST, then implement the feature.

```bash
# Step 1: Write test (red phase)
# Create test file: tests/e2e/feature-name.spec.ts
# Test should fail initially

# Step 2: Implement feature (green phase)
# Make the test pass

# Step 3: Refactor
# Improve code while keeping tests green

# Step 4: Run all tests
pnpm test:e2e
```

### 2. Check Current Status Before Starting

**ALWAYS** check if feature is already implemented:
1. Read [Project Status Summary](../PROJECT_STATUS_SUMMARY.md)
2. Check [Status Report](../STATUS_REPORT.md)
3. Review [Detailed Tasks](../scrum/detailed-tasks.md) for implementation steps

### 3. Use Existing Patterns

Follow existing code patterns in the project:
- **Models**: See `app/models.py` for model structure
- **Views**: See `app/views.py` for view patterns
- **Forms**: See `app/forms.py` for form patterns
- **Templates**: See `app/templates/` for template structure
- **API**: See `app/api_views.py` for API patterns

## Priority Tasks Implementation

### Task 1: Playwright Tests Verification (High Priority)

**Status**: Tests written, need verification  
**Story Points**: 8  
**Estimated Time**: 1-2 days

#### Steps

1. **Load Fixtures** (REQUIRED):
   ```bash
   # Windows
   .\load_fixtures.ps1
   
   # Unix/MacOS
   ./load_fixtures.sh
   
   # Or cross-platform
   pnpm load:fixtures
   ```

2. **Run All Tests**:
   ```bash
   pnpm test:e2e
   ```

3. **Identify Failing Tests**:
   - Document all failures
   - Categorize: selector issues, authentication, timing, missing features

4. **Fix Test Issues**:
   - **Selector Problems**: Check actual HTML, update selectors
   - **Authentication**: Verify test users exist in fixtures
   - **Timing**: Add explicit waits (`await page.waitForSelector(...)`)
   - **Missing Features**: Implement feature first, then fix test

5. **Verify All Tests Pass**:
   ```bash
   # Run 3 times to check for flaky tests
   pnpm test:e2e
   pnpm test:e2e
   pnpm test:e2e
   ```

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

- [ ] All 7 test files pass
- [ ] No flaky tests (run 3 times, all pass)
- [ ] Tests run in headless mode
- [ ] Test coverage report generated

**Documentation**: See [005-pending-tasks-implementation.md](../scrum/005-pending-tasks-implementation.md#task-1-playwright-tests-verification-and-fixes)

---

### Task 2: Conversation Management UI (High Priority)

**Status**: Backend ready (thread_id exists), UI missing  
**Story Points**: 13  
**Estimated Time**: 1 week

#### Overview

Implement a conversation list UI that allows users to:
- See all conversations grouped by thread_id
- Switch between conversations easily
- See unread message indicators
- See last message preview and timestamp

#### Implementation Steps

1. **Update MessageListView** (`app/views.py`):
   ```python
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
           thread_messages = Message.objects.filter(thread_id=thread_id).order_by('-sent_date')
           
           if thread_messages.exists():
               latest_message = thread_messages.first()
               
               # Determine other character
               if latest_message.sender_character in user_characters:
                   other_character = latest_message.receiver_character
               else:
                   other_character = latest_message.sender_character
               
               # Count unread messages
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
                   'message_preview': latest_message.content[:100],
               })
       
       # Sort by latest message date
       conversations.sort(key=lambda x: x['latest_message'].sent_date, reverse=True)
       
       context['conversations'] = conversations
       context['current_thread_id'] = self.request.GET.get('thread_id')
       
       return context
   ```

2. **Create Conversation List Template** (`app/templates/messages/conversation_list.html`):
   ```django
   {% load i18n %}
   
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

3. **Update Message List Template** (`app/templates/messages/message_list.html`):
   ```django
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

4. **Mark Messages as Read** (in `MessageListView.get()`):
   ```python
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

5. **Write Playwright Test** (`tests/e2e/messaging/conversation-list.spec.ts`):
   ```typescript
   import { test, expect } from '@playwright/test';
   
   test.describe('Conversation List', () => {
     test.beforeEach(async ({ page }) => {
       await page.goto('/login');
       await page.fill('input[name="login"]', 'testuser');
       await page.fill('input[name="password"]', 'testpass123');
       await page.click('button[type="submit"]');
       await page.waitForURL('**/');
     });
   
     test('should display conversation list', async ({ page }) => {
       await page.goto('/messages/');
       await expect(page.locator('.conversation-list')).toBeVisible();
     });
   
     test('should switch between conversations', async ({ page }) => {
       await page.goto('/messages/');
       const firstConversation = page.locator('.list-group-item').first();
       await firstConversation.click();
       await page.waitForURL(/\?thread_id=.*/);
       await expect(page.locator('.message-bubble, .message-item')).toBeVisible({ timeout: 5000 });
     });
   });
   ```

#### Acceptance Criteria

- [ ] Conversation list displays all user's conversations
- [ ] Each conversation shows avatar, nickname, unread count
- [ ] Last message preview shows (first 100 chars)
- [ ] Timestamp shows relative time
- [ ] Clicking conversation switches to that thread
- [ ] Active conversation is highlighted
- [ ] Messages marked as read when viewing thread
- [ ] Mobile-responsive (collapsible sidebar)
- [ ] Playwright tests pass

**Documentation**: See [005-pending-tasks-implementation.md](../scrum/005-pending-tasks-implementation.md#task-2-conversation-management-ui)

---

### Task 3: Character Profile Screenshots & Memories UI (Medium Priority)

**Status**: Backend ready (JSONField), UI missing  
**Story Points**: 13  
**Estimated Time**: 1 week

#### Overview

Implement UI for uploading screenshots and managing memories for character profiles.

#### Implementation Steps

1. **Update CharacterProfileForm** (`app/forms.py`):
   ```python
   class CharacterProfileForm(forms.ModelForm):
       screenshots = forms.FileField(
           required=False,
           widget=forms.ClearableFileInput(attrs={'multiple': True}),
           help_text="Upload multiple screenshots (images only)"
       )
       
       class Meta:
           model = CharacterProfile
           fields = ['custom_bio', 'is_public', 'screenshots']
       
       def save(self, commit=True):
           profile = super().save(commit=False)
           
           if commit:
               profile.save()
               
               # Handle screenshot uploads
               screenshots = self.cleaned_data.get('screenshots')
               if screenshots:
                   uploaded_files = self.files.getlist('screenshots')
                   screenshot_urls = list(profile.screenshots) if profile.screenshots else []
                   
                   for uploaded_file in uploaded_files:
                       from django.core.files.storage import default_storage
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

2. **Create Screenshot Upload Template** (`app/templates/characters/screenshot_upload.html`):
   ```django
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

3. **Create Memory Management Template** (`app/templates/characters/memory_management.html`):
   ```django
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

4. **Add JavaScript for Memory Management** (`app/static/app/memory-manager.js`):
   ```javascript
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
       // Add to DOM and clear form
       this.reset();
     });
     
     updateMemoriesJson();
   });
   ```

5. **Update Character Profile Edit View** (`app/views.py`):
   ```python
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
       
       # Handle memories JSON
       memories_json = self.request.POST.get('memories_json')
       if memories_json:
           import json
           try:
               profile.memories = json.loads(memories_json)
           except json.JSONDecodeError:
               pass
       
       profile.save()
       return redirect('character_detail', ...)
   ```

6. **Write Playwright Test** (`tests/e2e/characters/character-profile-screenshots-memories.spec.ts`):
   ```typescript
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
       await page.goto('/characters/my-character/edit-profile/');
       const fileInput = page.locator('input[type="file"][name="screenshots"]');
       await fileInput.setInputFiles({
         name: 'test-screenshot.png',
         mimeType: 'image/png',
         buffer: Buffer.from('fake-image-data')
       });
       await page.click('button[type="submit"]');
       await page.waitForURL(/\//);
       await page.goto('/characters/my-character/');
       await expect(page.locator('.screenshots-section img')).toBeVisible();
     });
   
     test('should add memory', async ({ page }) => {
       await page.goto('/characters/my-character/edit-profile/');
       await page.fill('#memory-title', 'Epic Win');
       await page.fill('#memory-description', 'We won the championship!');
       await page.fill('#memory-date', '2024-01-15');
       await page.click('#add-memory-form button[type="submit"]');
       await expect(page.locator('.memory-item')).toContainText('Epic Win');
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
- [ ] Memories can be deleted
- [ ] Memories display on character profile page
- [ ] Playwright tests pass

**Documentation**: See [005-pending-tasks-implementation.md](../scrum/005-pending-tasks-implementation.md#task-3-character-profile-screenshots--memories-ui)

---

## Common Patterns and Best Practices

### Django Models

```python
# Always use UUIDs for primary keys
class MyModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Use proper field types
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'created_at']),
        ]
```

### Django Views

```python
# Use class-based views for complex logic
class MyListView(ListView):
    model = MyModel
    template_name = 'my_template.html'
    context_object_name = 'objects'
    
    def get_queryset(self):
        return MyModel.objects.filter(user=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['extra_data'] = self.get_extra_data()
        return context
```

### Django Forms

```python
# Use ModelForm when possible
class MyForm(forms.ModelForm):
    class Meta:
        model = MyModel
        fields = ['field1', 'field2']
        widgets = {
            'field1': forms.TextInput(attrs={'class': 'form-control'}),
        }
    
    def clean_field1(self):
        # Add validation
        value = self.cleaned_data['field1']
        if not value:
            raise forms.ValidationError("Field is required")
        return value
```

### Playwright Tests

```typescript
// Always use proper selectors
test('should do something', async ({ page }) => {
  // Wait for navigation
  await page.goto('/url');
  await page.waitForURL('**/expected-url');
  
  // Wait for elements
  await page.waitForSelector('.element-class');
  
  // Use data-testid when possible
  await page.click('[data-testid="my-button"]');
  
  // Verify results
  await expect(page.locator('.result')).toBeVisible();
});
```

## Testing Checklist

Before considering any task complete:

- [ ] Playwright tests written
- [ ] Playwright tests pass (run 3 times)
- [ ] Manual testing completed
- [ ] Code reviewed
- [ ] No console errors
- [ ] Mobile tested (for UI tasks)
- [ ] Documentation updated
- [ ] Status documents updated

## Getting Help

If you're stuck:

1. **Check Documentation**:
   - [Project Status Summary](../PROJECT_STATUS_SUMMARY.md)
   - [Detailed Tasks](../scrum/detailed-tasks.md)
   - [005-pending-tasks-implementation.md](../scrum/005-pending-tasks-implementation.md)

2. **Review Existing Code**:
   - Look at similar features already implemented
   - Follow existing patterns

3. **Ask Questions**:
   - Check if feature is already implemented
   - Review test files for examples
   - Check Django documentation

## POKE System Implementation

**Status**: 📋 Ready for Implementation  
**Story Points**: 13  
**Priority**: High

### Overview

The POKE system is a lightweight, spam-protected initial contact mechanism that unlocks full messaging after mutual acknowledgment. See detailed documentation:

- **[POKE System Architecture](./poke-system-architecture.md)** - Complete technical architecture
- **[POKE Feature Specification](../features/poke-system-specification.md)** - Detailed feature spec

### Quick Implementation Steps

1. **Read Documentation First**:
   - Review [POKE System Architecture](./poke-system-architecture.md) for model design and business logic
   - Review [POKE Feature Specification](../features/poke-system-specification.md) for functional requirements

2. **Phase 1: Models & Migrations** (2-3 hours):
   ```bash
   # Create models: Poke, PokeBlock
   # See architecture doc for model specifications
   python manage.py makemigrations
   python manage.py migrate
   ```

3. **Phase 2: Business Logic** (4-6 hours):
   - Content filtering (URL/link detection, character limits)
   - Rate limiting logic
   - Status management (PENDING, RESPONDED, IGNORED, BLOCKED)
   - Mutual POKE detection
   - Message unlock logic

4. **Phase 3: API/Views** (4-6 hours):
   - API endpoints (send, list, respond, ignore, block)
   - View classes (ListView, DetailView, FormView)
   - Forms with validation

5. **Phase 4: UI Templates** (4-6 hours):
   - POKE list template
   - Send POKE form/modal
   - POKE detail view
   - Status indicators

6. **Phase 5: Integration** (2-3 hours):
   - Update Message system to check POKE status
   - Hide "Send Message" if not unlocked
   - Show "Send POKE" instead
   - Notifications

7. **Phase 6: Testing** (6-8 hours):
   - Unit tests (models, business logic)
   - Integration tests (API, workflows)
   - Playwright E2E tests (all user flows)

**Total Estimated Time**: 22-32 hours (3-4 days for mid-level developer)

### Key Implementation Notes

- **Always validate content server-side** (never trust client)
- **Use existing Character model** (no changes needed)
- **Integrate with existing Message system** (check unlock status)
- **Follow existing patterns** (see Message views/forms for reference)
- **Write Playwright tests FIRST** (TDD approach)

### Testing Checklist

- [ ] Unit tests for content filtering
- [ ] Unit tests for rate limiting
- [ ] Unit tests for status transitions
- [ ] API endpoint tests
- [ ] Playwright: Send POKE flow
- [ ] Playwright: Receive and respond flow
- [ ] Playwright: Ignore flow
- [ ] Playwright: Block flow
- [ ] Playwright: Message unlocking flow

## Next Steps

After completing a task:

1. Update [Status Report](../STATUS_REPORT.md) with completion status
2. Update [Project Status Summary](../PROJECT_STATUS_SUMMARY.md)
3. Create PR with:
   - Implementation code
   - Playwright tests
   - Documentation updates
   - Status updates

---

**Document Version**: 1.0  
**Last Updated**: 2024-12-19  
**Maintained By**: Tech Lead, Development Team


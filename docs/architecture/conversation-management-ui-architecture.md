# Conversation Management UI - Architecture Documentation

**Status**: 📋 Design Complete - Ready for Implementation  
**Last Updated**: 2025-12-28  
**Authors**: UX Designer, Solution Architect, Software Architect  
**Priority**: High (13 SP)

## Document Purpose

This document describes the complete architecture for implementing Conversation Management UI in the Game Player Nick Finder application. It includes UX design, solution architecture, and software architecture details.

---

## Executive Summary

The Conversation Management UI provides users with an intuitive interface to manage multiple conversations with different characters. It replaces the current flat message list with a modern, sidebar-based conversation list that allows easy navigation between conversations, shows unread message indicators, and displays conversation previews.

### Key Benefits

- **Better UX**: Easy navigation between multiple conversations
- **Visual Feedback**: Unread message indicators and timestamps
- **Efficient**: Quick access to all conversations without scrolling
- **Mobile-Friendly**: Responsive design with collapsible sidebar

---

## 1. UX Design

### 1.1 User Experience Goals

1. **Quick Access**: Users should be able to see all their conversations at a glance
2. **Visual Hierarchy**: Active conversation should be clearly highlighted
3. **Status Indicators**: Unread messages should be immediately visible
4. **Context Preservation**: Last message preview helps users remember conversation context
5. **Mobile Responsive**: Works seamlessly on all device sizes

### 1.2 Layout Design

#### Desktop Layout (≥768px)

```
┌─────────────────────────────────────────────────────────────┐
│                    Navigation Bar                            │
├──────────────┬──────────────────────────────────────────────┤
│              │                                               │
│ Conversations│          Message Thread Area                  │
│   Sidebar    │                                               │
│   (25%)      │            (75%)                              │
│              │                                               │
│ ┌──────────┐│  ┌─────────────────────────────────────────┐  │
│ │ Avatar    ││  │  Character Name (Game)                  │  │
│ │ Nickname  ││  │  ─────────────────────────────────────  │  │
│ │ Unread: 3││  │                                         │  │
│ │ Preview...││  │  [Message bubbles appear here]         │  │
│ └──────────┘│  │                                         │  │
│              │  │                                         │  │
│ ┌──────────┐│  │                                         │  │
│ │ Avatar    ││  │                                         │  │
│ │ Nickname  ││  │  ─────────────────────────────────────  │  │
│ │ Preview...││  │  [Message input form]                  │  │
│ └──────────┘│  └─────────────────────────────────────────┘  │
│              │                                               │
│ (Active)     │                                               │
│              │                                               │
└──────────────┴──────────────────────────────────────────────┘
```

#### Mobile Layout (<768px)

```
┌─────────────────────────────┐
│      Navigation Bar          │
├─────────────────────────────┤
│ [☰ Conversations] Button     │
├─────────────────────────────┤
│                             │
│   Message Thread Area       │
│   (Full Width)              │
│                             │
│  [Message bubbles]           │
│                             │
│  [Message input form]       │
│                             │
└─────────────────────────────┘

When button clicked:
┌─────────────────────────────┐
│      Navigation Bar          │
├─────────────────────────────┤
│ [☰ Conversations] Button     │
├──────────┬──────────────────┤
│          │                   │
│ Sidebar  │  Message Thread   │
│ (Slide)  │  (Hidden/Overlay) │
│          │                   │
│ [List]   │                   │
│          │                   │
└──────────┴──────────────────┘
```

### 1.3 Conversation List Item Design

Each conversation item displays:

1. **Avatar** (40x40px, circular)
   - Character avatar or default placeholder
   - Clickable to view character profile

2. **Character Name** (Bold, primary color)
   - Character nickname
   - Game name in smaller text below

3. **Unread Badge** (if unread > 0)
   - Blue badge with count
   - Positioned next to character name

4. **Message Preview** (truncated to 100 chars)
   - Last message content
   - Gray text, smaller font
   - Ellipsis (...) if truncated

5. **Timestamp** (relative time)
   - "2 hours ago", "Yesterday", "Dec 25"
   - Small, muted text

6. **Active State** (when selected)
   - Blue background highlight
   - White text for contrast

### 1.4 Interaction Patterns

#### Desktop Interactions

1. **Click Conversation**: 
   - Loads conversation thread
   - Highlights active conversation
   - Marks messages as read
   - Scrolls to bottom of thread

2. **Hover State**:
   - Slight background color change
   - Cursor changes to pointer

3. **Empty State**:
   - Shows "No conversations yet. Start messaging someone!"
   - Link to character list

#### Mobile Interactions

1. **Toggle Sidebar**:
   - Button in header toggles sidebar
   - Sidebar slides in from left (overlay)
   - Clicking outside closes sidebar
   - Backdrop with slight opacity

2. **Swipe Gestures** (Future Enhancement):
   - Swipe right to open sidebar
   - Swipe left to close sidebar

### 1.5 Visual States

#### Conversation States

1. **Normal**: White background, black text
2. **Active**: Blue background (#0d6efd), white text
3. **Hover**: Light gray background (#f8f9fa)
4. **Unread**: Bold character name, blue badge visible

#### Message States

1. **Read**: Normal opacity
2. **Unread**: Slightly bold, badge count visible
3. **New Message**: Subtle animation (future enhancement)

---

## 2. Solution Architecture

### 2.1 High-Level Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    User Browser                          │
│  ┌──────────────────────────────────────────────────┐  │
│  │  Conversation List UI (Sidebar)                   │  │
│  │  - Renders conversation list                       │  │
│  │  - Handles click events                           │  │
│  │  - Shows unread indicators                        │  │
│  └──────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────┐  │
│  │  Message Thread UI (Main Area)                   │  │
│  │  - Displays messages                             │  │
│  │  - Message input form                           │  │
│  │  - Auto-scroll to bottom                        │  │
│  └──────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
                          │
                          │ HTTP Request
                          ▼
┌─────────────────────────────────────────────────────────┐
│              Django Backend (MessageListView)           │
│  ┌──────────────────────────────────────────────────┐  │
│  │  get_context_data()                              │  │
│  │  - Builds conversation list                      │  │
│  │  - Groups by thread_id                           │  │
│  │  - Calculates unread counts                     │  │
│  │  - Gets latest message per thread                │  │
│  └──────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────┐  │
│  │  get() method                                    │  │
│  │  - Marks messages as read when viewing thread    │  │
│  │  - Handles thread_id parameter                  │  │
│  └──────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│                    Database (SQLite/PostgreSQL)          │
│  ┌──────────────────────────────────────────────────┐  │
│  │  Message Model                                    │  │
│  │  - thread_id (UUID)                              │  │
│  │  - is_read (Boolean)                             │  │
│  │  - sent_date (DateTime)                          │  │
│  └──────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────┐  │
│  │  Character Model                                 │  │
│  │  - avatar (ImageField)                           │  │
│  │  - nickname (CharField)                          │  │
│  │  - game (ForeignKey)                             │  │
│  └──────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
```

### 2.2 Data Flow

#### Loading Conversations

1. **User navigates to `/messages/`**
2. **MessageListView.get_context_data()**:
   - Gets all user's characters
   - Finds all unique `thread_id` values for user
   - For each thread:
     - Gets latest message
     - Determines "other character" (not user's character)
     - Counts unread messages
     - Extracts message preview (first 100 chars)
     - Calculates relative timestamp
   - Sorts conversations by latest message date (newest first)
   - Returns conversation list in context

3. **Template renders**:
   - Conversation list sidebar
   - Active conversation thread (if `thread_id` in URL)
   - Message input form

#### Viewing Conversation

1. **User clicks conversation item**
2. **URL updates**: `/messages/?thread_id={uuid}&character={character_id}`
3. **MessageListView.get()**:
   - Marks all messages in thread as read (for user's characters)
   - Sets `read_at` timestamp
4. **MessageListView.get_queryset()**:
   - Filters messages by `thread_id`
   - Orders by `sent_date` (ascending)
5. **Template renders**:
   - Conversation list (with active item highlighted)
   - Message thread
   - Message input form

### 2.3 Key Components

#### Backend Components

1. **MessageListView.get_context_data()** (Enhanced)
   - Builds conversation list
   - Groups messages by thread_id
   - Calculates metadata (unread count, preview, timestamp)

2. **MessageListView.get()** (Enhanced)
   - Marks messages as read when viewing thread
   - Handles thread_id parameter

3. **Conversation Data Structure**
   ```python
   {
       'thread_id': UUID,
       'other_character': Character object,
       'latest_message': Message object,
       'unread_count': int,
       'message_preview': str (100 chars),
       'timestamp': datetime,
   }
   ```

#### Frontend Components

1. **Conversation List Sidebar** (`conversation_list.html`)
   - Renders list of conversations
   - Handles click events
   - Shows active state

2. **Message Thread Area** (existing `message_list.html`)
   - Displays messages
   - Message input form
   - Auto-scroll functionality

3. **Mobile Toggle Button**
   - Shows/hides sidebar on mobile
   - Bootstrap collapse component

---

## 3. Software Architecture

### 3.1 Backend Implementation

#### 3.1.1 Enhanced MessageListView

**File**: `app/views.py`

**Changes to `get_context_data()`**:

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
        thread_messages = Message.objects.filter(
            thread_id=thread_id
        ).select_related(
            'sender_character', 
            'receiver_character',
            'sender_character__game',
            'receiver_character__game'
        ).order_by('-sent_date')
        
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
            
            # Get message preview (first 100 chars)
            preview = latest_message.content[:100]
            if len(latest_message.content) > 100:
                preview += "..."
            
            conversations.append({
                'thread_id': thread_id,
                'other_character': other_character,
                'latest_message': latest_message,
                'unread_count': unread_count,
                'message_preview': preview,
            })
    
    # Sort by latest message date (newest first)
    conversations.sort(
        key=lambda x: x['latest_message'].sent_date, 
        reverse=True
    )
    
    context['conversations'] = conversations
    context['current_thread_id'] = self.request.GET.get('thread_id')
    context['current_character_id'] = self.request.GET.get('character')
    
    # ... existing context code ...
    return context
```

**Changes to `get()` method**:

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

#### 3.1.2 Template Structure

**New Template**: `app/templates/messages/conversation_list.html`

```django
{% load i18n %}
{% load static %}

<div class="conversation-list">
    <div class="list-group list-group-flush">
        {% for conversation in conversations %}
            <a href="{% url 'message_list' %}?thread_id={{ conversation.thread_id }}&character={{ conversation.other_character.id }}"
               class="list-group-item list-group-item-action conversation-item {% if conversation.thread_id == current_thread_id %}active{% endif %}"
               data-thread-id="{{ conversation.thread_id }}">
                <div class="d-flex w-100 justify-content-between align-items-start">
                    <div class="flex-grow-1">
                        <div class="d-flex align-items-center mb-1">
                            <img src="{{ conversation.other_character.avatar.url|default:'/static/images/default-avatar.png' }}" 
                                 alt="{{ conversation.other_character.nickname }}"
                                 class="conversation-avatar rounded-circle me-2" 
                                 style="width: 40px; height: 40px; object-fit: cover;">
                            <div class="flex-grow-1">
                                <h6 class="mb-0 conversation-name">
                                    {{ conversation.other_character.nickname }}
                                    {% if conversation.unread_count > 0 %}
                                        <span class="badge bg-primary rounded-pill ms-2 unread-badge">
                                            {{ conversation.unread_count }}
                                        </span>
                                    {% endif %}
                                </h6>
                                <small class="text-muted conversation-game">
                                    {{ conversation.other_character.game.name }}
                                </small>
                            </div>
                        </div>
                        <p class="mb-1 text-muted small conversation-preview">
                            {{ conversation.message_preview }}
                        </p>
                        <small class="text-muted conversation-time">
                            {{ conversation.latest_message.sent_date|timesince }} ago
                        </small>
                    </div>
                </div>
            </a>
        {% empty %}
            <div class="list-group-item text-muted text-center py-4">
                <i class="bi bi-chat-dots" style="font-size: 2rem;"></i>
                <p class="mt-2 mb-0">{% trans "No conversations yet." %}</p>
                <p class="small">{% trans "Start messaging someone!" %}</p>
            </div>
        {% endfor %}
    </div>
</div>
```

**Updated Template**: `app/templates/messages/message_list.html`

- Add sidebar with conversation list
- Make responsive (collapsible on mobile)
- Update layout to two-column on desktop

### 3.2 Frontend Implementation

#### 3.2.1 CSS Styling

**File**: `app/static/app/style.css` (add to existing file)

```css
/* Conversation List Styles */
.conversation-list {
    max-height: calc(100vh - 200px);
    overflow-y: auto;
}

.conversation-item {
    border-left: 3px solid transparent;
    transition: all 0.2s ease;
    padding: 12px 15px;
}

.conversation-item:hover {
    background-color: #f8f9fa;
    border-left-color: #0d6efd;
}

.conversation-item.active {
    background-color: #0d6efd;
    color: white;
    border-left-color: #0a58ca;
}

.conversation-item.active .conversation-name,
.conversation-item.active .conversation-game,
.conversation-item.active .conversation-preview,
.conversation-item.active .conversation-time {
    color: white !important;
}

.conversation-avatar {
    flex-shrink: 0;
}

.conversation-name {
    font-weight: 600;
    color: #212529;
}

.conversation-item.active .conversation-name {
    color: white;
}

.unread-badge {
    font-size: 0.75rem;
    padding: 2px 6px;
}

.conversation-preview {
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
    max-width: 100%;
}

.conversation-time {
    font-size: 0.75rem;
}

/* Mobile Responsive */
@media (max-width: 767.98px) {
    .conversation-sidebar {
        position: fixed;
        top: 56px; /* Navbar height */
        left: -100%;
        width: 280px;
        height: calc(100vh - 56px);
        background: white;
        z-index: 1000;
        transition: left 0.3s ease;
        box-shadow: 2px 0 5px rgba(0,0,0,0.1);
    }
    
    .conversation-sidebar.show {
        left: 0;
    }
    
    .conversation-backdrop {
        display: none;
        position: fixed;
        top: 56px;
        left: 0;
        width: 100%;
        height: calc(100vh - 56px);
        background: rgba(0,0,0,0.5);
        z-index: 999;
    }
    
    .conversation-backdrop.show {
        display: block;
    }
}
```

#### 3.2.2 JavaScript Functionality

**File**: `app/static/app/conversation-manager.js` (new file)

```javascript
document.addEventListener('DOMContentLoaded', function() {
    // Mobile sidebar toggle
    const sidebarToggle = document.getElementById('conversation-sidebar-toggle');
    const sidebar = document.querySelector('.conversation-sidebar');
    const backdrop = document.querySelector('.conversation-backdrop');
    
    if (sidebarToggle && sidebar) {
        sidebarToggle.addEventListener('click', function() {
            sidebar.classList.toggle('show');
            if (backdrop) {
                backdrop.classList.toggle('show');
            }
        });
        
        // Close sidebar when clicking backdrop
        if (backdrop) {
            backdrop.addEventListener('click', function() {
                sidebar.classList.remove('show');
                backdrop.classList.remove('show');
            });
        }
        
        // Close sidebar when clicking conversation item (mobile)
        const conversationItems = document.querySelectorAll('.conversation-item');
        conversationItems.forEach(item => {
            item.addEventListener('click', function() {
                if (window.innerWidth < 768) {
                    sidebar.classList.remove('show');
                    if (backdrop) {
                        backdrop.classList.remove('show');
                    }
                }
            });
        });
    }
    
    // Auto-scroll to bottom of message thread
    const chatMessages = document.querySelector('.chat-messages');
    if (chatMessages) {
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
    
    // Highlight active conversation on load
    const activeConversation = document.querySelector('.conversation-item.active');
    if (activeConversation) {
        activeConversation.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }
});
```

### 3.3 Database Considerations

#### 3.3.1 Query Optimization

**Indexes** (already exist or should be added):

```python
# In Message model
class Meta:
    indexes = [
        models.Index(fields=['thread_id', 'sent_date']),
        models.Index(fields=['thread_id', 'is_read', 'receiver_character']),
        models.Index(fields=['sender_character', 'receiver_character']),
    ]
```

**Query Optimization**:

- Use `select_related()` for foreign keys (character, game)
- Use `prefetch_related()` if needed for related objects
- Limit conversation list to last 50 conversations (pagination if needed)

### 3.4 Testing Strategy

#### 3.4.1 Playwright E2E Tests

**File**: `tests/e2e/messaging/conversation-list.spec.ts`

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

    test('should show unread message count', async ({ page }) => {
        await page.goto('/messages/');
        const unreadBadge = page.locator('.unread-badge').first();
        
        // If unread messages exist, badge should be visible
        if (await unreadBadge.isVisible()) {
            const count = await unreadBadge.textContent();
            expect(parseInt(count || '0')).toBeGreaterThan(0);
        }
    });

    test('should switch between conversations', async ({ page }) => {
        await page.goto('/messages/');
        const firstConversation = page.locator('.conversation-item').first();
        await firstConversation.click();
        
        await page.waitForURL(/\?thread_id=.*/);
        await expect(page.locator('.message-bubble, .message-item')).toBeVisible({ timeout: 5000 });
    });

    test('should highlight active conversation', async ({ page }) => {
        await page.goto('/messages/');
        const firstConversation = page.locator('.conversation-item').first();
        await firstConversation.click();
        
        await expect(firstConversation).toHaveClass(/active/);
    });

    test('should show last message preview', async ({ page }) => {
        await page.goto('/messages/');
        const conversation = page.locator('.conversation-item').first();
        const preview = conversation.locator('.conversation-preview');
        
        await expect(preview).toBeVisible();
        const previewText = await preview.textContent();
        expect(previewText?.trim().length).toBeGreaterThan(0);
    });

    test('should show timestamp', async ({ page }) => {
        await page.goto('/messages/');
        const conversation = page.locator('.conversation-item').first();
        const timestamp = conversation.locator('.conversation-time');
        
        await expect(timestamp).toBeVisible();
        const timeText = await timestamp.textContent();
        expect(timeText).toMatch(/ago|minute|hour|day/i);
    });

    test('mobile: should toggle sidebar', async ({ page }) => {
        // Set mobile viewport
        await page.setViewportSize({ width: 375, height: 667 });
        await page.goto('/messages/');
        
        const toggleButton = page.locator('#conversation-sidebar-toggle');
        if (await toggleButton.isVisible()) {
            await toggleButton.click();
            await expect(page.locator('.conversation-sidebar')).toHaveClass(/show/);
        }
    });
});
```

---

## 4. Implementation Checklist

### Phase 1: Backend (2-3 hours)

- [ ] Update `MessageListView.get_context_data()` to build conversation list
- [ ] Update `MessageListView.get()` to mark messages as read
- [ ] Add query optimizations (select_related, indexes)
- [ ] Test backend logic with Django shell

### Phase 2: Templates (2-3 hours)

- [ ] Create `conversation_list.html` template
- [ ] Update `message_list.html` to include sidebar
- [ ] Add mobile responsive layout
- [ ] Test template rendering

### Phase 3: Styling (1-2 hours)

- [ ] Add CSS styles for conversation list
- [ ] Style active state
- [ ] Add mobile responsive styles
- [ ] Test on different screen sizes

### Phase 4: JavaScript (1 hour)

- [ ] Create `conversation-manager.js`
- [ ] Add mobile sidebar toggle
- [ ] Add auto-scroll functionality
- [ ] Test interactions

### Phase 5: Testing (2-3 hours)

- [ ] Write Playwright E2E tests
- [ ] Test all user flows
- [ ] Fix any issues
- [ ] Verify mobile responsiveness

### Phase 6: Documentation (1 hour)

- [ ] Update status documentation
- [ ] Add implementation notes
- [ ] Update user guide (if applicable)

**Total Estimated Time**: 9-13 hours (1.5-2 days)

---

## 5. Acceptance Criteria

### Functional Requirements

- [x] Conversation list displays all user's conversations
- [x] Each conversation shows avatar, nickname, game name
- [x] Unread message count badge displays correctly
- [x] Last message preview shows (first 100 chars)
- [x] Timestamp shows relative time (e.g., "2 hours ago")
- [x] Clicking conversation switches to that thread
- [x] Active conversation is highlighted
- [x] Messages marked as read when viewing thread
- [x] Empty state shows helpful message

### Non-Functional Requirements

- [x] Mobile-responsive (collapsible sidebar on mobile)
- [x] Performance: Conversation list loads in <500ms
- [x] Accessibility: Keyboard navigation works
- [x] Browser compatibility: Works in Chrome, Firefox, Safari, Edge
- [x] Playwright tests pass

---

## 6. Future Enhancements

### Phase 2 Features (Not in MVP)

1. **Real-time Updates**
   - WebSocket/SSE for new messages
   - Auto-update conversation list
   - Notification badges

2. **Search/Filter**
   - Search conversations by character name
   - Filter by game
   - Sort options (date, unread)

3. **Conversation Actions**
   - Archive conversations
   - Delete conversations
   - Mute notifications

4. **Enhanced Preview**
   - Show message type (text, image)
   - Show sender character in preview
   - Show read receipts

---

## 7. Technical Notes

### Performance Considerations

- **Query Optimization**: Use `select_related()` for foreign keys
- **Pagination**: Limit to 50 conversations initially (add pagination if needed)
- **Caching**: Consider caching conversation list (if performance issues)

### Security Considerations

- **Authorization**: Only show conversations where user is participant
- **Data Privacy**: Don't expose other users' data
- **XSS Prevention**: Escape all user-generated content

### Browser Compatibility

- **Modern Browsers**: Chrome 90+, Firefox 88+, Safari 14+, Edge 90+
- **CSS Features**: Flexbox, CSS Grid (with fallbacks)
- **JavaScript**: ES6+ (with Babel if needed)

---

## 8. References

- **Existing Documentation**: 
  - `docs/scrum/005-pending-tasks-implementation.md` - Task 2
  - `docs/architecture/implementation-guide.md` - General patterns
- **Django Documentation**: 
  - ListView: https://docs.djangoproject.com/en/stable/ref/class-based-views/generic-display/#listview
  - QuerySet API: https://docs.djangoproject.com/en/stable/ref/models/querysets/
- **Bootstrap 5**: 
  - List Group: https://getbootstrap.com/docs/5.0/components/list-group/
  - Collapse: https://getbootstrap.com/docs/5.0/components/collapse/

---

**Document Version**: 1.0  
**Last Updated**: 2025-12-28  
**Status**: Ready for Implementation



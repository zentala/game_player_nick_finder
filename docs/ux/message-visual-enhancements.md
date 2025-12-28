# Message Visual Enhancements - UX Design Document

**Status**: 📋 Design Phase  
**Priority**: High  
**Target Audience**: Mid-level Frontend Developers

## Overview

This document describes UX enhancements for message display to clearly distinguish between:
1. **Masked (Anonymous) messages** - Character nickname only
2. **Unmasked (Real Name) messages** - Character nickname + user real name + profile info

---

## Current State

### What We Have
- ✅ Basic message display with nickname
- ✅ Badge "Real Name" / "Anonymous"
- ✅ Link to user profile when unmasked
- ✅ Social media icons

### What We Need
- ❌ Different background colors for masked/unmasked messages
- ❌ Clearer visual hierarchy showing character nickname vs real name
- ❌ Better indication of "you're writing as character" vs "you're writing as real person"
- ❌ Profile information display (name, registration info) when unmasked

---

## Design Requirements

### 1. Visual Distinction: Background Colors

#### Masked (Anonymous) Messages
- **Background**: Light gray (`#f8f9fa` or `bg-light`)
- **Border**: Subtle gray border
- **Badge**: Gray "Anonymous" badge with mask icon
- **Feel**: Neutral, anonymous, safe

#### Unmasked (Real Name) Messages
- **Background**: Light blue/teal tint (`#e7f3ff` or custom `bg-info-subtle`)
- **Border**: Blue border (`border-primary` or `border-info`)
- **Badge**: Green "Real Name" badge with star icon
- **Feel**: Personal, connected, verified

### 2. Message Header Structure

#### For Masked Messages:
```
┌─────────────────────────────────────┐
│ [Character Avatar] CharacterNick   │ ← Character only
│ 🎭 Anonymous                        │
│                                     │
│ Message content here...             │
└─────────────────────────────────────┘
```

#### For Unmasked Messages:
```
┌─────────────────────────────────────┐
│ [Character Avatar] CharacterNick    │ ← Character nickname
│ ⭐ Real Name                        │
│                                     │
│ [User Avatar] @username             │ ← Real account
│ John Doe                            │ ← Real name (if available)
│ Registered: Jan 2020                │ ← Registration info
│                                     │
│ [Steam] [GitHub] [LinkedIn]        │ ← Social links
│                                     │
│ Message content here...             │
└─────────────────────────────────────┘
```

### 3. Visual Hierarchy

**Priority Order:**
1. **Character Nickname** (always visible, bold, larger)
2. **Real Name Badge** (if unmasked, prominent)
3. **User Info** (if unmasked, secondary)
4. **Message Content** (main content)

---

## Implementation Details

### CSS Classes

```css
/* Message bubble base */
.message-bubble {
    border-radius: 15px;
    padding: 12px 16px;
    margin: 4px 0;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

/* Masked (Anonymous) message */
.message-bubble.masked {
    background-color: #f8f9fa;
    border: 1px solid #dee2e6;
    color: #212529;
}

/* Unmasked (Real Name) message */
.message-bubble.unmasked {
    background-color: #e7f3ff;
    border: 2px solid #0dcaf0;
    color: #212529;
}

/* Character nickname (always prominent) */
.message-character {
    font-weight: 700;
    font-size: 1.1em;
    color: #0d6efd;
    margin-bottom: 4px;
}

/* Real name section (when unmasked) */
.identity-revealed-section {
    margin-top: 8px;
    padding-top: 8px;
    border-top: 1px solid rgba(0,0,0,0.1);
}

.identity-revealed-section .user-info {
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 4px;
}

.identity-revealed-section .user-avatar {
    width: 32px;
    height: 32px;
    border-radius: 50%;
    border: 2px solid #28a745;
}

.identity-revealed-section .user-name {
    font-weight: 600;
    color: #198754;
}

.identity-revealed-section .user-details {
    font-size: 0.85em;
    color: #6c757d;
    margin-left: 40px; /* Align with username */
}

/* Badge styling */
.badge-real-name {
    background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
    color: white;
    font-weight: 600;
    padding: 4px 8px;
    border-radius: 12px;
}

.badge-anonymous {
    background-color: #6c757d;
    color: white;
    font-weight: 500;
    padding: 4px 8px;
    border-radius: 12px;
}
```

### Template Structure

```html
<!-- Masked Message -->
<div class="message-bubble masked">
    <div class="message-header">
        <span class="message-character">{{ message.sender_character.nickname }}</span>
        <span class="badge badge-anonymous">
            <i class="bi bi-mask"></i> Anonymous
        </span>
    </div>
    <div class="message-content">{{ message.content }}</div>
    <div class="message-time">{{ message.sent_date|date:"H:i" }}</div>
</div>

<!-- Unmasked Message -->
<div class="message-bubble unmasked">
    <div class="message-header">
        <span class="message-character">{{ message.sender_character.nickname }}</span>
        <span class="badge badge-real-name">
            <i class="bi bi-star-fill"></i> Real Name
        </span>
    </div>
    
    <div class="identity-revealed-section">
        <div class="user-info">
            {% if message.sender_character.user.profile_picture %}
                <img src="{{ message.sender_character.user.profile_picture.url }}" 
                     class="user-avatar" 
                     alt="{{ message.sender_character.user.username }}">
            {% else %}
                <i class="bi bi-person-circle user-avatar-icon"></i>
            {% endif %}
            <div>
                <a href="{% url 'user_profile_display' username=message.sender_character.user.username %}" 
                   class="user-name">
                    @{{ message.sender_character.user.username }}
                </a>
                {% if message.sender_character.user.first_name or message.sender_character.user.last_name %}
                    <div class="user-real-name">
                        {{ message.sender_character.user.first_name }} {{ message.sender_character.user.last_name }}
                    </div>
                {% endif %}
            </div>
        </div>
        
        <div class="user-details">
            <i class="bi bi-calendar-check"></i> 
            Registered: {{ message.sender_character.user.date_joined|date:"M Y" }}
        </div>
        
        {% if message.sender_character.user.steam_profile or message.sender_character.user.github_profile %}
            <div class="social-links mt-2">
                {% if message.sender_character.user.steam_profile %}
                    <a href="{{ message.sender_character.user.steam_profile }}" target="_blank" class="social-link">
                        <i class="bi bi-steam"></i> Steam
                    </a>
                {% endif %}
                {% if message.sender_character.user.github_profile %}
                    <a href="{{ message.sender_character.user.github_profile }}" target="_blank" class="social-link">
                        <i class="bi bi-github"></i> GitHub
                    </a>
                {% endif %}
            </div>
        {% endif %}
    </div>
    
    <div class="message-content">{{ message.content }}</div>
    <div class="message-time">{{ message.sent_date|date:"H:i" }}</div>
</div>
```

---

## User Experience Flow

### Scenario 1: Viewing Masked Message
1. User sees message with gray background
2. Character nickname is prominent
3. "Anonymous" badge clearly visible
4. No personal information shown
5. **Feel**: Safe, anonymous, gaming-focused

### Scenario 2: Viewing Unmasked Message
1. User sees message with blue/teal background
2. Character nickname still prominent (top)
3. "Real Name" badge with star icon
4. User's real account info displayed below
5. Registration date shown
6. Social media links available
7. **Feel**: Personal, connected, verified

### Scenario 3: Writing Message (Masked)
1. User types message
2. Sees preview: "Sending as CharacterNick (Anonymous)"
3. Message will have gray background
4. **Feel**: Anonymous, safe

### Scenario 3: Writing Message (Unmasked)
1. User types message
2. Sees preview: "Sending as CharacterNick → @username (Real Name)"
3. Message will have blue background
4. **Feel**: Personal, connected

---

## Implementation Checklist

### Frontend Tasks
- [ ] Add CSS classes for masked/unmasked messages
- [ ] Update message template structure
- [ ] Add user info section for unmasked messages
- [ ] Add registration date display
- [ ] Style badges differently
- [ ] Add hover effects
- [ ] Test responsive design
- [ ] Write E2E tests

### Backend Tasks
- [ ] Ensure `date_joined` is available in template context
- [ ] Ensure `first_name` and `last_name` are available
- [ ] Add helper function to get user display name
- [ ] Update message serializers if needed

### Testing
- [ ] Visual regression tests
- [ ] E2E tests for message display
- [ ] Test with/without profile picture
- [ ] Test with/without real name
- [ ] Test with/without social links
- [ ] Test responsive design

---

## Design Mockups

### Masked Message
```
┌─────────────────────────────────────────┐
│ Warrior123                    🎭 Anonymous │
├─────────────────────────────────────────┤
│                                         │
│ Hey, remember that raid?               │
│                                         │
│                             14:23      │
└─────────────────────────────────────────┘
(Gray background, subtle border)
```

### Unmasked Message
```
┌─────────────────────────────────────────┐
│ Warrior123                    ⭐ Real Name │
├─────────────────────────────────────────┤
│ [Avatar] @johndoe                       │
│ John Doe                                │
│ 📅 Registered: Jan 2020                 │
│ [Steam] [GitHub]                        │
├─────────────────────────────────────────┤
│                                         │
│ Hey! Yes, I remember! That was epic!   │
│                                         │
│                             14:25      │
└─────────────────────────────────────────┘
(Blue/teal background, blue border)
```

---

## Accessibility Considerations

1. **Color Contrast**: Ensure sufficient contrast for text on colored backgrounds
2. **Screen Readers**: Add ARIA labels for badges and user info
3. **Keyboard Navigation**: Ensure all links are keyboard accessible
4. **Focus States**: Clear focus indicators for interactive elements

---

## Performance Considerations

1. **Avatar Loading**: Lazy load user avatars
2. **Social Icons**: Use icon fonts (Bootstrap Icons) instead of images
3. **CSS**: Use CSS classes instead of inline styles
4. **Caching**: Cache user profile data if needed

---

## Future Enhancements

1. **Animation**: Subtle fade-in when message appears
2. **Hover Effects**: Show more info on hover
3. **Profile Preview**: Modal with full profile on click
4. **Custom Colors**: Let users choose message bubble colors
5. **Themes**: Dark mode support

---

**Document Version**: 1.0  
**Last Updated**: 2024  
**Author**: UX Engineer  
**Reviewers**: Solution Architect, Frontend Lead


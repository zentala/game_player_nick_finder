# POKE System Architecture

**Status**: 📋 Specification / Design Phase  
**Last Updated**: 2024-12-19  
**Author**: Software Architect  
**Reviewers**: UX Team, Tech Lead

## Document Purpose

This document describes the architecture and design of the POKE system - a lightweight, spam-protected initial contact mechanism that precedes full messaging capabilities in the Game Player Nick Finder application.

## Executive Summary

The POKE system is designed to:
- Provide a safe, limited initial contact mechanism between characters
- Prevent spam through strict limitations and filtering
- Serve as a "handshake" that unlocks full messaging when both parties reciprocate
- Enable users to block and report spam/abuse

## Core Concept

**POKE** is a lightweight "hello" message system that acts as a gateway to full messaging:

1. **Initial Contact**: User A sends a POKE to Character B
2. **Reciprocation**: If Character B responds with a POKE back, both parties can now send full messages
3. **Unlocking**: After mutual POKE exchange, the full Message system becomes available
4. **Protection**: Strict limitations prevent spam and abuse

## Design Principles

1. **Spam Prevention First**: Multiple layers of protection (rate limiting, content filtering, blocking)
2. **User Privacy**: Respect existing privacy settings (profile visibility, etc.)
3. **Gradual Trust Building**: POKE → Response → Full Messaging (trust escalates)
4. **Character-Based**: Consistent with existing character-centric messaging system
5. **Reversible**: Users can block/report even after POKE exchange

## System Architecture

### Data Model

```
┌─────────────────────────────────────────────────────────┐
│                       Character                          │
│  (existing model - sender/receiver)                      │
└─────────────────────────────────────────────────────────┘
                          │
                          │ (sender/receiver)
                          │
        ┌─────────────────┴─────────────────┐
        │                                   │
        ▼                                   ▼
┌──────────────┐                  ┌──────────────┐
│     Poke     │                  │   Message    │
│              │                  │  (existing)  │
│ - content    │                  │              │
│ - status     │                  │ - content    │
│ - sent_date  │                  │ - thread_id  │
│ - read_at    │                  │ - privacy    │
│ - responded  │                  │ - etc.       │
└──────────────┘                  └──────────────┘
        │
        │ (unlocks)
        │
        ▼
┌─────────────────────────────────────────┐
│      PokeResponse (optional)            │
│  - tracks mutual POKE completion        │
│  - unlocks Message system               │
└─────────────────────────────────────────┘
```

### Core Models

#### 1. Poke Model

```python
class Poke(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),      # Sent, waiting for response
        ('RESPONDED', 'Responded'),  # Recipient sent POKE back
        ('IGNORED', 'Ignored'),      # Recipient ignored
        ('BLOCKED', 'Blocked'),      # Blocked by recipient
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    sender_character = models.ForeignKey(Character, on_delete=models.CASCADE, related_name='sent_pokes')
    receiver_character = models.ForeignKey(Character, on_delete=models.CASCADE, related_name='received_pokes')
    
    # Content (strictly limited)
    content = models.CharField(max_length=100)  # Max 100 chars, no links allowed
    
    # Status tracking
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    sent_date = models.DateTimeField(auto_now_add=True)
    responded_at = models.DateTimeField(null=True, blank=True)
    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)
    
    # Moderation
    reported_as_spam = models.BooleanField(default=False)
    reported_at = models.DateTimeField(null=True, blank=True)
    reported_by = models.ForeignKey(get_user_model(), null=True, blank=True, on_delete=models.SET_NULL)
    
    class Meta:
        unique_together = ('sender_character', 'receiver_character')
        ordering = ['-sent_date']
        indexes = [
            models.Index(fields=['receiver_character', 'status', '-sent_date']),
            models.Index(fields=['sender_character', 'status']),
        ]
    
    def can_send_full_message(self):
        """Check if mutual POKE exchange completed"""
        return self.status == 'RESPONDED' or self.is_mutual()
    
    def is_mutual(self):
        """Check if receiver also sent a POKE back"""
        return Poke.objects.filter(
            sender_character=self.receiver_character,
            receiver_character=self.sender_character,
            status__in=['PENDING', 'RESPONDED']
        ).exists()
```

#### 2. PokeBlock Model (Optional, can use existing blocking system)

```python
class PokeBlock(models.Model):
    """Block POKEs from specific character"""
    blocker_character = models.ForeignKey(
        Character,
        on_delete=models.CASCADE,
        related_name='blocked_poke_senders'
    )
    blocked_character = models.ForeignKey(
        Character,
        on_delete=models.CASCADE,
        related_name='blocked_poke_receivers'
    )
    blocked_at = models.DateTimeField(auto_now_add=True)
    reason = models.CharField(max_length=200, blank=True)  # Optional reason
    
    class Meta:
        unique_together = ('blocker_character', 'blocked_character')
```

### Business Logic

#### 1. POKE Sending Rules

**Rate Limiting**:
- Maximum 5 POKEs per user per 24 hours (configurable)
- Maximum 1 POKE to same character per 30 days (configurable)
- Check against PokeBlock before allowing

**Content Validation**:
- Maximum 100 characters (strict)
- No URLs/links allowed (regex: `(http|https|www\.|\.com|\.net|\.org|://)`)
- No email addresses allowed (regex: `@`)
- Basic profanity filtering (configurable word list)
- HTML/strip tags (sanitize input)

**Prerequisites**:
- User must have at least one character
- Receiver character must be from different user
- No existing POKE in last 30 days to same character
- Receiver character's user profile must allow contacts (respect privacy settings)

#### 2. POKE Response Flow

```
User A sends POKE to Character B
    ↓
Character B receives POKE (status: PENDING)
    ↓
Character B has 3 options:
    1. RESPOND - Send POKE back to Character A
    2. IGNORE - Mark as ignored (no response)
    3. BLOCK - Block Character A from sending more POKEs
    ↓
If RESPOND:
    - Character B sends POKE to Character A
    - Both POKEs marked as RESPONDED
    - Both parties can now send full Messages
    ↓
If IGNORE:
    - POKE status = IGNORED
    - No full messaging unlocked
    - User A can see status
    ↓
If BLOCK:
    - POKE status = BLOCKED
    - PokeBlock record created
    - User A cannot send more POKEs
    - Can report as spam
```

#### 3. Message Unlocking Logic

Full `Message` system becomes available when:
- Both characters have sent POKEs to each other
- At least one POKE has status `RESPONDED`
- No active PokeBlock exists between characters

Implementation check:
```python
def can_send_message(sender_character, receiver_character):
    # Check if mutual POKE exists
    poke_a_to_b = Poke.objects.filter(
        sender_character=sender_character,
        receiver_character=receiver_character,
        status='RESPONDED'
    ).exists()
    
    poke_b_to_a = Poke.objects.filter(
        sender_character=receiver_character,
        receiver_character=sender_character,
        status__in=['PENDING', 'RESPONDED']
    ).exists()
    
    # Check for blocks
    is_blocked = PokeBlock.objects.filter(
        blocker_character=receiver_character,
        blocked_character=sender_character
    ).exists()
    
    return (poke_a_to_b or poke_b_to_a) and not is_blocked
```

### Anti-Spam Measures

#### Layer 1: Rate Limiting
- User-level: 5 POKEs per 24h
- Character-pair level: 1 POKE per 30 days
- Configurable in Django settings

#### Layer 2: Content Filtering
- URL/link detection and rejection
- Email address detection and rejection
- Profanity filter (configurable word list)
- Character limit (100 chars max)

#### Layer 3: User Controls
- Block functionality (prevents future POKEs)
- Report as spam (flags for moderation)
- Ignore option (silent rejection)

#### Layer 4: System Monitoring
- Track POKE rejection rates per character
- Flag characters with high block/report rates
- Automatic temporary restrictions for abusive patterns

### API Design

#### Endpoints

```
POST   /api/pokes/                    # Send POKE
GET    /api/pokes/received/           # List received POKEs
GET    /api/pokes/sent/               # List sent POKEs
POST   /api/pokes/{id}/respond/       # Respond to POKE (send POKE back)
POST   /api/pokes/{id}/ignore/        # Ignore POKE
POST   /api/pokes/{id}/block/         # Block sender + report
GET    /api/pokes/{id}/               # Get POKE details
DELETE /api/pokes/{id}/               # Delete POKE (own sent ones)
```

#### Example Request/Response

**Send POKE**:
```json
POST /api/pokes/
{
  "receiver_character_id": "uuid",
  "content": "Hey! Remember playing together in 2010?"
}

Response 201:
{
  "id": "uuid",
  "sender_character": {...},
  "receiver_character": {...},
  "content": "Hey! Remember playing together in 2010?",
  "status": "PENDING",
  "sent_date": "2024-12-19T10:00:00Z"
}

Response 400 (rate limit):
{
  "error": "rate_limit_exceeded",
  "message": "You can send maximum 5 POKEs per 24 hours",
  "retry_after": 3600
}
```

**List Received POKEs**:
```json
GET /api/pokes/received/?status=PENDING&page=1

Response 200:
{
  "count": 15,
  "next": "/api/pokes/received/?page=2",
  "results": [
    {
      "id": "uuid",
      "sender_character": {
        "id": "uuid",
        "nickname": "OldGamer",
        "game": {"name": "World of Warcraft"},
        "avatar": "url"
      },
      "content": "Hey! Remember playing together?",
      "status": "PENDING",
      "sent_date": "2024-12-19T10:00:00Z",
      "is_read": false
    },
    ...
  ]
}
```

### UI/UX Flow

#### 1. Sending POKE

**Location**: Character profile page, character list, search results

**UI Elements**:
- "Send POKE" button (replaces "Send Message" if not unlocked)
- Modal/form with:
  - Character info (nickname, game, avatar)
  - Text input (100 char limit, counter)
  - Preview of filtered content
  - "Send" button
  - Character counter: "X POKEs remaining today"

**Validation**:
- Real-time character count
- Real-time content validation (show warnings for URLs/links)
- Disable submit if invalid

#### 2. Receiving POKE

**Notification**:
- Badge/count on "POKEs" menu item
- Email notification (optional, user preference)
- In-app notification

**POKE List View**:
- List of received POKEs (similar to message list)
- Show: sender character, game, content, timestamp
- Actions per POKE:
  - "Respond" (sends POKE back)
  - "Ignore"
  - "Block & Report"

**POKE Detail View**:
- Full POKE content
- Sender character info
- Actions (Respond/Ignore/Block)

#### 3. Status Indicators

- **PENDING**: "Waiting for response"
- **RESPONDED**: "Mutual POKE - You can now message!"
- **IGNORED**: "Not responded"
- **BLOCKED**: "Blocked by recipient"

### Database Migrations

```python
# Migration 0003_add_poke_system.py

operations = [
    migrations.CreateModel(
        name='Poke',
        fields=[
            ('id', models.UUIDField(...)),
            ('sender_character', models.ForeignKey(...)),
            ('receiver_character', models.ForeignKey(...)),
            ('content', models.CharField(max_length=100)),
            ('status', models.CharField(...)),
            ('sent_date', models.DateTimeField(...)),
            ('responded_at', models.DateTimeField(...)),
            ('is_read', models.BooleanField(...)),
            ('read_at', models.DateTimeField(...)),
            ('reported_as_spam', models.BooleanField(...)),
            ('reported_at', models.DateTimeField(...)),
            ('reported_by', models.ForeignKey(...)),
        ],
        options={
            'unique_together': {('sender_character', 'receiver_character')},
            'indexes': [...],
        },
    ),
    migrations.CreateModel(
        name='PokeBlock',
        fields=[...],
    ),
]
```

### Settings Configuration

```python
# settings/base.py

# POKE System Settings
POKE_MAX_CONTENT_LENGTH = 100
POKE_MAX_PER_USER_PER_DAY = 5
POKE_COOLDOWN_DAYS = 30  # Days between POKEs to same character
POKE_CONTENT_FILTER_URLS = True
POKE_CONTENT_FILTER_EMAILS = True
POKE_PROFANITY_FILTER_ENABLED = True
POKE_PROFANITY_WORDLIST = ['list', 'of', 'words']  # Or load from file
```

### Testing Strategy

#### Unit Tests

1. **Model Tests**:
   - POKE creation and validation
   - Status transitions
   - Mutual POKE detection
   - Block functionality

2. **Content Filtering Tests**:
   - URL detection and rejection
   - Email detection and rejection
   - Character limit enforcement
   - Profanity filtering

3. **Rate Limiting Tests**:
   - Per-user rate limits
   - Per-character-pair cooldowns
   - Block enforcement

#### Integration Tests

1. **API Tests**:
   - All endpoints with valid/invalid data
   - Authentication and authorization
   - Rate limiting responses

2. **Workflow Tests**:
   - Full POKE → Response → Message unlock flow
   - Block → Cannot send POKE flow
   - Rate limit → Wait → Send flow

#### E2E Tests (Playwright)

1. **Send POKE Flow**:
   - Navigate to character profile
   - Click "Send POKE"
   - Fill form, submit
   - Verify POKE sent

2. **Receive and Respond Flow**:
   - Receive POKE notification
   - View POKE list
   - Respond to POKE
   - Verify mutual POKE unlocks messaging

3. **Block Flow**:
   - Receive POKE
   - Block sender
   - Attempt to send POKE back (should fail)
   - Verify block status

### Security Considerations

1. **Input Validation**:
   - Always validate content server-side (never trust client)
   - Sanitize HTML/strip tags
   - Validate character IDs (UUID format)
   - Check permissions before actions

2. **Rate Limiting**:
   - Implement at middleware/API level
   - Use Redis/cache for distributed rate limiting (if multi-instance)
   - Return proper HTTP 429 responses

3. **Privacy**:
   - Respect user profile visibility settings
   - Don't expose blocked status to blocked user
   - Audit log for moderation actions

4. **Moderation**:
   - Track report counts per character/user
   - Automatic flagging for high report rates
   - Admin interface for reviewing reports

### Performance Considerations

1. **Database Indexing**:
   - Index on `(receiver_character, status, sent_date)` for list queries
   - Index on `(sender_character, status)` for sent list
   - Index on `(blocker_character, blocked_character)` for block checks

2. **Caching**:
   - Cache rate limit counters (Redis/Memcached)
   - Cache mutual POKE status (for message unlock checks)
   - Invalidate cache on POKE creation/update

3. **Query Optimization**:
   - Use `select_related` for character/user data
   - Paginate POKE lists (50 per page)
   - Bulk updates for read status

### Migration Strategy

1. **Phase 1: Backend Implementation**
   - Create models and migrations
   - Implement business logic and validation
   - Create API endpoints
   - Write unit/integration tests

2. **Phase 2: UI Implementation**
   - Add POKE sending UI
   - Create POKE list/detail views
   - Add notifications
   - Write E2E tests

3. **Phase 3: Integration**
   - Update Message system to check POKE status
   - Hide "Send Message" if not unlocked
   - Show "Send POKE" instead
   - Update existing message flows

4. **Phase 4: Monitoring & Tuning**
   - Monitor rate limit effectiveness
   - Track spam/abuse patterns
   - Adjust limits based on usage
   - User feedback and improvements

### Future Enhancements

1. **Smart Suggestions**:
   - Suggest characters to POKE based on shared games/years
   - "You played together in 2010" suggestions

2. **POKE Templates**:
   - Pre-written POKE messages
   - "Remember playing [game] together in [year]?"

3. **Analytics**:
   - POKE response rates
   - Time to response
   - Conversion to full messaging

4. **Moderation Dashboard**:
   - Admin interface for reviewing reports
   - Automated spam detection
   - Bulk actions

## Related Documentation

- [Implementation Guide](./implementation-guide.md) - Step-by-step implementation
- [POKE Feature Specification](../features/poke-system-specification.md) - Detailed feature spec
- [Message System Architecture](../architecture/messaging-architecture.md) - Existing messaging system

---

**Document Version**: 1.0  
**Last Updated**: 2024-12-19  
**Author**: Software Architect  
**Reviewers**: UX Team, Tech Lead  
**Status**: 📋 Ready for Review


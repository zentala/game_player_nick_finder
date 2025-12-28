# POKE System Feature Specification

**Status**: 📋 Specification  
**Last Updated**: 2024-12-19  
**Epic**: Enhanced Messaging with Privacy Controls  
**Story Points**: 13  
**Priority**: High

## Overview

The POKE system is a lightweight, spam-protected initial contact mechanism that allows users to initiate conversations with characters they want to reconnect with. It serves as a "handshake" that unlocks full messaging capabilities after mutual acknowledgment.

## User Stories

### As a User

1. **Send POKE**: As a user, I want to send a short "hello" message (POKE) to a character, so I can initiate contact without spamming.

2. **Receive POKE**: As a user, I want to receive and review POKEs from other characters, so I can decide if I want to respond.

3. **Respond to POKE**: As a user, I want to respond to a POKE by sending one back, so we can unlock full messaging.

4. **Ignore POKE**: As a user, I want to ignore unwanted POKEs, so I don't have to engage with everyone.

5. **Block Spam**: As a user, I want to block and report spam POKEs, so I can protect myself from abuse.

6. **Unlock Messaging**: As a user, after mutual POKE exchange, I want to use the full messaging system, so I can have longer conversations.

### As a System

1. **Prevent Spam**: The system must prevent spam through rate limiting and content filtering.

2. **Track Status**: The system must track POKE status (pending, responded, ignored, blocked).

3. **Enforce Limits**: The system must enforce daily limits and cooldown periods.

4. **Unlock Messaging**: The system must unlock full messaging after mutual POKE exchange.

## Functional Requirements

### FR1: POKE Creation

**Priority**: Must Have

**Description**: Users can send a POKE to any character (except their own).

**Acceptance Criteria**:
- [ ] User must be logged in and have at least one character
- [ ] POKE can only be sent to characters from different users
- [ ] POKE content is limited to 100 characters
- [ ] POKE content cannot contain URLs or links
- [ ] POKE content cannot contain email addresses
- [ ] User can send maximum 5 POKEs per 24 hours
- [ ] User can send maximum 1 POKE to same character per 30 days
- [ ] POKE cannot be sent if receiver has blocked sender
- [ ] POKE respects receiver's profile visibility settings
- [ ] POKE is stored with status "PENDING"

**UI Elements**:
- "Send POKE" button on character profile/page
- Modal with character info, text input (100 char limit), send button
- Character counter: "X POKEs remaining today"
- Real-time validation warnings

### FR2: POKE Reception

**Priority**: Must Have

**Description**: Users receive POKEs in a dedicated list view.

**Acceptance Criteria**:
- [ ] Users see list of all received POKEs
- [ ] POKEs are sorted by sent_date (newest first)
- [ ] Unread POKEs are marked/highlighted
- [ ] Each POKE shows: sender character (nickname, game, avatar), content, timestamp
- [ ] POKEs can be filtered by status (PENDING, RESPONDED, IGNORED, BLOCKED)
- [ ] POKE list is paginated (50 per page)
- [ ] Badge/count shows number of unread POKEs
- [ ] Clicking POKE opens detail view

**UI Elements**:
- "POKEs" menu item with unread count badge
- POKE list view (similar to message list)
- POKE detail view
- Filter buttons (All, Pending, Responded, etc.)

### FR3: POKE Response

**Priority**: Must Have

**Description**: Users can respond to a POKE by sending a POKE back.

**Acceptance Criteria**:
- [ ] User can respond to POKE with status "PENDING"
- [ ] Responding creates new POKE from receiver to original sender
- [ ] Both POKEs are marked as "RESPONDED"
- [ ] After mutual POKE, both parties can send full Messages
- [ ] Response follows same validation rules as POKE creation
- [ ] Response is subject to same rate limits

**UI Elements**:
- "Respond" button on POKE detail view
- Response form (same as POKE creation)
- Success message: "POKE sent! You can now send full messages."

### FR4: POKE Ignore

**Priority**: Must Have

**Description**: Users can ignore unwanted POKEs without responding.

**Acceptance Criteria**:
- [ ] User can mark POKE as "IGNORED"
- [ ] Ignored POKEs are removed from "Pending" list
- [ ] Sender can see their POKE status changed to "IGNORED"
- [ ] Ignoring does not unlock messaging
- [ ] Ignored POKEs can be viewed in "Ignored" filter

**UI Elements**:
- "Ignore" button on POKE detail view
- Confirmation dialog: "Ignore this POKE? Sender will not be notified."
- POKE moved to "Ignored" status

### FR5: POKE Block & Report

**Priority**: Must Have

**Description**: Users can block senders and report spam POKEs.

**Acceptance Criteria**:
- [ ] User can block sender character from sending more POKEs
- [ ] Blocking creates PokeBlock record
- [ ] Blocked sender cannot send new POKEs to blocker
- [ ] User can optionally report POKE as spam
- [ ] Reported POKEs are flagged for moderation
- [ ] Blocked POKEs are marked as "BLOCKED"
- [ ] Blocked sender sees status "BLOCKED" (but not who blocked)

**UI Elements**:
- "Block & Report" button on POKE detail view
- Modal with:
  - Reason selection (Spam, Harassment, Other)
  - Optional text field for details
  - "Block" and "Cancel" buttons
- Confirmation message

### FR6: Message Unlocking

**Priority**: Must Have

**Description**: Full messaging system unlocks after mutual POKE exchange.

**Acceptance Criteria**:
- [ ] "Send Message" button appears after mutual POKE
- [ ] "Send POKE" button is hidden after mutual POKE
- [ ] Message system checks mutual POKE status before allowing messages
- [ ] Message system respects existing privacy settings
- [ ] Block status prevents messaging even after POKE

**UI Elements**:
- Conditional button: "Send POKE" or "Send Message"
- Status indicator: "POKE sent - waiting for response"
- Status indicator: "Mutual POKE - messaging unlocked!"

### FR7: Rate Limiting

**Priority**: Must Have

**Description**: System enforces rate limits to prevent spam.

**Acceptance Criteria**:
- [ ] Maximum 5 POKEs per user per 24 hours (configurable)
- [ ] Maximum 1 POKE to same character per 30 days (configurable)
- [ ] Rate limit errors return HTTP 429 with retry_after
- [ ] Rate limit counters reset at appropriate intervals
- [ ] Rate limits are enforced at API/view level

**UI Elements**:
- Character counter: "X POKEs remaining today"
- Rate limit error message: "You can send maximum 5 POKEs per 24 hours. Try again in X hours."
- Disabled "Send" button when limit reached

### FR8: Content Filtering

**Priority**: Must Have

**Description**: System filters POKE content to prevent spam/abuse.

**Acceptance Criteria**:
- [ ] URLs/links are detected and rejected (regex: `(http|https|www\.|\.com|\.net|\.org|://)`)
- [ ] Email addresses are detected and rejected (regex: `@`)
- [ ] Content is limited to 100 characters
- [ ] HTML tags are stripped/sanitized
- [ ] Profanity filter (optional, configurable word list)
- [ ] Validation errors shown in real-time

**UI Elements**:
- Real-time validation warnings in form
- Character counter (100 max)
- Warning message: "URLs and links are not allowed"
- Warning message: "Email addresses are not allowed"

### FR9: Notifications

**Priority**: Should Have

**Description**: Users receive notifications for new POKEs.

**Acceptance Criteria**:
- [ ] In-app notification badge on "POKEs" menu item
- [ ] Email notification (optional, user preference)
- [ ] Notification when POKE is responded to
- [ ] Notification when POKE is ignored/blocked (for sender)

**UI Elements**:
- Badge with unread count
- Email notification template
- In-app notification toast

### FR10: POKE Management

**Priority**: Should Have

**Description**: Users can manage their sent and received POKEs.

**Acceptance Criteria**:
- [ ] Users can view list of sent POKEs
- [ ] Users can see status of sent POKEs (Pending, Responded, Ignored, Blocked)
- [ ] Users can delete their own sent POKEs
- [ ] Users can view history of POKEs with specific character
- [ ] POKEs older than 90 days are auto-archived (optional)

**UI Elements**:
- "Sent POKEs" tab/view
- Status indicators per POKE
- Delete button on sent POKEs
- Archive/history view

## Non-Functional Requirements

### NFR1: Performance

- POKE list queries must complete in < 200ms
- POKE creation must complete in < 500ms
- Rate limit checks must complete in < 50ms
- Support 1000+ concurrent POKE operations

### NFR2: Scalability

- Database indexes on critical query paths
- Cache rate limit counters (Redis/Memcached)
- Pagination for POKE lists
- Efficient queries (select_related, prefetch_related)

### NFR3: Security

- Input validation always on server-side
- XSS protection (HTML sanitization)
- CSRF protection on all forms
- Rate limiting at middleware level
- Audit logging for moderation actions

### NFR4: Usability

- Clear status indicators
- Intuitive UI/UX
- Helpful error messages
- Mobile-responsive design
- Accessibility compliance (WCAG 2.1 AA)

## Technical Implementation

### Models

See [POKE System Architecture](../architecture/poke-system-architecture.md#core-models) for detailed model specifications.

### API Endpoints

See [POKE System Architecture](../architecture/poke-system-architecture.md#api-design) for API specifications.

### Views/Forms

- `PokeListView` - List received/sent POKEs
- `PokeDetailView` - View POKE details
- `SendPokeView` - Send POKE form
- `RespondPokeView` - Respond to POKE
- `IgnorePokeView` - Ignore POKE
- `BlockPokeView` - Block sender
- `PokeForm` - POKE creation form with validation

### Templates

- `pokes/poke_list.html` - POKE list view
- `pokes/poke_detail.html` - POKE detail view
- `pokes/send_poke.html` - Send POKE form/modal
- `pokes/poke_item.html` - POKE list item component

## Testing Requirements

### Unit Tests

- [ ] Model validation tests
- [ ] Content filtering tests
- [ ] Rate limiting tests
- [ ] Status transition tests
- [ ] Block functionality tests

### Integration Tests

- [ ] API endpoint tests
- [ ] Workflow tests (send → respond → unlock)
- [ ] Rate limit enforcement tests

### E2E Tests (Playwright)

- [ ] Send POKE flow
- [ ] Receive and respond flow
- [ ] Ignore POKE flow
- [ ] Block POKE flow
- [ ] Message unlocking flow
- [ ] Rate limit display and enforcement

## Dependencies

- Existing Character model
- Existing Message model (for unlocking)
- User authentication system
- Notification system (optional)
- Email service (optional)

## Configuration

See [POKE System Architecture](../architecture/poke-system-architecture.md#settings-configuration) for settings.

## Migration Plan

1. **Phase 1**: Backend (models, API, business logic)
2. **Phase 2**: UI (forms, views, templates)
3. **Phase 3**: Integration (message unlocking, notifications)
4. **Phase 4**: Testing & refinement

## Open Questions

1. Should POKEs expire after certain time? (e.g., 90 days)
2. Should users be able to edit sent POKEs? (probably no)
3. Should there be POKE templates/suggestions?
4. Should blocked users see they're blocked or just silently fail?
5. Should admins have moderation dashboard for reported POKEs?

## Related Documentation

- [POKE System Architecture](../architecture/poke-system-architecture.md) - Technical architecture
- [Implementation Guide](../architecture/implementation-guide.md) - Step-by-step implementation
- [Message System](../architecture/messaging-architecture.md) - Existing messaging system

---

**Document Version**: 1.0  
**Last Updated**: 2024-12-19  
**Author**: Product Owner, UX Team  
**Reviewers**: Tech Lead, Development Team  
**Status**: 📋 Ready for Implementation


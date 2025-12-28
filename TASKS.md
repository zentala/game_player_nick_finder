# Development Tasks Roadmap
## Game Player Nick Finder - Developer Tasks

**Last Updated**: 2025-12-28
**Based On**: [Technical Audit 2025-12-28](TECHNICAL_AUDIT_2025-12-28.md)
**Project Status**: [PROJECT_STATUS_SUMMARY.md](docs/PROJECT_STATUS_SUMMARY.md)

---

## 📋 Table of Contents

1. [🚨 Pre-Production Deployment Checklist](#-pre-production-deployment-checklist) **← START HERE BEFORE LAUNCH**
2. [Current State Overview](#current-state-overview)
3. [Sprint 1: CRITICAL - Test Verification](#sprint-1-critical---test-verification)
4. [Sprint 2: HIGH - Screenshots & Memories UI](#sprint-2-high---screenshots--memories-ui)
5. [Sprint 3: MEDIUM - Mobile Responsiveness](#sprint-3-medium---mobile-responsiveness)
6. [Sprint 4+: LOW - Future Enhancements](#sprint-4-low---future-enhancements)
7. [Task Assignment & Branching Strategy](#task-assignment--branching-strategy)
8. [CI/CD & GitHub Actions](#cicd--github-actions)

---

## 🚨 Pre-Production Deployment Checklist

**Priority**: CRITICAL - MUST COMPLETE BEFORE PRODUCTION LAUNCH
**Status**: ⛔ NOT READY - Email validation disabled (development mode only)
**Duration**: 2-3 weeks of focused work
**Assignee**: DevOps Team + Backend Team

### Overview
Before launching to production, this project requires comprehensive security hardening, email validation setup, and E2E test verification. Email is currently disabled for development but MUST be required in production.

**Detailed Checklist**: [docs/deployment/BEFORE_PRODUCTION_CHECKLIST.md](docs/deployment/BEFORE_PRODUCTION_CHECKLIST.md)

### Quick Task List

**🔴 CRITICAL - Email Validation (1 week)**:
- [ ] Enable email requirement in production settings (`ACCOUNT_EMAIL_REQUIRED = True`)
- [ ] Enable email verification (`ACCOUNT_EMAIL_VERIFICATION = 'mandatory'`)
- [ ] Set up SendGrid/AWS SES email service
- [ ] Update and test all signup/email tests
- [ ] Document email configuration process

**🔴 CRITICAL - Security Hardening (3-4 days)**:
- [ ] Disable DEBUG mode (`DEBUG = False`)
- [ ] Set secure ALLOWED_HOSTS
- [ ] Configure HTTPS and security headers (HSTS, CSP, etc.)
- [ ] Change admin URL from /admin/
- [ ] Secure cookies (SESSION_COOKIE_SECURE, CSRF_COOKIE_SECURE)

**🟠 HIGH - E2E Test Completion (1 week)**:
- [ ] All 24 E2E tests must pass (currently 27% pass rate)
- [ ] Fix failing tests
- [ ] Verify consistent passes (run 3x each)
- [ ] Load fixtures (`pnpm load:fixtures`) before testing

**🟡 MEDIUM - Database & Monitoring (1 week)**:
- [ ] Migrate from SQLite to PostgreSQL
- [ ] Set up automated backups
- [ ] Configure error tracking (Sentry)
- [ ] Set up application monitoring
- [ ] Configure centralized logging

**🟡 MEDIUM - Testing & Compliance (3-4 days)**:
- [ ] Security audit (OWASP ZAP scan)
- [ ] Accessibility audit (WCAG 2.1 AA)
- [ ] Write Privacy Policy & Terms of Service
- [ ] Load testing and performance baseline

### Key Decisions Made
- ✅ Email disabled for development (ease of testing)
- ✅ Email required for production (security, password reset, compliance)
- ✅ SQLite for development, PostgreSQL for production
- ✅ Bootstrap 5 for development, migration to Next.js + Joy UI planned for future

### No Deploy Without Checklist Completion!
**DO NOT DEPLOY TO PRODUCTION UNTIL ALL ITEMS ARE COMPLETED!**

---

## 🎯 Current State Overview

**Project Completion**: **85%** (MVP features)

### ✅ What IS Implemented (100% Complete)

**All 7 Epics Fully Implemented**:
1. ✅ Enhanced Messaging + POKE System + Conversation UI
2. ✅ Character-Based Friend System
3. ✅ User Profile System
4. ✅ Character Custom Profile (backend)
5. ✅ Character Blocking System
6. ✅ Identity Reveal System
7. ✅ Homepage Layout Switcher

**Backend**: 100% Complete for MVP
**Frontend**: 90% Complete (missing Screenshots/Memories UI)
**Tests**: 24 E2E tests written (need verification)

### ❌ What Needs Work (15% Remaining)

1. ⚠️ **CRITICAL**: Verify all 24 E2E tests work correctly
2. ❌ **HIGH**: Screenshots Upload UI (backend ready)
3. ❌ **HIGH**: Memories Management UI (backend ready)
4. ⚠️ **MEDIUM**: Mobile Responsiveness polish
5. ❌ **LOW**: Future enhancements (real-time, advanced UX)

---

## 🔴 SPRINT 0: CRITICAL - Security Vulnerabilities
**Priority**: CRITICAL (BLOCKER)
**Duration**: 1-2 days
**Effort**: ~5-8 hours
**Assignee**: TBD
**GitHub Alert**: https://github.com/zentala/game_player_nick_finder/security/dependabot

### Goal
Fix 9 security vulnerabilities detected by GitHub Dependabot.

### Vulnerability Summary
- **1 Critical** - Requires immediate attention
- **3 High** - Should be fixed ASAP
- **4 Moderate** - Fix before MVP launch
- **1 Low** - Can be addressed later

### Tasks

#### Task 0.1: Analyze Vulnerabilities
**Branch**: `fix/security-vulnerabilities`
**Effort**: 1 hour

**Steps**:
```bash
# 1. Visit Dependabot alerts
# https://github.com/zentala/game_player_nick_finder/security/dependabot

# 2. Document each vulnerability
# - Package name
# - Current version
# - Fixed version
# - CVE number
# - Severity
# - Impact on project
```

**Deliverable**: Create `docs/security/VULNERABILITIES_2025-12-28.md` with analysis

---

#### Task 0.2: Fix Critical & High Vulnerabilities
**Branch**: Same as 0.1
**Effort**: 3-4 hours

**Steps**:
```bash
# Update Python dependencies
pipenv update [package-name]

# Or update all
pipenv update

# Update Node dependencies
pnpm update [package-name]

# Or update all with security fixes
pnpm audit fix
```

**Acceptance Criteria**:
- [ ] All CRITICAL vulnerabilities fixed
- [ ] All HIGH vulnerabilities fixed
- [ ] Dependencies updated in Pipfile.lock and pnpm-lock.yaml
- [ ] Application still works (run tests)
- [ ] No breaking changes introduced

---

#### Task 0.3: Fix Moderate & Low Vulnerabilities
**Branch**: Same as 0.1
**Effort**: 2-3 hours

**Similar to 0.2 but for lower priority issues**

**Acceptance Criteria**:
- [ ] All MODERATE vulnerabilities fixed
- [ ] LOW vulnerability assessed (fix or accept risk)
- [ ] All tests still passing
- [ ] Documentation updated

---

#### Task 0.4: Verify & Document
**Branch**: Same as 0.1
**Effort**: 1 hour

**Steps**:
```bash
# Run security audit
pipenv check
pnpm audit

# Run all tests
pnpm test:e2e

# Check GitHub Dependabot
# Should show 0 vulnerabilities
```

**Deliverable**: Update `docs/security/VULNERABILITIES_2025-12-28.md` with resolution

---

## 🔴 SPRINT 1: CRITICAL - Test Verification
**Priority**: HIGHEST
**Duration**: 5-7 days
**Effort**: ~43 hours (based on detailed breakdown)
**Assignee**: TBD
**Strategy**: [E2E Test Strategy](docs/testing/E2E_TEST_STRATEGY.md)

### Goal
Verify all 24 E2E tests pass and all implemented features work correctly.

**IMPORTANT**: Follow the detailed strategy in [docs/testing/E2E_TEST_STRATEGY.md](docs/testing/E2E_TEST_STRATEGY.md) for:
- 📋 Faza 1: IDENTYFIKACJA (Discovery Phase) - How to identify and categorize errors
- 📊 Faza 2: PRIORYTETYZACJA (Triage Phase) - P0/P1/P2/P3 priority framework
- 🔧 Faza 3: EXECUTION (Fix Phase) - Sprint breakdown and fix templates
- 🎯 Faza 4: VERIFICATION (QA Phase) - Regression testing and manual QA

### Tasks

#### Task 1.1: Test Environment Setup
**Branch**: `test/verify-e2e-tests`
**Effort**: 2 hours

**Steps**:
```bash
# 1. Create branch
git checkout -b test/verify-e2e-tests

# 2. Load fixtures
pnpm load:fixtures
# Or: .\load_fixtures.ps1 (Windows) / ./load_fixtures.sh (Unix)

# 3. Verify database has test data
python manage.py shell
>>> from app.models import CustomUser, Character
>>> CustomUser.objects.count()  # Should be > 0
>>> Character.objects.count()   # Should be > 0

# 4. Start Django server
python manage.py runserver
```

**Acceptance Criteria**:
- [ ] Fixtures loaded successfully
- [ ] Database contains test users: `testuser`, `otheruser`, `privateuser`
- [ ] Django server running on http://localhost:7600
- [ ] No migration warnings

---

#### Task 1.2: Run All E2E Tests
**Branch**: Same as 1.1
**Effort**: 3 hours

**Steps**:
```bash
# Run all tests
pnpm test:e2e

# Or run specific category
pnpm test:e2e tests/e2e/auth/
pnpm test:e2e tests/e2e/characters/
pnpm test:e2e tests/e2e/friends/
pnpm test:e2e tests/e2e/profile/
pnpm test:e2e tests/e2e/blocking/
pnpm test:e2e tests/e2e/pokes/
pnpm test:e2e tests/e2e/messaging/
pnpm test:e2e tests/e2e/navigation/
```

**Document Results**:
Create `docs/testing/E2E_TEST_RESULTS_2025-12-28.md`:

```markdown
# E2E Test Results - 2025-12-28

## Summary
- Total Tests: 24
- Passed: X
- Failed: Y
- Skipped: Z

## Failures Detail

### Authentication Tests (5 tests)
- [ ] login.spec.ts - PASS/FAIL - [error details if fail]
- [ ] logout.spec.ts - PASS/FAIL
- [ ] password-change.spec.ts - PASS/FAIL
- [ ] password-reset.spec.ts - PASS/FAIL
- [ ] signup.spec.ts - PASS/FAIL

### Character Tests (2 tests)
- [ ] character-profile-display.spec.ts - PASS/FAIL
- [ ] character-profile-edit.spec.ts - PASS/FAIL

[... continue for all 24 tests]

## Critical Failures
List failures that block core functionality:
1. [Test name] - [Error] - [Impact]

## Minor Failures
List failures that are UI/UX issues:
1. [Test name] - [Error] - [Impact]
```

**Acceptance Criteria**:
- [ ] All 24 tests executed
- [ ] Results documented with screenshots for failures
- [ ] Failures categorized (critical vs minor)
- [ ] GitHub Issues created for each failure

---

#### Task 1.3: Fix Test Failures (CRITICAL)
**Branch**: `fix/e2e-test-failures-critical`
**Effort**: 10-15 hours (depends on failure count)

**Process**:
1. For each CRITICAL failure:
   - Create sub-branch: `fix/e2e-[test-name]`
   - Fix the issue in code
   - Re-run test to verify fix
   - Commit with message: `fix: [test-name] - [what was fixed]`
   - Merge to `fix/e2e-test-failures-critical`

2. Create PR: `fix/e2e-test-failures-critical` → `main`

**Acceptance Criteria**:
- [ ] All CRITICAL test failures fixed
- [ ] Tests pass consistently (run 3 times to verify)
- [ ] No new bugs introduced
- [ ] Code reviewed

---

#### Task 1.4: Fix Test Failures (MINOR)
**Branch**: `fix/e2e-test-failures-minor`
**Effort**: 5-10 hours

Similar process as 1.3 but for minor/UX failures.

**Acceptance Criteria**:
- [ ] All MINOR test failures fixed
- [ ] 100% test pass rate achieved
- [ ] Test report shows all green

---

#### Task 1.5: Manual QA Verification
**Branch**: N/A (testing only)
**Effort**: 5 hours

**Test All User Flows Manually**:
1. **Authentication Flow**:
   - [ ] Registration with email verification
   - [ ] Login/Logout
   - [ ] Password reset
   - [ ] Password change

2. **Character Management**:
   - [ ] Create character
   - [ ] Edit character
   - [ ] View character profile
   - [ ] Edit character custom profile

3. **POKE System Flow** (CRITICAL):
   - [ ] Send POKE to new character (no prior interaction)
   - [ ] Verify cannot send message before POKE
   - [ ] Receive POKE and respond
   - [ ] Verify message unlock after mutual POKE
   - [ ] Verify rate limiting (5 POKEs/day)
   - [ ] Verify cooldown (can't POKE same person for 30 days)
   - [ ] Verify content filtering (no URLs, no emails)

4. **Blocking System**:
   - [ ] Block character
   - [ ] Verify blocked character cannot send POKEs
   - [ ] Verify blocked character cannot send messages
   - [ ] Verify blocked character cannot send friend requests
   - [ ] View blocked list
   - [ ] Unblock character

5. **Messaging System**:
   - [ ] Send message (after POKE unlock)
   - [ ] Receive message
   - [ ] View conversation list
   - [ ] Switch between conversations
   - [ ] See unread indicators
   - [ ] Mark as read when viewing

6. **Identity Reveal**:
   - [ ] Send anonymous message
   - [ ] Reveal identity to character
   - [ ] Verify revealed identity shows in messages
   - [ ] Hide identity
   - [ ] Verify identity hidden again

7. **Friend System**:
   - [ ] Send friend request
   - [ ] Receive friend request
   - [ ] Accept friend request
   - [ ] Decline friend request
   - [ ] View friend list

**Acceptance Criteria**:
- [ ] All flows tested manually
- [ ] No bugs found in critical flows
- [ ] UI/UX issues documented (not blockers)
- [ ] Sign-off from QA/Product Owner

---

## 🟡 SPRINT 2: HIGH - Screenshots & Memories UI
**Priority**: HIGH
**Duration**: 10-12 days
**Effort**: 40-50 hours
**Assignee**: TBD

### Goal
Complete Character Profile features by implementing Screenshots Upload UI and Memories Management UI.

### Context
**Backend is 100% ready**:
- `CharacterProfile` model has `screenshots` JSONField
- `CharacterProfile` model has `memories` JSONField
- API endpoint exists: `/api/v1/character-profiles/`

**What we need**: Frontend UI to interact with these fields.

---

### Task 2.1: Screenshots Upload UI
**Branch**: `feature/screenshots-upload-ui`
**Effort**: 20-25 hours

#### Detailed Specification

**User Story**:
> As a user, I want to upload screenshots from my gaming sessions to my character profile, so other players can see my achievements and memories.

**UI Components Needed**:

1. **Upload Form** (in character profile edit page):
```html
<!-- Location: app/templates/characters/character_profile_edit.html -->

<div class="screenshots-section">
  <h3>Screenshots</h3>

  <!-- Upload Area -->
  <div class="upload-area" id="screenshot-upload">
    <input type="file" id="screenshot-input" accept="image/*" multiple>
    <div class="drag-drop-zone">
      <i class="bi bi-cloud-upload"></i>
      <p>Drag & drop screenshots here or click to browse</p>
      <small>Supports: JPG, PNG, GIF (max 5MB each)</small>
    </div>
  </div>

  <!-- Preview Area -->
  <div class="screenshot-preview-grid" id="preview-grid">
    <!-- Dynamically populated with uploaded images -->
  </div>

  <!-- Existing Screenshots -->
  <div class="existing-screenshots" id="existing-screenshots">
    {% if profile.screenshots %}
      {% for screenshot in profile.screenshots %}
        <div class="screenshot-item" data-screenshot-id="{{ forloop.counter0 }}">
          <img src="{{ screenshot.url }}" alt="{{ screenshot.title }}">
          <div class="screenshot-overlay">
            <input type="text" value="{{ screenshot.title }}" placeholder="Title">
            <textarea placeholder="Description">{{ screenshot.description }}</textarea>
            <button class="btn btn-sm btn-danger delete-screenshot">Delete</button>
          </div>
        </div>
      {% endfor %}
    {% endif %}
  </div>
</div>
```

2. **Gallery Display** (in character detail page):
```html
<!-- Location: app/templates/characters/character_detail_content.html -->

<div class="screenshots-gallery">
  <h3>Screenshots</h3>

  {% if character.profile.screenshots %}
    <div class="gallery-grid">
      {% for screenshot in character.profile.screenshots %}
        <div class="gallery-item" data-bs-toggle="modal" data-bs-target="#screenshot-modal-{{ forloop.counter0 }}">
          <img src="{{ screenshot.thumbnail_url }}" alt="{{ screenshot.title }}">
          <div class="gallery-caption">{{ screenshot.title }}</div>
        </div>

        <!-- Modal for full size -->
        <div class="modal fade" id="screenshot-modal-{{ forloop.counter0 }}">
          <div class="modal-dialog modal-lg">
            <div class="modal-content">
              <div class="modal-header">
                <h5>{{ screenshot.title }}</h5>
                <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
              </div>
              <div class="modal-body">
                <img src="{{ screenshot.url }}" class="img-fluid">
                <p>{{ screenshot.description }}</p>
              </div>
            </div>
          </div>
        </div>
      {% endfor %}
    </div>
  {% else %}
    <p class="text-muted">No screenshots yet.</p>
  {% endif %}
</div>
```

**JavaScript Logic** (`static/js/screenshot-upload.js`):
```javascript
// File upload handling
const uploadInput = document.getElementById('screenshot-input');
const previewGrid = document.getElementById('preview-grid');
let uploadedFiles = [];

uploadInput.addEventListener('change', (e) => {
  const files = Array.from(e.target.files);
  files.forEach(file => handleFileUpload(file));
});

// Drag & drop
const dropZone = document.querySelector('.drag-drop-zone');
dropZone.addEventListener('dragover', (e) => {
  e.preventDefault();
  dropZone.classList.add('drag-over');
});

dropZone.addEventListener('drop', (e) => {
  e.preventDefault();
  dropZone.classList.remove('drag-over');
  const files = Array.from(e.dataTransfer.files);
  files.forEach(file => handleFileUpload(file));
});

function handleFileUpload(file) {
  // Validate file
  if (!file.type.startsWith('image/')) {
    alert('Only images allowed');
    return;
  }
  if (file.size > 5 * 1024 * 1024) {
    alert('File too large (max 5MB)');
    return;
  }

  // Create preview
  const reader = new FileReader();
  reader.onload = (e) => {
    const preview = createPreviewElement(e.target.result, file.name);
    previewGrid.appendChild(preview);
  };
  reader.readAsDataURL(file);

  // Add to upload queue
  uploadedFiles.push(file);
}

function createPreviewElement(dataUrl, filename) {
  const div = document.createElement('div');
  div.className = 'preview-item';
  div.innerHTML = `
    <img src="${dataUrl}">
    <input type="text" placeholder="Title" class="form-control form-control-sm">
    <textarea placeholder="Description" class="form-control form-control-sm"></textarea>
    <button class="btn btn-sm btn-danger remove-preview">Remove</button>
  `;

  div.querySelector('.remove-preview').addEventListener('click', () => {
    div.remove();
    // Remove from uploadedFiles array
  });

  return div;
}

// Form submission
const profileForm = document.querySelector('form');
profileForm.addEventListener('submit', async (e) => {
  e.preventDefault();

  // Upload screenshots to backend
  const formData = new FormData();
  uploadedFiles.forEach((file, index) => {
    formData.append(`screenshot_${index}`, file);
    formData.append(`screenshot_${index}_title`, document.querySelector(`[data-index="${index}"] input`).value);
    formData.append(`screenshot_${index}_desc`, document.querySelector(`[data-index="${index}"] textarea`).value);
  });

  // Send to API
  const response = await fetch('/api/v1/character-profiles/upload-screenshots/', {
    method: 'POST',
    body: formData,
    headers: {
      'X-CSRFToken': getCookie('csrftoken')
    }
  });

  if (response.ok) {
    window.location.reload();
  } else {
    alert('Upload failed');
  }
});
```

**Backend API Endpoint** (add to `app/api_views.py`):
```python
from rest_framework.decorators import action
from rest_framework.response import Response
from django.core.files.storage import default_storage
import uuid

class CharacterProfileViewSet(viewsets.ModelViewSet):
    # ... existing code ...

    @action(detail=True, methods=['post'])
    def upload_screenshots(self, request, pk=None):
        """Upload screenshots to character profile"""
        profile = self.get_object()

        # Ensure user owns this character
        if profile.character.user != request.user:
            return Response({'error': 'Permission denied'}, status=403)

        screenshots = profile.screenshots or []

        # Process uploaded files
        for key, file in request.FILES.items():
            if key.startswith('screenshot_'):
                # Save file
                filename = f"screenshots/{uuid.uuid4()}{os.path.splitext(file.name)[1]}"
                filepath = default_storage.save(filename, file)
                url = default_storage.url(filepath)

                # Get metadata
                index = key.split('_')[1]
                title = request.POST.get(f'screenshot_{index}_title', '')
                description = request.POST.get(f'screenshot_{index}_desc', '')

                # Add to screenshots array
                screenshots.append({
                    'url': url,
                    'thumbnail_url': url,  # TODO: Generate thumbnail
                    'title': title,
                    'description': description,
                    'uploaded_at': timezone.now().isoformat()
                })

        # Save to profile
        profile.screenshots = screenshots
        profile.save()

        return Response({'success': True, 'screenshots': screenshots})

    @action(detail=True, methods=['post'])
    def delete_screenshot(self, request, pk=None):
        """Delete a screenshot from profile"""
        profile = self.get_object()

        if profile.character.user != request.user:
            return Response({'error': 'Permission denied'}, status=403)

        screenshot_index = request.data.get('index')
        if screenshot_index is not None:
            screenshots = profile.screenshots or []
            if 0 <= screenshot_index < len(screenshots):
                deleted = screenshots.pop(screenshot_index)
                # Delete file from storage
                if 'url' in deleted:
                    # Extract filename from URL and delete
                    pass  # TODO: Implement file deletion

                profile.screenshots = screenshots
                profile.save()
                return Response({'success': True})

        return Response({'error': 'Invalid index'}, status=400)
```

**Acceptance Criteria**:
- [ ] Can upload multiple screenshots (drag & drop or file picker)
- [ ] Image preview before upload
- [ ] Can add title and description to each screenshot
- [ ] Can delete screenshots
- [ ] Screenshots displayed in gallery on character detail page
- [ ] Click screenshot opens full-size modal
- [ ] Responsive on mobile
- [ ] E2E test written and passing

**Files to Create/Modify**:
- `app/templates/characters/character_profile_edit.html` - Add upload UI
- `app/templates/characters/character_detail_content.html` - Add gallery
- `static/js/screenshot-upload.js` - Upload logic
- `static/css/screenshot-gallery.css` - Gallery styles
- `app/api_views.py` - Add upload/delete endpoints
- `tests/e2e/characters/character-screenshots.spec.ts` - E2E tests

---

### Task 2.2: Memories Management UI
**Branch**: `feature/memories-management-ui`
**Effort**: 20-25 hours

#### Detailed Specification

**User Story**:
> As a user, I want to record memorable moments from my gaming sessions (achievements, funny moments, epic battles) on my character profile, so I can reminisce and share stories with other players.

**UI Components Needed**:

1. **Memories Timeline** (in character detail page):
```html
<!-- Location: app/templates/characters/character_detail_content.html -->

<div class="memories-section">
  <h3>Memories</h3>

  {% if character.profile.memories %}
    <div class="timeline">
      {% for memory in character.profile.memories|dictsortreversed:"date" %}
        <div class="timeline-item" data-memory-id="{{ forloop.counter0 }}">
          <div class="timeline-marker"></div>
          <div class="timeline-content">
            <div class="timeline-date">{{ memory.date|date:"F d, Y" }}</div>
            <h4>{{ memory.title }}</h4>
            <p>{{ memory.description }}</p>
            {% if memory.screenshot_url %}
              <img src="{{ memory.screenshot_url }}" alt="{{ memory.title }}" class="memory-screenshot">
            {% endif %}
            {% if character.user == request.user %}
              <div class="memory-actions">
                <button class="btn btn-sm btn-outline-primary edit-memory">Edit</button>
                <button class="btn btn-sm btn-outline-danger delete-memory">Delete</button>
              </div>
            {% endif %}
          </div>
        </div>
      {% endfor %}
    </div>
  {% else %}
    <p class="text-muted">No memories recorded yet.</p>
  {% endif %}

  {% if character.user == request.user %}
    <button class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#add-memory-modal">
      <i class="bi bi-plus-circle"></i> Add Memory
    </button>
  {% endif %}
</div>

<!-- Add Memory Modal -->
<div class="modal fade" id="add-memory-modal">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <h5>Add Memory</h5>
        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
      </div>
      <div class="modal-body">
        <form id="add-memory-form">
          <div class="mb-3">
            <label class="form-label">Title *</label>
            <input type="text" class="form-control" name="title" required maxlength="200">
          </div>

          <div class="mb-3">
            <label class="form-label">Date *</label>
            <input type="date" class="form-control" name="date" required>
          </div>

          <div class="mb-3">
            <label class="form-label">Description *</label>
            <textarea class="form-control" name="description" rows="4" required maxlength="1000"></textarea>
          </div>

          <div class="mb-3">
            <label class="form-label">Screenshot (optional)</label>
            <input type="file" class="form-control" name="screenshot" accept="image/*">
            <small class="text-muted">Max 2MB</small>
          </div>

          <div class="mb-3">
            <label class="form-label">Tags (optional)</label>
            <input type="text" class="form-control" name="tags" placeholder="achievement, funny, epic">
            <small class="text-muted">Comma-separated</small>
          </div>
        </form>
      </div>
      <div class="modal-footer">
        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
        <button type="button" class="btn btn-primary" id="save-memory">Save Memory</button>
      </div>
    </div>
  </div>
</div>
```

**JavaScript Logic** (`static/js/memories-manager.js`):
```javascript
// Add memory
document.getElementById('save-memory').addEventListener('click', async () => {
  const form = document.getElementById('add-memory-form');
  const formData = new FormData(form);

  // Validate
  if (!formData.get('title') || !formData.get('date') || !formData.get('description')) {
    alert('Please fill required fields');
    return;
  }

  // Upload screenshot if provided
  let screenshotUrl = null;
  const screenshotFile = formData.get('screenshot');
  if (screenshotFile && screenshotFile.size > 0) {
    screenshotUrl = await uploadMemoryScreenshot(screenshotFile);
  }

  // Create memory object
  const memory = {
    title: formData.get('title'),
    date: formData.get('date'),
    description: formData.get('description'),
    screenshot_url: screenshotUrl,
    tags: formData.get('tags').split(',').map(t => t.trim()).filter(t => t),
    created_at: new Date().toISOString()
  };

  // Send to API
  const response = await fetch(`/api/v1/character-profiles/${profileId}/add-memory/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': getCookie('csrftoken')
    },
    body: JSON.stringify(memory)
  });

  if (response.ok) {
    window.location.reload();
  } else {
    alert('Failed to save memory');
  }
});

// Edit memory
document.querySelectorAll('.edit-memory').forEach(btn => {
  btn.addEventListener('click', (e) => {
    const memoryItem = e.target.closest('.timeline-item');
    const memoryId = memoryItem.dataset.memoryId;
    // Open modal with pre-filled data
    // Similar to add but with existing data
  });
});

// Delete memory
document.querySelectorAll('.delete-memory').forEach(btn => {
  btn.addEventListener('click', async (e) => {
    if (!confirm('Delete this memory?')) return;

    const memoryItem = e.target.closest('.timeline-item');
    const memoryId = memoryItem.dataset.memoryId;

    const response = await fetch(`/api/v1/character-profiles/${profileId}/delete-memory/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCookie('csrftoken')
      },
      body: JSON.stringify({ index: parseInt(memoryId) })
    });

    if (response.ok) {
      memoryItem.remove();
    }
  });
});

async function uploadMemoryScreenshot(file) {
  const formData = new FormData();
  formData.append('screenshot', file);

  const response = await fetch('/api/v1/character-profiles/upload-memory-screenshot/', {
    method: 'POST',
    body: formData,
    headers: {
      'X-CSRFToken': getCookie('csrftoken')
    }
  });

  if (response.ok) {
    const data = await response.json();
    return data.url;
  }
  return null;
}
```

**Backend API Endpoints** (add to `app/api_views.py`):
```python
@action(detail=True, methods=['post'])
def add_memory(self, request, pk=None):
    """Add memory to character profile"""
    profile = self.get_object()

    if profile.character.user != request.user:
        return Response({'error': 'Permission denied'}, status=403)

    memories = profile.memories or []

    # Create memory object
    memory = {
        'title': request.data.get('title'),
        'date': request.data.get('date'),
        'description': request.data.get('description'),
        'screenshot_url': request.data.get('screenshot_url'),
        'tags': request.data.get('tags', []),
        'created_at': timezone.now().isoformat()
    }

    # Validate
    if not all([memory['title'], memory['date'], memory['description']]):
        return Response({'error': 'Missing required fields'}, status=400)

    # Add to memories array (sorted by date, newest first)
    memories.append(memory)
    memories.sort(key=lambda m: m['date'], reverse=True)

    profile.memories = memories
    profile.save()

    return Response({'success': True, 'memory': memory})

@action(detail=True, methods=['post'])
def update_memory(self, request, pk=None):
    """Update existing memory"""
    profile = self.get_object()

    if profile.character.user != request.user:
        return Response({'error': 'Permission denied'}, status=403)

    memory_index = request.data.get('index')
    if memory_index is not None:
        memories = profile.memories or []
        if 0 <= memory_index < len(memories):
            # Update memory
            memories[memory_index].update({
                'title': request.data.get('title'),
                'date': request.data.get('date'),
                'description': request.data.get('description'),
                'screenshot_url': request.data.get('screenshot_url'),
                'tags': request.data.get('tags', []),
                'updated_at': timezone.now().isoformat()
            })

            # Re-sort
            memories.sort(key=lambda m: m['date'], reverse=True)

            profile.memories = memories
            profile.save()
            return Response({'success': True})

    return Response({'error': 'Invalid index'}, status=400)

@action(detail=True, methods=['post'])
def delete_memory(self, request, pk=None):
    """Delete memory from profile"""
    profile = self.get_object()

    if profile.character.user != request.user:
        return Response({'error': 'Permission denied'}, status=403)

    memory_index = request.data.get('index')
    if memory_index is not None:
        memories = profile.memories or []
        if 0 <= memory_index < len(memories):
            deleted = memories.pop(memory_index)
            profile.memories = memories
            profile.save()
            return Response({'success': True})

    return Response({'error': 'Invalid index'}, status=400)
```

**Acceptance Criteria**:
- [ ] Can add new memory with title, date, description
- [ ] Can attach optional screenshot to memory
- [ ] Can add tags to memory
- [ ] Memories displayed in chronological timeline (newest first)
- [ ] Can edit existing memories
- [ ] Can delete memories
- [ ] Timeline responsive on mobile
- [ ] E2E test written and passing

**Files to Create/Modify**:
- `app/templates/characters/character_detail_content.html` - Add timeline
- `static/js/memories-manager.js` - CRUD logic
- `static/css/memories-timeline.css` - Timeline styles
- `app/api_views.py` - Add CRUD endpoints
- `tests/e2e/characters/character-memories.spec.ts` - E2E tests

---

### Task 2.3: E2E Tests for Screenshots & Memories
**Branch**: Same as 2.1/2.2
**Effort**: 5 hours

**Create Tests**:

`tests/e2e/characters/character-screenshots.spec.ts`:
```typescript
test.describe('Character Screenshots', () => {
  test('should upload screenshot', async ({ page }) => {
    // Login as testuser
    // Navigate to character profile edit
    // Upload screenshot file
    // Add title and description
    // Save
    // Verify screenshot appears in gallery
  });

  test('should delete screenshot', async ({ page }) => {
    // ... test deletion
  });
});
```

`tests/e2e/characters/character-memories.spec.ts`:
```typescript
test.describe('Character Memories', () => {
  test('should add memory', async ({ page }) => {
    // Login as testuser
    // Navigate to character detail
    // Click "Add Memory"
    // Fill form
    // Save
    // Verify memory appears in timeline
  });

  test('should edit memory', async ({ page }) => {
    // ... test editing
  });

  test('should delete memory', async ({ page }) => {
    // ... test deletion
  });
});
```

---

## 🟢 SPRINT 3: MEDIUM - Mobile Responsiveness
**Priority**: MEDIUM
**Duration**: 5-7 days
**Effort**: 20-30 hours
**Assignee**: TBD

### Goal
Ensure all features work perfectly on mobile devices (iOS Safari, Android Chrome).

### Tasks

#### Task 3.1: Mobile Testing Audit
**Branch**: N/A (testing only)
**Effort**: 3 hours

**Test Matrix**:

| Feature | iOS Safari | Android Chrome | Issues Found |
|---------|-----------|----------------|--------------|
| Login/Signup | ⬜ | ⬜ | |
| Navigation | ⬜ | ⬜ | |
| Character List | ⬜ | ⬜ | |
| Character Detail | ⬜ | ⬜ | |
| Send POKE | ⬜ | ⬜ | |
| Messaging | ⬜ | ⬜ | |
| Conversation List | ⬜ | ⬜ | |
| Block Character | ⬜ | ⬜ | |
| Friend Requests | ⬜ | ⬜ | |
| Screenshots Upload | ⬜ | ⬜ | |
| Memories Timeline | ⬜ | ⬜ | |

Document issues in: `docs/testing/MOBILE_ISSUES.md`

---

#### Task 3.2: Fix Mobile Responsiveness Issues
**Branch**: `fix/mobile-responsiveness`
**Effort**: 15-20 hours

Based on issues found in 3.1, fix:
- Navigation collapse on mobile
- Form inputs touch-friendly
- Conversation list collapsible
- Image galleries mobile-optimized
- Modals full-screen on mobile

---

#### Task 3.3: Mobile E2E Tests
**Branch**: `test/mobile-e2e`
**Effort**: 5 hours

Add mobile viewport tests to existing E2E tests:
```typescript
test.use({ viewport: { width: 375, height: 667 } }); // iPhone SE
test.use({ viewport: { width: 390, height: 844 } }); // iPhone 12/13/14
```

---

## 🔵 SPRINT 4+: LOW - Future Enhancements
**Priority**: LOW (Post-MVP)
**Duration**: TBD
**Effort**: TBD

### Tasks (Not Prioritized)

1. Real-time Messaging (WebSocket/SSE)
2. Notification Center
3. Quick Actions Menu
4. Enhanced Search & Discovery
5. Activity Feed
6. Performance Optimization
7. SEO Optimization
8. Migration to Next.js + Cloudflare

**These will be planned after MVP launch.**

---

## 🌳 Task Assignment & Branching Strategy

### Git Branching Model

```
main (production-ready)
  ├── test/verify-e2e-tests
  ├── fix/e2e-test-failures-critical
  │     ├── fix/e2e-login
  │     ├── fix/e2e-poke-send
  │     └── fix/e2e-blocking
  ├── fix/e2e-test-failures-minor
  ├── feature/screenshots-upload-ui
  ├── feature/memories-management-ui
  └── fix/mobile-responsiveness
```

### Branch Naming Convention

- `test/*` - Testing and QA work
- `fix/*` - Bug fixes
- `feature/*` - New features
- `docs/*` - Documentation only
- `chore/*` - Configuration, scripts, etc.

### PR Workflow

1. Create feature branch from `main`
2. Work on task
3. Write E2E tests
4. Self-review code
5. Create PR to `main`
6. Request review (if team exists)
7. Fix review comments
8. Merge to `main`
9. Delete feature branch

### Commit Message Convention

```
<type>: <subject>

<body>

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
```

**Types**: feat, fix, test, docs, chore, refactor, style

---

## 📝 Developer Notes

### Before Starting Any Task

1. Read [CLAUDE.md](CLAUDE.md) for codebase overview
2. Read [Technical Audit](TECHNICAL_AUDIT_2025-12-28.md) for context
3. Check [Project Status](docs/PROJECT_STATUS_SUMMARY.md) for current state
4. Load fixtures: `pnpm load:fixtures`
5. Run Django server: `python manage.py runserver`

### Development Workflow

1. Create branch for task
2. Write failing E2E test (TDD red phase)
3. Implement feature (TDD green phase)
4. Refactor code (TDD refactor phase)
5. Run all tests: `pnpm test:e2e`
6. Manual testing
7. Create PR

### Testing Requirements

- **MANDATORY**: Every feature MUST have E2E test
- **MANDATORY**: All tests must pass before merge
- **MANDATORY**: Load fixtures before testing

### Code Quality

- Follow Django coding style (PEP 8)
- Use class-based views when possible
- Keep business logic in models/utils
- Keep views light (request handling only)
- Use Bootstrap 5 for styling
- Write semantic HTML
- Add comments for complex logic only

---

## 🎯 Success Metrics

### Sprint 1 Success
- [ ] 100% E2E tests passing
- [ ] All critical flows manually verified
- [ ] No blocking bugs

### Sprint 2 Success
- [ ] Screenshots upload/delete/display works
- [ ] Memories CRUD works
- [ ] Timeline displays correctly
- [ ] Mobile responsive

### Sprint 3 Success
- [ ] All features work on iOS Safari
- [ ] All features work on Android Chrome
- [ ] No layout breaking on small screens
- [ ] Touch interactions work properly

### MVP Launch Success
- [ ] All Sprints 1-3 complete
- [ ] 100% E2E test coverage
- [ ] Manual QA sign-off
- [ ] Product Owner approval
- [ ] Ready for production deployment

---

---

## 🤖 CI/CD & GitHub Actions

### GitHub Actions Configured ✅

**Workflows Created**:
1. **`.github/workflows/e2e-tests.yml`** - E2E testing on PR
2. **`.github/workflows/django-ci.yml`** - Django unit tests + linting

**How It Works with Render**:
- **GitHub Actions** = Quality Gate (tests before merge)
- **Render** = Deployment (auto-deploy after merge)
- See: [CI/CD Strategy](docs/CI_CD_STRATEGY.md) for complete explanation

**Features**:
- ✅ Runs on every PR to `main`
- ✅ Tests on 3 browsers (Chromium, Firefox, WebKit)
- ✅ Blocks merge if tests fail
- ✅ Uploads test reports as artifacts
- ✅ Free tier (2000 min/month)

**Branch Protection** (Recommended):
1. Go to GitHub → Settings → Branches
2. Add rule for `main` branch
3. Enable: "Require status checks to pass before merging"
4. Select: `e2e-tests` and `django-tests`
5. Save → Now PRs cannot merge if tests fail

---

**Last Updated**: 2025-12-28
**Maintained By**: Technical Project Manager (Claude Code)
**Questions**: See [Technical Audit - Questions Section](TECHNICAL_AUDIT_2025-12-28.md#-pytania-jako-project-manager-do-zespołu-dev)
**CI/CD Strategy**: See [CI/CD Strategy](docs/CI_CD_STRATEGY.md)

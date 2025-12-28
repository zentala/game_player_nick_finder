# E2E Test Strategy - Identyfikacja i Naprawa Błędów
## Game Player Nick Finder

**Data**: 2025-12-28
**Status**: PLANNING PHASE
**Cel**: Strategia identyfikacji, priorytetyzacji i naprawy błędów E2E

---

## 📋 Faza 1: IDENTYFIKACJA - Discovery Phase

### Krok 1.1: Przygotowanie Środowiska (30 min)

**Checklist**:
```bash
# 1. Fresh database reset
rm db.sqlite3
python manage.py migrate

# 2. Load fixtures
pnpm load:fixtures

# 3. Verify data loaded
python manage.py shell
>>> from app.models import CustomUser, Character, Message, Poke
>>> print(f"Users: {CustomUser.objects.count()}")
>>> print(f"Characters: {Character.objects.count()}")
>>> print(f"Messages: {Message.objects.count()}")
>>> print(f"POKEs: {Poke.objects.count()}")
>>> exit()

# 4. Start Django server
python manage.py runserver

# 5. Open new terminal for tests
```

**Expected Output**:
- Users: 3+ (testuser, otheruser, privateuser)
- Characters: 5+ (test characters)
- Messages: 0 initially
- POKEs: 0 initially

---

### Krok 1.2: Uruchomienie Wszystkich Testów z Raportowaniem (2h)

**Command**:
```bash
# Run ALL tests with detailed output
pnpm test:e2e --reporter=html --reporter=list

# Or run by category to identify patterns
pnpm test:e2e tests/e2e/auth/ --reporter=list
pnpm test:e2e tests/e2e/characters/ --reporter=list
pnpm test:e2e tests/e2e/friends/ --reporter=list
pnpm test:e2e tests/e2e/profile/ --reporter=list
pnpm test:e2e tests/e2e/blocking/ --reporter=list
pnpm test:e2e tests/e2e/pokes/ --reporter=list
pnpm test:e2e tests/e2e/messaging/ --reporter=list
pnpm test:e2e tests/e2e/navigation/ --reporter=list
```

**Document Results in**: `docs/testing/E2E_RESULTS_INITIAL.md`

**Template**:
```markdown
# Initial E2E Test Results - 2025-12-28

## Environment
- Django Server: ✅ Running on localhost:8000
- Fixtures: ✅ Loaded
- Browser: Chromium (Playwright default)

## Summary Statistics
| Category | Total | Pass | Fail | Skip | Pass Rate |
|----------|-------|------|------|------|-----------|
| Authentication (5) | 5 | X | Y | Z | XX% |
| Characters (2) | 2 | X | Y | Z | XX% |
| Friends (3) | 3 | X | Y | Z | XX% |
| Profile (2) | 2 | X | Y | Z | XX% |
| Blocking (4) | 4 | X | Y | Z | XX% |
| POKEs (4) | 4 | X | Y | Z | XX% |
| Messaging (1) | 1 | X | Y | Z | XX% |
| Navigation (3) | 3 | X | Y | Z | XX% |
| **TOTAL** | **24** | **X** | **Y** | **Z** | **XX%** |

## Detailed Results

### ✅ Passing Tests
1. [test-name] - PASS - [notes if any]

### ❌ Failing Tests (Categorized by Error Type)

#### Error Type: "Element not found" / Timeout
- [ ] test-name-1 - Expected: X, Got: timeout
- [ ] test-name-2 - Expected: Y, Got: element not visible

#### Error Type: "Assertion failed" / Wrong value
- [ ] test-name-3 - Expected: "Success", Got: "Error"
- [ ] test-name-4 - Expected: 5 items, Got: 0 items

#### Error Type: "Navigation failed" / URL mismatch
- [ ] test-name-5 - Expected URL: /success, Actual: /error

#### Error Type: "Database state" / Data missing
- [ ] test-name-6 - Expected user to exist, not found

[... continue for all failures]
```

---

### Krok 1.3: Kategoryzacja Błędów (1h)

**Analiza Patterns**:

1. **Grupuj błędy po typie**:
   - Timeout errors (element nie pojawia się)
   - Assertion errors (złe dane)
   - Navigation errors (złe URL)
   - Database errors (brak danych)
   - Authentication errors (login fails)

2. **Identyfikuj powtarzalne problemy**:
   - Czy ten sam błąd występuje w wielu testach?
   - Czy to problem fixture vs problem w kodzie?
   - Czy to problem timing (async) czy logika?

**Output**: `docs/testing/E2E_ERROR_PATTERNS.md`

**Template**:
```markdown
# E2E Error Patterns Analysis

## Pattern 1: Fixture Data Missing
**Tests Affected**: 8 tests
**Root Cause**: Fixtures nie mają POKEs, więc testy zakładające istniejące POKEs failują
**Solution**: Dodać POKEs do fixtures OR adjust tests to create POKEs
**Priority**: CRITICAL (blocks 8 tests)

## Pattern 2: Timing Issues (Async)
**Tests Affected**: 5 tests
**Root Cause**: Page transitions nie czekają na full load
**Solution**: Add explicit waits: `await page.waitForSelector()`
**Priority**: HIGH (intermittent failures)

## Pattern 3: URL Mismatch After Actions
**Tests Affected**: 3 tests
**Root Cause**: Django redirects nie są prawidłowe
**Solution**: Fix view redirects in views.py
**Priority**: MEDIUM (UX issue but tests reveal bugs)

[... continue for all patterns]
```

---

## 📊 Faza 2: PRIORYTETYZACJA - Triage Phase

### Framework Priorytetyzacji

**Impact Matrix**:

| Priority | Criteria | Example |
|----------|----------|---------|
| **P0 - CRITICAL** | Blocks core user flow, affects MVP | Login fails, POKE send fails, message send fails |
| **P1 - HIGH** | Breaks important feature, but workaround exists | Friend request fails, block doesn't work |
| **P2 - MEDIUM** | UX issue, doesn't break flow | Wrong redirect, slow page load |
| **P3 - LOW** | Nice-to-have, cosmetic | Typo in error message, missing icon |

**Severity x Frequency Matrix**:

```
         │ Affects 1 Test │ Affects 2-5 Tests │ Affects 6+ Tests
─────────┼────────────────┼───────────────────┼──────────────────
CRITICAL │      P1        │        P0         │       P0
HIGH     │      P2        │        P1         │       P1
MEDIUM   │      P3        │        P2         │       P2
LOW      │      P3        │        P3         │       P3
```

**Decision Tree**:
```
Błąd występuje?
├─ Czy blokuje login/POKE/messaging? → P0 (Critical)
├─ Czy dotyczy core feature (friends/blocking)? → P1 (High)
├─ Czy to UX/redirect issue? → P2 (Medium)
└─ Czy to cosmetic/minor? → P3 (Low)
```

---

### Krok 2.1: Przypisanie Priorytetów (1h)

**Process**:
1. Dla każdego failing test określ:
   - Severity (Critical/High/Medium/Low)
   - Frequency (How many tests affected by same root cause?)
   - Impact (Blocks MVP? Blocks user flow?)

2. Assign Priority (P0/P1/P2/P3)

**Output**: `docs/testing/E2E_PRIORITIZED_BACKLOG.md`

**Template**:
```markdown
# E2E Test Fixes - Prioritized Backlog

## P0 - CRITICAL (Fix Immediately - Sprint 1.1)

### Fix 1: Login Authentication Fails
- **Tests Affected**: 5 (all auth tests)
- **Root Cause**: Session cookie not persisting
- **Impact**: Blocks ALL tests that require login (24 tests total)
- **Estimate**: 4 hours
- **Blocker**: YES - must fix first

### Fix 2: POKE Send Fails
- **Tests Affected**: 4 (all POKE tests)
- **Root Cause**: `can_send_poke()` returns False (rate limit or validation issue)
- **Impact**: Blocks messaging unlock flow
- **Estimate**: 3 hours
- **Blocker**: YES

## P1 - HIGH (Fix Next - Sprint 1.2)

### Fix 3: Friend Request Not Sending
- **Tests Affected**: 3 (friend request tests)
- **Root Cause**: CSRF token missing in AJAX request
- **Impact**: Friend system unusable
- **Estimate**: 2 hours
- **Blocker**: NO (workaround: manual refresh)

[... continue]

## P2 - MEDIUM (Fix Later - Sprint 1.3)

## P3 - LOW (Fix Last or Defer)
```

---

### Krok 2.2: Utworzenie Sprint Backlogs (30 min)

**Breakdown**:

```
Sprint 1.1: P0 CRITICAL Fixes (Week 1, Days 1-3)
├── Fix 1: Login Authentication (4h)
├── Fix 2: POKE Send (3h)
├── Fix 3: Message Send After POKE (2h)
└── Verify: Re-run affected tests (2h)
TOTAL: 11 hours (1.5 days)

Sprint 1.2: P1 HIGH Fixes (Week 1, Days 4-5)
├── Fix 4: Friend Request Send (2h)
├── Fix 5: Block Character (2h)
├── Fix 6: Conversation List Display (3h)
└── Verify: Re-run affected tests (2h)
TOTAL: 9 hours (1 day)

Sprint 1.3: P2 MEDIUM Fixes (Week 2, Days 1-2)
├── Fix 7: Wrong Redirects (4h)
├── Fix 8: Timing Issues (3h)
└── Verify: Re-run all tests (2h)
TOTAL: 9 hours (1 day)

Sprint 1.4: P3 LOW Fixes (Week 2, Day 3)
├── Fix minor UX issues (4h)
└── Final verification (2h)
TOTAL: 6 hours (0.75 day)

Sprint 1.5: Full Regression (Week 2, Day 4)
├── Run ALL 24 tests 3 times (3h)
├── Manual QA of critical flows (4h)
└── Documentation update (1h)
TOTAL: 8 hours (1 day)
```

**Total Sprint 1**: ~43 hours (~5-6 days, 1 developer)

---

## 🔧 Faza 3: EXECUTION - Fix Phase

### Krok 3.1: Setup Git Branching

```bash
# Main branch for all Sprint 1 work
git checkout -b test/e2e-fixes-sprint-1

# Sub-branches for each priority group
git checkout -b fix/p0-critical-fixes    # From test/e2e-fixes-sprint-1
git checkout -b fix/p1-high-fixes        # From test/e2e-fixes-sprint-1
git checkout -b fix/p2-medium-fixes      # From test/e2e-fixes-sprint-1
git checkout -b fix/p3-low-fixes         # From test/e2e-fixes-sprint-1
```

---

### Krok 3.2: Fix Template (For Each Bug)

**Branch**: `fix/p0-[bug-name]` (sub-branch of `fix/p0-critical-fixes`)

**Process**:
1. **Reproduce**:
   ```bash
   # Run specific test to reproduce
   pnpm test:e2e tests/e2e/auth/login.spec.ts
   ```

2. **Diagnose**:
   - Add console.logs in code
   - Check Django logs: `python manage.py runserver` output
   - Check browser console: Playwright opens browser with `--headed` flag
   - Check database state: `python manage.py shell`

3. **Fix**:
   - Edit code (views.py, models.py, templates, etc.)
   - Test manually first: Open http://localhost:8000 in browser
   - Verify fix works manually

4. **Test**:
   ```bash
   # Re-run specific test
   pnpm test:e2e tests/e2e/auth/login.spec.ts
   # Should pass now
   ```

5. **Commit**:
   ```bash
   git add [files]
   git commit -m "fix(auth): [what was fixed]

   - Root cause: [explain]
   - Solution: [explain]
   - Tests affected: [list]
   - Verified: Test now passes

   Fixes #[issue-number]"
   ```

6. **Merge up**:
   ```bash
   git checkout fix/p0-critical-fixes
   git merge fix/p0-[bug-name]
   ```

---

### Krok 3.3: Daily Progress Tracking

**Use**: `docs/testing/E2E_DAILY_PROGRESS.md`

**Template**:
```markdown
# E2E Fixes - Daily Progress

## Day 1 - 2025-12-29 (Sprint 1.1 - P0 Critical)

### Planned
- [ ] Fix 1: Login Authentication (4h)
- [ ] Fix 2: POKE Send (3h)

### Actual
- [x] Fix 1: Login Authentication (5h) - DONE
  - Root cause: Session cookie domain mismatch
  - Solution: Updated settings.SESSION_COOKIE_DOMAIN
  - Tests passing: 5/5 auth tests ✅
- [ ] Fix 2: POKE Send (in progress)
  - Diagnosed: Rate limit validation too strict
  - Working on: Relaxing validation for test environment

### Blockers
- None

### Tomorrow
- Complete Fix 2
- Start Fix 3

## Day 2 - 2025-12-30

[... continue]
```

---

## 🎯 Faza 4: VERIFICATION - QA Phase

### Krok 4.1: Regression Testing (After Each Sprint)

**After Sprint 1.1 (P0 fixes)**:
```bash
# Run ALL tests to verify no regressions
pnpm test:e2e

# Expected:
# - All P0 tests: PASS
# - Other tests: May still fail (not fixed yet)
```

**After Sprint 1.2 (P1 fixes)**:
```bash
pnpm test:e2e
# Expected:
# - All P0 + P1 tests: PASS
# - P2/P3 may still fail
```

**After Sprint 1.5 (All fixes)**:
```bash
# Run 3 times to catch flaky tests
pnpm test:e2e --repeat-each=3

# Expected: 100% pass rate, all 24 tests, all 3 runs
```

---

### Krok 4.2: Manual QA Checklist

**Critical User Flows** (Test manually after all fixes):

```markdown
## Flow 1: Registration → Character Creation → POKE → Message
- [ ] Register new account
- [ ] Verify email (check console for verification link)
- [ ] Create character
- [ ] Find another character
- [ ] Send POKE
- [ ] Other user receives POKE
- [ ] Other user responds to POKE
- [ ] Both can now message
- [ ] Send message
- [ ] Receive message
- [ ] See unread indicator
- [ ] Conversation list works

## Flow 2: Blocking Flow
- [ ] Block a character
- [ ] Verify cannot send POKE to blocked
- [ ] Verify cannot send message to blocked
- [ ] Verify cannot send friend request to blocked
- [ ] Unblock character
- [ ] Verify can interact again

## Flow 3: Friend Request Flow
- [ ] Send friend request
- [ ] Receive notification
- [ ] Accept friend request
- [ ] See in friend list
- [ ] View friend's profile

[... all critical flows from TASKS.md]
```

---

## 📈 Success Metrics

### Sprint 1.1 Success
- [ ] All P0 tests passing (expected: ~5-10 tests)
- [ ] Login works 100%
- [ ] POKE system works 100%
- [ ] Message unlock works 100%

### Sprint 1.2 Success
- [ ] All P0 + P1 tests passing (expected: ~15-18 tests)
- [ ] Friend requests work
- [ ] Blocking works
- [ ] Conversation list works

### Sprint 1.3 Success
- [ ] All P0 + P1 + P2 tests passing (expected: ~20-22 tests)
- [ ] No wrong redirects
- [ ] No timing issues

### Sprint 1.5 Final Success
- [ ] **100% pass rate** (24/24 tests)
- [ ] **3 consecutive runs** all pass (no flaky tests)
- [ ] **Manual QA** all critical flows verified
- [ ] **No regressions** in existing features
- [ ] **Ready for MVP**

---

## 🚨 Escalation Rules

**If stuck on a bug > 4 hours**:
1. Document what you tried
2. Create detailed bug report with:
   - Steps to reproduce
   - Expected vs actual behavior
   - Screenshots/videos
   - Logs (Django + browser console)
3. Ask for help (PM, senior dev, or pause and move to next bug)

**If pass rate < 50% after Sprint 1.1**:
- STOP and reassess
- May indicate fundamental issue (fixtures, environment, etc.)
- Re-evaluate strategy

**If pass rate < 80% after Sprint 1.3**:
- Consider deferring P3 fixes to post-MVP
- Focus on critical flows only

---

## 📝 Documentation Updates

**After Sprint 1 Complete**:
- [ ] Update TASKS.md with actual effort vs estimated
- [ ] Update PROJECT_STATUS_SUMMARY.md: "Tests: ✅ 24/24 passing"
- [ ] Create `docs/testing/E2E_FIXES_RETROSPECTIVE.md`
- [ ] Document lessons learned
- [ ] Update fixture documentation if changed

---

**Strategy Owner**: Technical Project Manager (Claude Code)
**Last Updated**: 2025-12-28
**Status**: READY FOR EXECUTION

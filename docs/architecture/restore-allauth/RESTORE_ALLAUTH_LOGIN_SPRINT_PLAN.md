# Epic: Przywrócenie Allauth Login - Plan Sprintów

**Epic ID**: EPIC-001  
**Nazwa**: Restore Allauth Login System  
**Status**: Planning  
**Priority**: High  
**Owner**: Senior Software Architect

---

## 📊 OVERVIEW

**Cel**: Przywrócenie allauth jako jedynego systemu logowania, usunięcie standardowego Django login i aktualizacja wszystkich testów E2E.

**Zespół**: 4 Senior Developers (2 grupy po 2 osoby) + Scrum Master  
**Sprinty**: 2 równoległe sprints (można pracować równocześnie)  
**Metodologia**: Scrum z równoległą pracą agentów

---

## 🏗️ EPIC BREAKDOWN

```
EPIC-001: Restore Allauth Login System
├── SPRINT-1: Backend Implementation (Group A)
│   ├── TASK-1.1: Remove CustomLoginView
│   ├── TASK-1.2: Restore Allauth URLs
│   ├── TASK-1.3: Verify Allauth Settings
│   └── TASK-1.4: Remove Django Login Template
│
└── SPRINT-2: E2E Tests Update (Group B)
    ├── TASK-2.1: Update auth-helpers.ts
    ├── TASK-2.2: Update login.spec.ts
    ├── TASK-2.3: Update other auth tests
    └── TASK-2.4: Run Full Test Suite
```

---

## 👥 TEAM STRUCTURE

### Group A (Backend Sprint)
- **Agent 1**: Senior Backend Developer
- **Agent 2**: Senior Backend Developer
- **Scrum Master**: Coordinates sprint, reviews PRs

### Group B (Frontend/QA Sprint)
- **Agent 3**: Senior Frontend/QA Developer
- **Agent 4**: Senior Frontend/QA Developer
- **Scrum Master**: Coordinates sprint, reviews PRs

**Workflow**:
- Każda grupa pracuje niezależnie nad swoim sprintem
- Commitowanie: każdy agent commituje tylko swoje zmiany
- Code Review: wzajemne sprawdzanie w obrębie grupy
- Integration: po zakończeniu sprintów, merge do dev

---

## 🚀 SPRINT-1: Backend Implementation

**Sprint ID**: SPRINT-1  
**Group**: Group A (Agent 1, Agent 2)  
**Duration**: 1 sprint  
**Priority**: P0 (Must be done first - testy zależne od backendu)

**Goal**: Przywrócenie allauth w backendzie, usunięcie CustomLoginView i standardowego Django login.

---

### TASK-1.1: Remove CustomLoginView

**Assigned to**: Agent 1  
**Story Points**: 2  
**Priority**: P0  
**Dependencies**: None  
**Status**: TODO

**Description**:
Usunięcie klasy `CustomLoginView` i wszystkich związanych z nią importów.

**Acceptance Criteria**:
- [ ] Klasa `CustomLoginView` usunięta z `app/views.py` (linie 1879-1887)
- [ ] Import `from django.contrib.auth.views import LoginView as DjangoLoginView` usunięty z `app/views.py`
- [ ] Import `CustomLoginView` usunięty z `game_player_nick_finder/urls.py`
- [ ] Aplikacja uruchamia się bez błędów importu
- [ ] Brak referencji do `CustomLoginView` w kodzie (sprawdzić grep)

**Files to modify**:
- `app/views.py`
- `game_player_nick_finder/urls.py`

**Testing**:
- [ ] Django app starts without errors
- [ ] No import errors in console
- [ ] Grep search shows no remaining references to CustomLoginView

**Commit message**: `refactor: remove CustomLoginView class and imports`

---

### TASK-1.2: Restore Allauth URLs

**Assigned to**: Agent 1  
**Story Points**: 3  
**Priority**: P0  
**Dependencies**: TASK-1.1 (must remove CustomLoginView first)  
**Status**: TODO

**Description**:
Odkomentowanie allauth URLs i usunięcie override `/accounts/login/` z CustomLoginView.

**Acceptance Criteria**:
- [ ] `path('accounts/', include('allauth.urls'))` jest odkomentowane w `urls.py`
- [ ] Komentarz `# DISABLED: allauth conflicts with django.contrib.auth` usunięty
- [ ] Linia `path('accounts/login/', CustomLoginView.as_view(), name='login')` usunięta
- [ ] Allauth URLs są aktywny przed `django.contrib.auth.urls`
- [ ] Aplikacja uruchamia się bez błędów URL conflicts
- [ ] `/accounts/login/` prowadzi do allauth login page

**Files to modify**:
- `game_player_nick_finder/urls.py`

**Order of operations**:
1. Najpierw usunąć CustomLoginView override (z TASK-1.1)
2. Potem odkomentować `allauth.urls`
3. Sprawdzić kolejność URL patterns (allauth przed django.contrib.auth)

**Testing**:
- [ ] Django app starts without errors
- [ ] `/accounts/login/` returns allauth login page (200 OK)
- [ ] No URL conflicts in Django logs
- [ ] Login page uses template `account/login.html`

**Commit message**: `feat: restore allauth URLs configuration`

---

### TASK-1.3: Verify Allauth Settings

**Assigned to**: Agent 2  
**Story Points**: 2  
**Priority**: P0  
**Dependencies**: None (can be done in parallel with TASK-1.1)  
**Status**: TODO

**Description**:
Weryfikacja że wszystkie wymagane allauth settings są skonfigurowane poprawnie.

**Acceptance Criteria**:
- [ ] `allauth` w INSTALLED_APPS (linia 17)
- [ ] `allauth.account` w INSTALLED_APPS (linia 18)
- [ ] `allauth.socialaccount` w INSTALLED_APPS (linia 19)
- [ ] `allauth.account.middleware.AccountMiddleware` w MIDDLEWARE (linia 45)
- [ ] `allauth.account.auth_backends.AuthenticationBackend` w AUTHENTICATION_BACKENDS (linia 105)
- [ ] `ACCOUNT_EMAIL_VERIFICATION = 'none'` (linia 117)
- [ ] `ACCOUNT_AUTHENTICATION_METHOD = 'username_email'` (linia 118)
- [ ] `LOGIN_REDIRECT_URL = '/'` (linia 109)
- [ ] `LOGIN_URL = '/accounts/login/'` (linia 110)
- [ ] Template `account/base_display.html` istnieje
- [ ] Brak błędów konfiguracji przy starcie Django

**Files to verify**:
- `game_player_nick_finder/settings/base.py`
- `app/templates/account/base_display.html`

**Testing**:
- [ ] Django app starts without configuration errors
- [ ] Allauth middleware is active
- [ ] Authentication backend is configured correctly
- [ ] Template exists and is accessible

**Notes**:
- Jeśli coś brakuje, dodać/zmienić w settings
- Jeśli template brakuje, stworzyć lub zgłosić jako blocker

**Commit message**: `chore: verify and document allauth settings configuration`

---

### TASK-1.4: Remove Django Login Template

**Assigned to**: Agent 2  
**Story Points**: 1  
**Priority**: P0  
**Dependencies**: TASK-1.2 (must restore allauth first to ensure it works)  
**Status**: TODO

**Description**:
Usunięcie nieużywanego template `registration/login.html` po przywróceniu allauth.

**Acceptance Criteria**:
- [ ] Plik `app/templates/registration/login.html` usunięty
- [ ] Brak referencji do `registration/login.html` w kodzie (sprawdzić grep)
- [ ] Brak broken imports/urls po usunięciu
- [ ] Allauth login page działa poprawnie

**Files to delete**:
- `app/templates/registration/login.html`

**Files to check for references**:
- `app/views.py` (sprawdzić grep)
- `game_player_nick_finder/urls.py` (sprawdzić grep)
- Documentation files (can be left for history)

**Testing**:
- [ ] File deleted from filesystem
- [ ] Grep shows no references to `registration/login.html`
- [ ] Login page still works (uses `account/login.html`)

**Commit message**: `refactor: remove unused registration/login.html template`

---

## 🧪 SPRINT-2: E2E Tests Update

**Sprint ID**: SPRINT-2  
**Group**: Group B (Agent 3, Agent 4)  
**Duration**: 1 sprint  
**Priority**: P0 (Can start after SPRINT-1 TASK-1.2 is complete)

**Goal**: Aktualizacja wszystkich testów E2E do allauth - zmiana selektorów z `#id_username` na `#id_login`.

**Dependency**: 
- **BLOCKED BY**: SPRINT-1 TASK-1.2 (Allauth URLs must be restored first)
- **Can start when**: Allauth login page is accessible at `/accounts/login/`

---

### TASK-2.1: Update auth-helpers.ts

**Assigned to**: Agent 3  
**Story Points**: 3  
**Priority**: P0  
**Dependencies**: SPRINT-1 TASK-1.2 (must have allauth working)  
**Status**: TODO

**Description**:
Aktualizacja selektorów w `auth-helpers.ts` z `#id_username` na `#id_login` i usunięcie komentarzy o CustomLoginView.

**Acceptance Criteria**:
- [ ] Wszystkie `#id_username` zamienione na `#id_login` w `auth-helpers.ts`
- [ ] Komentarze o CustomLoginView usunięte
- [ ] Komentarze zaktualizowane do allauth (account_login, LoginForm)
- [ ] Helper funkcja `login()` działa poprawnie
- [ ] Wszystkie selektory używają `#id_login`

**Files to modify**:
- `tests/helpers/auth-helpers.ts`

**Changes required**:
```typescript
// BEFORE:
await expect(page.locator('#id_username')).toBeVisible({ timeout: 5000 });
await page.fill('#id_username', username);
// Comment: CustomLoginView uses Django AuthenticationForm (username field)

// AFTER:
await expect(page.locator('#id_login')).toBeVisible({ timeout: 5000 });
await page.fill('#id_login', username);
// Comment: Allauth LoginForm uses login field (can be username or email)
```

**Testing**:
- [ ] Helper function works in manual test
- [ ] Login helper successfully logs in test user
- [ ] No TypeScript/ESLint errors
- [ ] All selectors updated correctly

**Commit message**: `test: update auth-helpers.ts to use allauth selectors (#id_login)`

---

### TASK-2.2: Update login.spec.ts

**Assigned to**: Agent 3  
**Story Points**: 5  
**Priority**: P0  
**Dependencies**: TASK-2.1 (auth-helpers must be updated first)  
**Status**: TODO

**Description**:
Aktualizacja wszystkich selektorów w `login.spec.ts` do allauth - zmiana `#id_username` na `#id_login`.

**Acceptance Criteria**:
- [ ] Wszystkie `#id_username` zamienione na `#id_login` w `login.spec.ts`
- [ ] Wszystkie `input[name="username"]` zamienione na `input[name="login"]`
- [ ] Form selector `form.login` działa poprawnie (allauth używa `class="login"`)
- [ ] Test "Remember me" używa `#id_remember` (sprawdzić w template)
- [ ] Test "redirect logged in user" działa poprawnie (allauth ma redirect domyślnie)
- [ ] **Wszystkie testy w login.spec.ts przechodzą (100%)**

**Files to modify**:
- `tests/e2e/auth/login.spec.ts`

**Changes required**:
```typescript
// BEFORE:
await expect(page.locator('#id_username')).toBeVisible();
await page.fill('#id_username', TEST_USERS.main.username);

// AFTER:
await expect(page.locator('#id_login')).toBeVisible();
await page.fill('#id_login', TEST_USERS.main.username);
```

**Test cases to verify**:
- [ ] "should display login form with all required elements"
- [ ] "should successfully login with valid credentials"
- [ ] "should fail login with invalid username"
- [ ] "should fail login with invalid password"
- [ ] "should fail login with empty fields"
- [ ] "should redirect to originally requested page after login"
- [ ] "should login with 'Remember me' checkbox if available"
- [ ] "should redirect logged in user away from login page"

**Testing**:
- [ ] Run: `npm run test:e2e tests/e2e/auth/login.spec.ts`
- [ ] All 8 tests pass (100%)
- [ ] No timeout errors
- [ ] No selector errors

**Commit message**: `test: update login.spec.ts to use allauth selectors (#id_login)`

---

### TASK-2.3: Update Other Auth Tests

**Assigned to**: Agent 4  
**Story Points**: 5  
**Priority**: P0  
**Dependencies**: TASK-2.1 (auth-helpers must be updated first)  
**Status**: TODO

**Description**:
Aktualizacja pozostałych testów auth do allauth URL names i selektorów.

**Acceptance Criteria**:
- [ ] `password-reset.spec.ts`: używa `account_reset_password` URL name
- [ ] `password-change.spec.ts`: używa `account_change_password` URL name
- [ ] `signup.spec.ts`: link "Log in" prowadzi do `/accounts/login/` (allauth)
- [ ] `logout.spec.ts`: używa `account_logout` URL name (jeśli potrzebne)
- [ ] `navbar-unauthenticated.spec.ts`: link "Log in" prowadzi do `/accounts/login/`
- [ ] `navbar-authenticated.spec.ts`: logout używa `account_logout`
- [ ] **Wszystkie zaktualizowane testy przechodzą**

**Files to modify**:
- `tests/e2e/auth/password-reset.spec.ts` (jeśli potrzeba)
- `tests/e2e/auth/password-change.spec.ts` (jeśli potrzeba)
- `tests/e2e/auth/signup.spec.ts` (jeśli potrzeba)
- `tests/e2e/auth/logout.spec.ts` (jeśli potrzeba)
- `tests/e2e/navigation/navbar-unauthenticated.spec.ts` (jeśli potrzeba)
- `tests/e2e/navigation/navbar-authenticated.spec.ts` (jeśli potrzeba)

**Changes required**:
- Sprawdzić czy testy używają URL names: `account_reset_password`, `account_change_password`, `account_logout`
- Sprawdzić czy linki prowadzą do właściwych URLi
- Zaktualizować selektory jeśli używają `#id_username`

**Testing**:
- [ ] Run each test file individually to verify
- [ ] All modified tests pass
- [ ] No broken URL references
- [ ] No selector errors

**Commit message**: `test: update auth tests to use allauth URL names and selectors`

---

### TASK-2.4: Run Full Test Suite and Fix Issues

**Assigned to**: Agent 4  
**Story Points**: 5  
**Priority**: P0  
**Dependencies**: TASK-2.2, TASK-2.3 (all test updates must be complete)  
**Status**: TODO

**Description**:
Uruchomienie pełnej suity testów E2E i naprawienie wszystkich błędów związanych z allauth.

**Acceptance Criteria**:
- [ ] Pełna suita testów E2E uruchomiona: `npm run test:e2e`
- [ ] Wszystkie auth-related testy przechodzą (100%):
  - `auth/login.spec.ts`
  - `auth/logout.spec.ts`
  - `auth/password-change.spec.ts`
  - `auth/password-reset.spec.ts`
  - `auth/signup.spec.ts`
  - `navigation/*.spec.ts`
- [ ] Brak błędów związanych z selektorami `#id_username`
- [ ] Brak błędów związanych z URL names (`login` vs `account_login`)
- [ ] Brak regresji w innych testach (non-auth tests)
- [ ] Test results documented

**Files to check**:
- All test files in `tests/e2e/`

**Testing**:
- [ ] Run: `npm run test:e2e`
- [ ] Check test results
- [ ] Fix any remaining issues
- [ ] Verify no regressions in other tests
- [ ] Document test results

**Issues to watch for**:
- Selector errors: `#id_username` not found → should use `#id_login`
- URL errors: `login` not found → should use `account_login`
- Template errors: wrong template → should use `account/login.html`

**Commit message**: `test: fix all E2E tests after allauth migration, all auth tests passing`

---

## 📋 PARALLEL WORK COORDINATION

### Sprint Dependencies

```
SPRINT-1 (Backend)                SPRINT-2 (Tests)
├── TASK-1.1 (Agent 1)           │
├── TASK-1.3 (Agent 2) ──┐       │
├── TASK-1.2 (Agent 1) ──┼───────┼──> TASK-2.1 (Agent 3) ──┐
└── TASK-1.4 (Agent 2)   │       │                          │
                          │       │                          ├──> TASK-2.2 (Agent 3)
                          │       │                          │
                          │       ├──> TASK-2.3 (Agent 4) ──┤
                          │       │                          │
                          │       └──> TASK-2.4 (Agent 4) ──┘
                          │
                          └──> Must complete before SPRINT-2 starts
```

### Workflow Rules

1. **SPRINT-1 must start first** (backend changes)
2. **SPRINT-2 can start** when SPRINT-1 TASK-1.2 is complete (allauth URLs restored)
3. **Within SPRINT-1**: Tasks 1.1 and 1.3 can be done in parallel
4. **Within SPRINT-2**: Tasks 2.1 must be done before 2.2 and 2.3
5. **All tasks**: Can commit independently, but must coordinate through PRs

---

## 🔄 CODE REVIEW PROCESS

### Within Group Review

**Group A (Backend)**:
- Agent 1 reviews Agent 2's PRs
- Agent 2 reviews Agent 1's PRs
- Scrum Master reviews all PRs before merge

**Group B (Tests)**:
- Agent 3 reviews Agent 4's PRs
- Agent 4 reviews Agent 3's PRs
- Scrum Master reviews all PRs before merge

### Cross-Group Review

- After SPRINT-1 completion: Group B reviews backend changes
- After SPRINT-2 completion: Group A reviews test changes
- Final integration: Both groups review final merge

---

## 📝 COMMIT GUIDELINES

### Commit Rules

1. **Each agent commits only their own changes**
2. **One task = one or more commits** (as needed)
3. **Commit messages must follow format**: `type: description`
   - `refactor:` for removing code
   - `feat:` for adding/restoring features
   - `test:` for test changes
   - `chore:` for configuration/verification

### Branch Strategy

**Each group uses separate branch**:
- Group A: `feature/restore-allauth-backend`
- Group B: `feature/restore-allauth-tests`

**Merge strategy**:
1. Group A merges to `dev` after SPRINT-1 completion
2. Group B merges to `dev` after SPRINT-2 completion
3. Both groups verify integration works

---

## ✅ SPRINT COMPLETION CRITERIA

### SPRINT-1 Complete When:
- [ ] All tasks 1.1-1.4 completed
- [ ] All acceptance criteria met
- [ ] All code reviewed and approved
- [ ] All PRs merged to `dev`
- [ ] Allauth login page accessible at `/accounts/login/`
- [ ] No backend errors
- [ ] Manual test: Login works with allauth

### SPRINT-2 Complete When:
- [ ] All tasks 2.1-2.4 completed
- [ ] All acceptance criteria met
- [ ] All code reviewed and approved
- [ ] All PRs merged to `dev`
- [ ] All auth-related E2E tests pass (100%)
- [ ] No regressions in other tests
- [ ] Full test suite results documented

### Epic Complete When:
- [ ] Both sprints completed
- [ ] Integration verified (backend + tests work together)
- [ ] All documentation updated
- [ ] Cleanup tasks completed (TASK-3.1, 3.2, 3.3 from original plan)

---

## 🚨 RISK MANAGEMENT

### Potential Issues

1. **URL Conflicts**: `django.contrib.auth.urls` vs `allauth.urls`
   - **Mitigation**: Verify URL order, test manually

2. **Template Missing**: `account/base_display.html` might not exist
   - **Mitigation**: TASK-1.3 verifies this early

3. **Selector Issues**: Tests might have other selector issues
   - **Mitigation**: TASK-2.4 runs full suite to catch all

4. **Test Regressions**: Other tests might break
   - **Mitigation**: Run full test suite, fix issues in TASK-2.4

### Blockers

- **SPRINT-2 blocked by SPRINT-1**: Must wait for allauth URLs
- **Template issues**: Could block TASK-1.3, need to resolve early

---

## 📊 PROGRESS TRACKING

### Sprint Board

```
SPRINT-1: Backend Implementation
├── [ ] TASK-1.1: Remove CustomLoginView (Agent 1)
├── [ ] TASK-1.2: Restore Allauth URLs (Agent 1)
├── [ ] TASK-1.3: Verify Allauth Settings (Agent 2)
└── [ ] TASK-1.4: Remove Django Login Template (Agent 2)

SPRINT-2: E2E Tests Update
├── [ ] TASK-2.1: Update auth-helpers.ts (Agent 3)
├── [ ] TASK-2.2: Update login.spec.ts (Agent 3)
├── [ ] TASK-2.3: Update Other Auth Tests (Agent 4)
└── [ ] TASK-2.4: Run Full Test Suite (Agent 4)
```

---

**Document Owner**: Senior Software Architect  
**Created**: 2025-12-30  
**Last Updated**: 2025-12-30


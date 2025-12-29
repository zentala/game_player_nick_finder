# Workflow dla 4 Agentów - Przywrócenie Allauth Login

**Dla**: 4 Senior Developers + Scrum Master  
**Metodologia**: Parallel Agent Workflow  
**Duration**: 2 równoległe sprints

---

## 👥 TEAM ASSIGNMENT

### Group A: Backend Sprint (SPRINT-1)
- **Agent 1**: Senior Backend Developer
  - Tasks: 1.1, 1.2
  - Focus: CustomLoginView removal, Allauth URLs restoration
  
- **Agent 2**: Senior Backend Developer
  - Tasks: 1.3, 1.4
  - Focus: Settings verification, Template cleanup

### Group B: Frontend/QA Sprint (SPRINT-2)
- **Agent 3**: Senior Frontend/QA Developer
  - Tasks: 2.1, 2.2
  - Focus: auth-helpers.ts, login.spec.ts
  
- **Agent 4**: Senior Frontend/QA Developer
  - Tasks: 2.3, 2.4
  - Focus: Other auth tests, Full test suite

**Scrum Master**: Coordinates both sprints, reviews PRs, manages dependencies

---

## 🔄 WORKFLOW OVERVIEW

```
DAY 1 (Start):
├── SPRINT-1 starts (Group A)
│   ├── Agent 1: TASK-1.1 (can start immediately)
│   └── Agent 2: TASK-1.3 (can start immediately, parallel)
│
└── SPRINT-2 blocked (Group B waits)

DAY 1-2 (SPRINT-1 continues):
├── Agent 1: TASK-1.2 (after TASK-1.1 done)
└── Agent 2: TASK-1.4 (after TASK-1.2 done, parallel with Agent 1)

DAY 2-3 (SPRINT-1 complete, SPRINT-2 starts):
├── SPRINT-1: All tasks done, merged to dev
│
└── SPRINT-2 starts (Group B)
    ├── Agent 3: TASK-2.1 (can start immediately)
    └── Agent 4: waits (TASK-2.3 blocked by TASK-2.1)

DAY 3-4 (SPRINT-2 continues):
├── Agent 3: TASK-2.2 (after TASK-2.1 done)
└── Agent 4: TASK-2.3 (after TASK-2.1 done, parallel with Agent 3)

DAY 4-5 (SPRINT-2 completion):
└── Agent 4: TASK-2.4 (after TASK-2.2 and TASK-2.3 done)
```

---

## 📋 DETAILED TASK WORKFLOW

### Phase 1: SPRINT-1 Backend (Days 1-2)

#### Agent 1 Workflow

**TASK-1.1: Remove CustomLoginView**
1. **Start**: Day 1, Hour 0
2. **Actions**:
   - Open `app/views.py`
   - Delete `CustomLoginView` class (lines 1879-1887)
   - Delete import `from django.contrib.auth.views import LoginView as DjangoLoginView`
   - Open `game_player_nick_finder/urls.py`
   - Remove `CustomLoginView` from imports
3. **Testing**:
   ```bash
   python manage.py check
   python manage.py runserver  # verify no import errors
   grep -r "CustomLoginView" .  # verify no remaining references
   ```
4. **Commit**: `refactor: remove CustomLoginView class and imports`
5. **PR**: Create PR, request review from Agent 2
6. **Done**: When PR approved and merged

**TASK-1.2: Restore Allauth URLs**
1. **Start**: After TASK-1.1 merged
2. **Dependencies**: TASK-1.1 must be complete
3. **Actions**:
   - Open `game_player_nick_finder/urls.py`
   - Remove line: `path('accounts/login/', CustomLoginView.as_view(), name='login')`
   - Uncomment: `path('accounts/', include('allauth.urls'))`
   - Remove comment: `# DISABLED: allauth conflicts with django.contrib.auth`
   - Verify URL order (allauth before django.contrib.auth)
4. **Testing**:
   ```bash
   python manage.py runserver
   curl http://localhost:8000/accounts/login/  # should return 200, allauth template
   python manage.py check --urls  # verify no URL conflicts
   ```
5. **Manual Test**:
   - Open browser: http://localhost:8000/accounts/login/
   - Verify: Uses `account/login.html` template
   - Verify: Form has field `id_login` (not `id_username`)
6. **Commit**: `feat: restore allauth URLs configuration`
7. **PR**: Create PR, request review from Agent 2
8. **Notify**: Inform Scrum Master and Group B that allauth is ready
9. **Done**: When PR approved and merged

---

#### Agent 2 Workflow

**TASK-1.3: Verify Allauth Settings**
1. **Start**: Day 1, Hour 0 (parallel with Agent 1 TASK-1.1)
2. **Actions**:
   - Open `game_player_nick_finder/settings/base.py`
   - Verify all required settings (see acceptance criteria)
   - Check if `account/base_display.html` exists
   - Document any missing settings
3. **Testing**:
   ```bash
   python manage.py check
   python manage.py runserver  # verify no config errors
   ```
4. **If issues found**:
   - Fix missing settings
   - Create `account/base_display.html` if missing (or report blocker)
5. **Commit**: `chore: verify and document allauth settings configuration`
6. **PR**: Create PR, request review from Agent 1
7. **Done**: When PR approved and merged

**TASK-1.4: Remove Django Login Template**
1. **Start**: After TASK-1.2 merged (allauth must be working)
2. **Dependencies**: TASK-1.2 must be complete
3. **Actions**:
   - Delete file: `app/templates/registration/login.html`
   - Verify no references: `grep -r "registration/login.html" .`
4. **Testing**:
   ```bash
   python manage.py runserver
   # Verify login still works (uses account/login.html)
   grep -r "registration/login.html" .  # should return no results (except docs)
   ```
5. **Manual Test**:
   - Open browser: http://localhost:8000/accounts/login/
   - Verify: Still works, uses `account/login.html`
6. **Commit**: `refactor: remove unused registration/login.html template`
7. **PR**: Create PR, request review from Agent 1
8. **Done**: When PR approved and merged

---

### Phase 2: SPRINT-2 Tests (Days 2-5)

#### Agent 3 Workflow

**TASK-2.1: Update auth-helpers.ts**
1. **Start**: After SPRINT-1 TASK-1.2 merged (allauth URLs restored)
2. **Dependencies**: SPRINT-1 TASK-1.2 must be complete
3. **Actions**:
   - Open `tests/helpers/auth-helpers.ts`
   - Find and replace: `#id_username` → `#id_login`
   - Find and replace: `input[name="username"]` → `input[name="login"]`
   - Update comments (remove CustomLoginView mentions, add allauth info)
4. **Testing**:
   ```bash
   npm run test:e2e tests/e2e/auth/login.spec.ts --grep "should successfully login"
   # Should use updated helper and work correctly
   ```
5. **Manual verification**:
   - Helper function should work with allauth login form
6. **Commit**: `test: update auth-helpers.ts to use allauth selectors (#id_login)`
7. **PR**: Create PR, request review from Agent 4
8. **Notify**: Inform Agent 4 that helper is ready
9. **Done**: When PR approved and merged

**TASK-2.2: Update login.spec.ts**
1. **Start**: After TASK-2.1 merged
2. **Dependencies**: TASK-2.1 must be complete
3. **Actions**:
   - Open `tests/e2e/auth/login.spec.ts`
   - Find and replace: `#id_username` → `#id_login` (all occurrences)
   - Find and replace: `input[name="username"]` → `input[name="login"]`
   - Update "Remember me" test to use `#id_remember`
   - Verify form selector `form.login` works
4. **Testing**:
   ```bash
   npm run test:e2e tests/e2e/auth/login.spec.ts
   # All 8 tests should pass (100%)
   ```
5. **If tests fail**:
   - Debug selector issues
   - Check if allauth form structure is different
   - Update selectors accordingly
6. **Commit**: `test: update login.spec.ts to use allauth selectors (#id_login)`
7. **PR**: Create PR, request review from Agent 4
8. **Done**: When PR approved and merged, all tests pass

---

#### Agent 4 Workflow

**TASK-2.3: Update Other Auth Tests**
1. **Start**: After TASK-2.1 merged (helper must be updated first)
2. **Dependencies**: TASK-2.1 must be complete
3. **Actions**:
   - Check each test file for allauth URL names:
     - `password-reset.spec.ts`: should use `account_reset_password`
     - `password-change.spec.ts`: should use `account_change_password`
     - `signup.spec.ts`: should link to `/accounts/login/`
     - `logout.spec.ts`: should use `account_logout`
     - `navbar-*.spec.ts`: should use allauth URLs
   - Update selectors if needed (`#id_username` → `#id_login`)
   - Update URL references if needed
4. **Testing**:
   ```bash
   npm run test:e2e tests/e2e/auth/password-reset.spec.ts
   npm run test:e2e tests/e2e/auth/password-change.spec.ts
   npm run test:e2e tests/e2e/auth/signup.spec.ts
   npm run test:e2e tests/e2e/auth/logout.spec.ts
   npm run test:e2e tests/e2e/navigation/*.spec.ts
   # All should pass
   ```
5. **Commit**: `test: update auth tests to use allauth URL names and selectors`
6. **PR**: Create PR, request review from Agent 3
7. **Done**: When PR approved and merged, all tests pass

**TASK-2.4: Run Full Test Suite**
1. **Start**: After TASK-2.2 and TASK-2.3 merged
2. **Dependencies**: TASK-2.2 and TASK-2.3 must be complete
3. **Actions**:
   - Run full E2E test suite:
     ```bash
     npm run test:e2e
     ```
   - Analyze results:
     - Check for any remaining `#id_username` errors
     - Check for URL name errors (`login` vs `account_login`)
     - Check for regressions in non-auth tests
   - Fix any issues found
   - Document test results
4. **Testing**:
   - Full suite should pass (or at least all auth tests 100%)
   - No regressions in other tests
5. **Commit**: `test: fix all E2E tests after allauth migration, all auth tests passing`
6. **PR**: Create PR, request review from Agent 3
7. **Documentation**: Update test results document
8. **Done**: When PR approved and merged, full suite passes

---

## 🤝 COORDINATION RULES

### Communication

**Daily Standup (Scrum Master coordinates)**:
- Each agent reports:
  - What they completed yesterday
  - What they're working on today
  - Any blockers or dependencies

**Dependency Notifications**:
- Agent 1 → Agent 2: "TASK-1.1 done, you can start TASK-1.2"
- Agent 1 → Group B: "TASK-1.2 done, allauth is ready, you can start SPRINT-2"
- Agent 3 → Agent 4: "TASK-2.1 done, helper updated, you can start TASK-2.3"

**PR Review Process**:
- Each PR must be reviewed by the other agent in the same group
- Scrum Master reviews all PRs before merge
- Cross-group review after sprints complete

### Conflict Resolution

**If two agents need same file**:
- First agent creates PR, second waits
- Or: Split file changes between agents
- Or: Coordinate through Scrum Master

**If test fails after merge**:
- Agent who wrote test fixes it
- Other agents can help debug
- Scrum Master coordinates if needed

---

## ✅ QUALITY GATES

### Before Committing

Each agent must verify:
- [ ] Code compiles/validates (TypeScript, Python)
- [ ] No linting errors
- [ ] Manual test passes (if applicable)
- [ ] Related tests pass (if applicable)

### Before PR Merge

PR reviewer must verify:
- [ ] Code follows project standards
- [ ] All acceptance criteria met
- [ ] Tests pass (if applicable)
- [ ] No obvious bugs
- [ ] Documentation updated (if needed)

### Before Sprint Completion

Sprint must have:
- [ ] All tasks completed
- [ ] All PRs merged
- [ ] Integration tested
- [ ] No blocking issues

---

## 📊 PROGRESS TRACKING

### Daily Status Updates

**Format** (each agent reports):
```
Agent X - Day Y:
✅ TASK-X.Y completed (merged)
🔄 TASK-X.Z in progress (50% done)
⏳ TASK-X.W waiting for dependency (Agent Y's TASK)
🚫 Blocker: [description]
```

### Sprint Board Updates

Update after each task completion:
- Move task from "In Progress" to "Done"
- Update sprint burndown chart
- Update epic progress

---

## 🚨 ESCALATION PROCESS

### Issues → Agent
- Agent tries to resolve independently
- Agent asks teammate for help
- Agent escalates to Scrum Master

### Blockers → Scrum Master
- Scrum Master coordinates resolution
- Scrum Master may reassign tasks
- Scrum Master escalates to Product Owner if needed

---

**Document Owner**: Scrum Master  
**Created**: 2025-12-30  
**For**: 4 Agent Development Team


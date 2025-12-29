# Quick Reference: Restore Allauth Login - Scrum Master Guide

**Epic**: EPIC-001 - Restore Allauth Login System  
**Team**: 4 Senior Developers (2 groups) + Scrum Master  
**Duration**: 2 sprints (parallel work)

---

## 👥 TEAM ASSIGNMENT

### Group A (Backend - SPRINT-1)
- **Agent 1**: TASK-1.1, TASK-1.2
- **Agent 2**: TASK-1.3, TASK-1.4

### Group B (Tests - SPRINT-2)
- **Agent 3**: TASK-2.1, TASK-2.2
- **Agent 4**: TASK-2.3, TASK-2.4

---

## ⏱️ TIMELINE

```
DAY 1:      SPRINT-1 starts (Group A)
            ├── Agent 1: TASK-1.1
            └── Agent 2: TASK-1.3 (parallel)

DAY 1-2:    SPRINT-1 continues
            ├── Agent 1: TASK-1.2 (after 1.1)
            └── Agent 2: TASK-1.4 (after 1.2)

DAY 2:      SPRINT-1 DONE → SPRINT-2 can start

DAY 2-3:    SPRINT-2 starts (Group B)
            ├── Agent 3: TASK-2.1
            └── Agent 4: waits (blocked)

DAY 3-4:    SPRINT-2 continues
            ├── Agent 3: TASK-2.2 (after 2.1)
            └── Agent 4: TASK-2.3 (after 2.1, parallel with 2.2)

DAY 4-5:    SPRINT-2 completion
            └── Agent 4: TASK-2.4 (after 2.2 and 2.3)
```

---

## 🔗 CRITICAL DEPENDENCIES

1. **SPRINT-2 blocked by SPRINT-1 TASK-1.2**
   - Group B cannot start until allauth URLs are restored
   - Agent 1 must notify when TASK-1.2 is complete

2. **TASK-1.2 blocked by TASK-1.1**
   - Must remove CustomLoginView before restoring allauth URLs

3. **TASK-1.4 blocked by TASK-1.2**
   - Must verify allauth works before removing old template

4. **TASK-2.2 and TASK-2.3 blocked by TASK-2.1**
   - Helper must be updated before test files

5. **TASK-2.4 blocked by TASK-2.2 and TASK-2.3**
   - Must update all tests before running full suite

---

## 📋 TASK SUMMARY

### SPRINT-1: Backend (4 tasks)

| Task | Agent | Story Points | Key Action |
|------|-------|--------------|------------|
| 1.1 | Agent 1 | 2 | Remove CustomLoginView |
| 1.2 | Agent 1 | 3 | Restore allauth URLs ⚠️ |
| 1.3 | Agent 2 | 2 | Verify allauth settings |
| 1.4 | Agent 2 | 1 | Remove old template |

**⚠️ TASK-1.2**: Critical - unlocks SPRINT-2

### SPRINT-2: Tests (4 tasks)

| Task | Agent | Story Points | Key Action |
|------|-------|--------------|------------|
| 2.1 | Agent 3 | 3 | Update auth-helpers.ts ⚠️ |
| 2.2 | Agent 3 | 5 | Update login.spec.ts |
| 2.3 | Agent 4 | 5 | Update other auth tests |
| 2.4 | Agent 4 | 5 | Run full test suite |

**⚠️ TASK-2.1**: Critical - unlocks TASK-2.2 and TASK-2.3

---

## ✅ ACCEPTANCE CRITERIA (Quick Check)

### SPRINT-1 Complete:
- [ ] CustomLoginView removed
- [ ] Allauth URLs active
- [ ] Login page works at `/accounts/login/`
- [ ] Uses `account/login.html` template
- [ ] Form has `#id_login` field (not `#id_username`)

### SPRINT-2 Complete:
- [ ] All selectors use `#id_login`
- [ ] All auth tests pass (100%)
- [ ] No regressions in other tests
- [ ] Full test suite passes

---

## 🚨 COMMON ISSUES & SOLUTIONS

### Issue: URL Conflicts
**Symptom**: Django error about duplicate URL patterns  
**Solution**: Verify allauth.urls is before django.contrib.auth.urls

### Issue: Template Not Found
**Symptom**: TemplateDoesNotExist: account/login.html  
**Solution**: Check TASK-1.3 - verify template exists

### Issue: Selector Errors in Tests
**Symptom**: `#id_username` not found  
**Solution**: Should use `#id_login` - check TASK-2.1/2.2

### Issue: Tests Fail After Merge
**Symptom**: Tests passing individually but failing in suite  
**Solution**: Check TASK-2.4 - run full suite, fix conflicts

---

## 📞 COORDINATION CHECKPOINTS

### Daily Standup Questions:
1. What did you complete yesterday?
2. What are you working on today?
3. Any blockers or dependencies?

### Key Notifications:
- **Agent 1 → Group B**: "TASK-1.2 done, allauth ready, SPRINT-2 can start"
- **Agent 3 → Agent 4**: "TASK-2.1 done, helper updated, TASK-2.3 can start"

---

## 📊 PROGRESS TRACKING

### Sprint Board Columns:
- **TODO**: Not started
- **IN PROGRESS**: Currently working
- **REVIEW**: PR created, waiting for review
- **DONE**: Merged to dev

### Burndown:
- SPRINT-1: 8 story points (4 tasks)
- SPRINT-2: 18 story points (4 tasks)
- **Total**: 26 story points

---

## 🔄 PR REVIEW PROCESS

### Within Group:
- Agent 1 ↔ Agent 2 (review each other's PRs)
- Agent 3 ↔ Agent 4 (review each other's PRs)

### Scrum Master:
- Reviews all PRs before merge
- Verifies acceptance criteria
- Checks for conflicts

### After Sprint:
- Cross-group review (Group B reviews Group A's work)
- Integration testing
- Final merge to dev

---

## ✅ DEFINITION OF DONE

### Task Level:
- [ ] Code written and tested
- [ ] Acceptance criteria met
- [ ] PR created and reviewed
- [ ] Merged to dev

### Sprint Level:
- [ ] All tasks completed
- [ ] All PRs merged
- [ ] Integration tested
- [ ] No blocking issues

### Epic Level:
- [ ] Both sprints completed
- [ ] Allauth is only login system
- [ ] All tests pass
- [ ] Documentation updated

---

**For Details**: See `RESTORE_ALLAUTH_LOGIN_SPRINT_PLAN.md` and `RESTORE_ALLAUTH_AGENTS_WORKFLOW.md`


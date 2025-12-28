# Git Workflow - Dev → Main Strategy
## Game Player Nick Finder

**Last Updated**: 2025-12-28
**Strategy**: Protected Main Branch with Dev Branch
**Owner**: Technical Project Manager

---

## 🎯 Strategia: Dev → Main (Recommended)

### Dlaczego NIE commitować bezpośrednio do `main`?

**Problem z current workflow**:
```
Developer → Commit directly to main → Push to main → Production (Render)
                                         ↓
                                   NO SAFETY NET!
                                   Bugs go directly to production!
```

**Nowy workflow z `dev` branch**:
```
Developer → Commit to dev → Push to dev → GitHub Actions Tests
                                              ↓ PASS
                                          Create PR: dev → main
                                              ↓ Approve
                                          Merge to main → Render Deploy
```

**Korzyści**:
- ✅ **Safety**: Testy uruchamiają się ZANIM kod trafi do produkcji
- ✅ **Quality Gate**: Main branch zawsze ma working code
- ✅ **Rollback**: Łatwo wrócić do poprzedniej wersji
- ✅ **Team Work**: Wielu developerów może pracować bez konfliktów
- ✅ **Review**: Możliwość code review przed merge

---

## 🌳 Branch Structure

```
main (production-ready, protected)
  ↑
  PR (after tests pass)
  ↑
dev (development, CI/CD testing)
  ↑
  merge
  ↑
feature/* (individual features)
  ├── feature/screenshots-upload
  ├── feature/memories-ui
  └── fix/login-selector
```

---

## 📋 Complete Workflow

### Setup (One Time)

```bash
# 1. Create dev branch from main
git checkout main
git pull origin main
git checkout -b dev
git push -u origin dev

# 2. Set dev as default branch for development
git config branch.dev.remote origin
git config branch.dev.merge refs/heads/dev
```

---

### Daily Development Workflow

#### Option A: Small Changes (Quick Fix)

```bash
# 1. Start from dev
git checkout dev
git pull origin dev

# 2. Make changes
# Edit files...

# 3. Commit to dev
git add .
git commit -m "fix: update login selector"

# 4. Push to dev
git push origin dev

# 5. GitHub Actions runs automatically on dev
# - Runs E2E tests
# - Runs Django CI
# - Takes ~15 minutes

# 6. If tests PASS:
#    - Create PR: dev → main (on GitHub)
#    - Approve PR
#    - Merge to main
#    - Render auto-deploys to production

# 7. If tests FAIL:
#    - Fix the issue
#    - Commit and push to dev again
#    - Repeat until tests pass
```

---

#### Option B: Larger Features (Multiple Commits)

```bash
# 1. Create feature branch from dev
git checkout dev
git pull origin dev
git checkout -b feature/screenshots-upload

# 2. Work on feature (multiple commits)
git add app/views.py
git commit -m "feat: add screenshot upload endpoint"

git add app/templates/
git commit -m "feat: add screenshot upload UI"

git add tests/e2e/
git commit -m "test: add screenshot upload E2E test"

# 3. Push feature branch
git push -u origin feature/screenshots-upload

# 4. Create PR: feature/screenshots-upload → dev
#    - GitHub Actions runs tests
#    - Wait for tests to pass

# 5. Merge to dev (on GitHub)
git checkout dev
git pull origin dev

# 6. When ready for production:
#    - Create PR: dev → main
#    - Tests run again (on dev branch)
#    - If pass → Merge to main
#    - Render deploys
```

---

## 🤖 GitHub Actions Integration

### What Triggers Tests?

**Current Configuration** (in `.github/workflows/e2e-tests.yml`):
```yaml
on:
  push:
    branches: [ main ]  # ← Tests on push to main
  pull_request:
    branches: [ main ]  # ← Tests on PR to main
```

**UPDATED Configuration** (recommended):
```yaml
on:
  push:
    branches: [ dev, main ]  # ← Tests on push to dev OR main
  pull_request:
    branches: [ dev, main ]  # ← Tests on PR to dev OR main
```

**What This Means**:
- Push to `dev` → Tests run automatically
- Create PR `dev → main` → Tests run again
- Push to `main` (after merge) → Tests run one more time
- **Triple safety**: Test on dev push, PR, and main push

---

### Workflow Examples

#### Example 1: Fix Bug in E2E Tests

```bash
# Current situation: Tests failing (95% fail rate)

# 1. Start from dev
git checkout dev
git pull origin dev

# 2. Fix login helper
# Edit: tests/helpers/auth-helpers.ts
# Update selectors: '#id_login' → correct selector

# 3. Commit
git add tests/helpers/auth-helpers.ts
git commit -m "fix(test): update login helper selector to match template"

# 4. Push to dev
git push origin dev

# 5. GitHub Actions runs (automatically)
# - Runs all 24 E2E tests
# - Status: Check GitHub Actions tab

# 6. Check results (after ~15 min)
# Scenario A: Tests PASS (60%+ pass rate)
#   → Great! Create PR: dev → main
#   → Merge to main
#   → Production updated with working tests

# Scenario B: Tests STILL FAIL
#   → Check GitHub Actions logs
#   → Fix more issues
#   → Commit and push to dev again
#   → Repeat until tests pass

# 7. When tests pass on dev:
# Go to GitHub → Pull Requests → New PR
# Base: main ← Compare: dev
# Title: "Fix E2E test selectors - pass rate 60%+"
# Create PR → Wait for tests → Merge
```

---

#### Example 2: Add New Feature (Screenshots)

```bash
# 1. Create feature branch
git checkout dev
git pull origin dev
git checkout -b feature/screenshots-upload

# 2. Implement backend
git add app/api_views.py
git commit -m "feat(api): add screenshot upload endpoint"

# 3. Implement frontend
git add app/templates/characters/character_profile_edit.html
git add static/js/screenshot-upload.js
git commit -m "feat(ui): add screenshot upload form"

# 4. Add tests
git add tests/e2e/characters/character-screenshots.spec.ts
git commit -m "test: add screenshot upload E2E test"

# 5. Push feature branch
git push -u origin feature/screenshots-upload

# 6. Create PR: feature/screenshots-upload → dev
# GitHub → New PR
# Base: dev ← Compare: feature/screenshots-upload
# Tests run automatically

# 7. If tests PASS:
#    Merge to dev (on GitHub)

# 8. Later, when ready for production:
#    Create PR: dev → main
#    Tests run again
#    Merge to main → Production deploy
```

---

## 🛡️ Branch Protection Rules

### For `main` Branch (Production)

**GitHub Settings → Branches → Add rule for `main`**:

```
Branch name pattern: main

✅ Require a pull request before merging
  ✅ Require approvals: 0 (if solo dev) or 1+ (if team)
  ✅ Dismiss stale pull request approvals when new commits are pushed
  ✅ Require approval of the most recent reviewable push

✅ Require status checks to pass before merging
  ✅ Require branches to be up to date before merging
  Status checks required:
    ✅ e2e-tests (from e2e-tests.yml)
    ✅ django-tests (from django-ci.yml)

✅ Require conversation resolution before merging

❌ Require signed commits (optional, for extra security)

✅ Require linear history (optional, keeps git log clean)

✅ Include administrators (IMPORTANT!)
  - Even admins cannot bypass rules
  - Ensures quality even for solo developers
```

**Effect**:
- ❌ Cannot push directly to `main` (blocked)
- ❌ Cannot merge PR if tests fail
- ✅ Must use PR workflow
- ✅ Always safe

---

### For `dev` Branch (Optional)

**Less strict, but still protected**:

```
Branch name pattern: dev

✅ Require status checks to pass before merging (if using PRs to dev)
  Status checks:
    ✅ e2e-tests
    ✅ django-tests

❌ Require pull request (can push directly to dev if solo dev)

❌ Include administrators (dev is less strict)
```

**Effect**:
- ✅ Can push directly to `dev` for quick iterations
- ✅ Tests run automatically on push
- ✅ PR required for `dev → main`

---

## 🚀 Render Integration

### How Render Knows What to Deploy

**Render Dashboard → Service Settings → Branch**:

**Current Setting** (likely):
```
Branch: main
```

**What This Means**:
- Render watches `main` branch ONLY
- When `main` is updated (via PR merge), Render deploys
- `dev` branch changes do NOT trigger deploy
- Perfect! Dev is for testing, main is for production

**No Changes Needed** - Current setup is correct!

---

### Complete Flow with Render

```
Developer
  ↓ commit
dev branch
  ↓ push
GitHub Actions (on dev)
  ↓ tests run
  ✅ PASS
  ↓ create PR
dev → main PR
  ↓ tests run again (on PR)
  ✅ PASS
  ↓ merge
main branch updated
  ↓ Render detects change
Render Build & Deploy
  ↓ 5-10 minutes
Production Updated ✅
```

---

## 📝 Update Documentation Files

### Files That Need Updating:

#### 1. CLAUDE.md

**Add Section**:
```markdown
## Git Workflow

**Branch Strategy**: Dev → Main (Protected Main)

**Daily Development**:
1. Work on `dev` branch
2. Push to `dev` → GitHub Actions tests
3. When tests pass → Create PR: `dev → main`
4. Merge to `main` → Render deploys to production

**Never commit directly to `main`** - Always use `dev` branch first.

See: [Git Workflow Guide](docs/GIT_WORKFLOW.md)
```

---

#### 2. .cursor/rules/always.mdc

**Add Section**:
```markdown
## Git Workflow Rules

**CRITICAL**: ALWAYS work on `dev` branch, NEVER commit directly to `main`.

### Default Branch for Development
- Default branch: `dev`
- Production branch: `main` (protected)

### Daily Workflow
1. Start from dev: `git checkout dev && git pull`
2. Make changes and commit to dev
3. Push to dev: `git push origin dev`
4. GitHub Actions runs tests automatically
5. When tests pass → Create PR: dev → main
6. Merge PR → Render deploys to production

### Feature Branches
For larger features:
- Create: `git checkout -b feature/feature-name` (from dev)
- Push: `git push -u origin feature/feature-name`
- PR: feature/feature-name → dev
- When ready: PR: dev → main

### NEVER
- ❌ NEVER commit directly to main
- ❌ NEVER push to main
- ❌ NEVER bypass branch protection

### Emergency Hotfix
If production is broken and needs immediate fix:
1. Create hotfix branch from main: `git checkout -b hotfix/critical-bug`
2. Fix the bug
3. Create PR: hotfix/critical-bug → main
4. Tests must pass even for hotfixes
5. After deploy, merge back to dev: `git checkout dev && git merge main`
```

---

## 🎓 Learning Curve

### For Solo Developer (You)

**Week 1**: Feels slower
- Extra step to create PR
- Wait for tests to run
- More clicks on GitHub

**Week 2**: Neutral
- Getting used to workflow
- Tests catch bugs before production
- Appreciate safety net

**Week 3+**: Faster overall
- Confidence in deployments
- No "oh no, I broke production" moments
- Tests validate changes before deploy
- Can deploy fearlessly

---

### For Team (Future)

**When you add developers**:
- ✅ Already have workflow in place
- ✅ Protected main prevents conflicts
- ✅ Each developer uses feature branches
- ✅ Code review via PR comments
- ✅ No accidental production breaks

---

## 📊 Comparison: Old vs New Workflow

### Old Workflow (Current)

```
Developer makes change
  ↓
Commit to main
  ↓
Push to main
  ↓
Render deploys to production
  ↓
Bug discovered in production! 😱
  ↓
Scramble to fix
  ↓
Push fix to main
  ↓
Hope it works...
```

**Issues**:
- No testing before production
- Bugs go live immediately
- High stress deployments
- No rollback mechanism

---

### New Workflow (Recommended)

```
Developer makes change
  ↓
Commit to dev
  ↓
Push to dev
  ↓
GitHub Actions runs tests (15 min)
  ↓ FAIL → Fix → Push to dev → Test again
  ↓ PASS
Create PR: dev → main
  ↓
Tests run again (double-check)
  ↓ PASS
Merge to main
  ↓
Render deploys to production
  ↓
Works perfectly! ✅
```

**Benefits**:
- Tests catch bugs BEFORE production
- Main branch always stable
- Low stress deployments
- Easy rollback (just revert PR)

---

## 🚨 Emergency Procedures

### What If Production Is Broken?

**Scenario**: You merged to main, Render deployed, production is broken.

**Solution 1: Revert PR** (Recommended)
```bash
# On GitHub:
1. Go to PR that was merged
2. Click "Revert" button
3. Creates new PR that undoes changes
4. Merge revert PR
5. Production rolls back automatically
```

**Solution 2: Rollback Manually**
```bash
# On Render Dashboard:
1. Go to service → Deploys tab
2. Find last working deploy
3. Click "Redeploy"
4. Production restored in ~5 minutes
```

**Solution 3: Hotfix**
```bash
# If simple fix:
git checkout main
git pull origin main
git checkout -b hotfix/critical-bug

# Fix the bug
# ...

git commit -m "hotfix: fix critical production bug"
git push -u origin hotfix/critical-bug

# Create PR: hotfix/critical-bug → main
# Tests run (even for hotfix!)
# Merge → Deploys

# Don't forget to sync dev:
git checkout dev
git merge main
git push origin dev
```

---

## ✅ Setup Checklist

### Initial Setup (Do Once)

- [ ] Create `dev` branch: `git checkout -b dev && git push -u origin dev`
- [ ] Update GitHub Actions to test on `dev` branch
- [ ] Set up branch protection for `main` (requires PR)
- [ ] Set up branch protection for `dev` (optional, lighter rules)
- [ ] Update CLAUDE.md with workflow
- [ ] Update .cursor/rules/always.mdc with workflow
- [ ] Test workflow: Make small change → Push to dev → Create PR → Merge
- [ ] Verify Render still deploys from `main` only

### Daily Checklist (Every Development Session)

- [ ] Start from dev: `git checkout dev && git pull origin dev`
- [ ] Make changes
- [ ] Commit to dev: `git add . && git commit -m "..."`
- [ ] Push to dev: `git push origin dev`
- [ ] Wait for GitHub Actions (check Actions tab)
- [ ] If tests pass → Create PR: dev → main
- [ ] Merge PR → Production deployed

---

## 📚 Resources

**Git Documentation**:
- Branch Protection: https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches
- Pull Requests: https://docs.github.com/en/pull-requests

**GitHub Actions**:
- Workflow Syntax: https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions

**Render**:
- Deploy Branches: https://render.com/docs/deploys

---

**Last Updated**: 2025-12-28
**Owner**: Technical Project Manager
**Status**: RECOMMENDED - Ready to implement

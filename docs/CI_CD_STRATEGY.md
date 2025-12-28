# CI/CD Strategy - GitHub Actions + Render
## Game Player Nick Finder

**Last Updated**: 2025-12-28
**Status**: CONFIGURED (GitHub Actions) + INTEGRATED (Render Auto-Deploy)

---

## 🎯 Strategia: Separation of Concerns

### GitHub Actions = **QUALITY GATE** (Testing)
- Uruchamia testy **PRZED** merge do `main`
- Blokuje merge jeśli testy failują
- Nie deployuje - tylko weryfikuje jakość kodu

### Render = **DEPLOYMENT** (Production)
- Automatycznie deployuje **PO** merge do `main`
- Używa własnego build procesu
- Nie uruchamia testów - tylko buduje i deployuje

**Flow**:
```
Developer → Create PR → GitHub Actions (Tests) → Merge to main → Render (Auto-Deploy) → Production
                             ↓ FAIL                    ↓ PASS
                          Block merge              Auto-deploy
```

---

## 📋 GitHub Actions - Co Robi?

### Workflow 1: `e2e-tests.yml` (E2E Testing)

**Trigger**: Push to `main` OR Pull Request to `main`

**Co robi**:
1. ✅ Checkout code
2. ✅ Setup Python 3.10 + Node.js 18
3. ✅ Install dependencies (pipenv + pnpm)
4. ✅ Install Playwright browsers (chromium, firefox, webkit)
5. ✅ Run Django migrations
6. ✅ Load test fixtures
7. ✅ Start Django server (localhost:8000)
8. ✅ Run E2E tests (all 24 tests)
9. ✅ Upload test reports (artifacts)
10. ✅ Upload screenshots on failure

**Matrix Strategy**: Testuje na 3 przeglądarkach równocześnie:
- Chromium (Chrome/Edge)
- Firefox
- WebKit (Safari)

**Output**:
- ✅ Green check mark jeśli wszystkie testy pass
- ❌ Red X jeśli jakikolwiek test fails
- 📊 Test reports dostępne jako artifacts (30 dni)

---

### Workflow 2: `django-ci.yml` (Django Unit Tests + Linting)

**Trigger**: Push to `main` OR Pull Request to `main`

**Co robi**:
1. ✅ Django unit tests (`python manage.py test`)
2. ✅ Migration check (czy brakuje migracji)
3. ✅ Code linting (flake8)

**Output**:
- ✅ Sprawdza czy kod jest czysty
- ❌ Blokuje merge jeśli unit tests failują

---

## 🚀 Render - Co Robi?

### Auto-Deploy on Main Branch

**Trigger**: Push to `main` branch (automatycznie po merge PR)

**Co robi** (Render Build Process):
1. ✅ Checkout latest `main` commit
2. ✅ Run `scripts/build.sh`:
   ```bash
   pip install -r requirements.txt
   python manage.py collectstatic --noinput
   python manage.py migrate
   ```
3. ✅ Deploy new version
4. ✅ Health check (czy serwis odpowiada)
5. ✅ Rollback jeśli health check fails

**NIE uruchamia testów** - zakłada że GitHub Actions już zweryfikowało jakość.

---

## ✅ Dlaczego To Ma Sens?

### GitHub Actions (Testing):
- **Fast feedback**: Developer widzi czy testy passują PRZED merge
- **Multi-browser**: Testuje na 3 przeglądarkach
- **Free**: GitHub Actions free tier: 2000 minut/miesiąc (wystarczy)
- **Artifacts**: Test reports dostępne do analizy

### Render (Deployment):
- **Specialized**: Render jest zoptymalizowany do deploymentu Django
- **Fast deploy**: Używa cache dla dependencies
- **Auto rollback**: Jeśli deploy fails, automatycznie rollback
- **Production DB**: Ma dostęp do production PostgreSQL

---

## 🔄 Complete Flow Example

### Scenario: Developer naprawia bug w POKE system

```
1. Developer creates branch
   git checkout -b fix/poke-rate-limit

2. Developer makes changes
   - Edit app/utils.py
   - Fix can_send_poke() function

3. Developer commits
   git commit -m "fix: relax POKE rate limit for test users"

4. Developer creates PR
   git push origin fix/poke-rate-limit
   # Creates PR on GitHub: fix/poke-rate-limit → main

5. GitHub Actions TRIGGERS (automatically)
   - Runs e2e-tests.yml
   - Runs django-ci.yml
   - Status: ⏳ Running...

6. Tests Complete (15 minutes later)
   Scenario A: ✅ ALL PASS
   - PR shows green checkmark
   - "All checks have passed"
   - Developer can merge

   Scenario B: ❌ SOME FAIL
   - PR shows red X
   - "Some checks failed"
   - Merge blocked
   - Developer must fix and push again

7. Developer merges PR (assuming tests pass)
   - PR merged to main
   - Branch deleted

8. Render TRIGGERS (automatically, ~30 seconds after merge)
   - Detects new commit on main
   - Starts build process
   - Status: ⏳ Building...

9. Render Build Complete (5-10 minutes later)
   Scenario A: ✅ BUILD SUCCESS
   - New version deployed to production
   - https://gpnf.zentala.io shows new code

   Scenario B: ❌ BUILD FAIL
   - Render automatically rollbacks to previous version
   - Production still shows old working code
   - Developer gets notification

10. DONE ✅
    - Code tested by GitHub Actions
    - Code deployed by Render
    - Production updated
```

---

## 🛡️ Safety Mechanisms

### 1. GitHub Actions Blocks Bad Code
```
Developer tries to merge buggy code
    ↓
GitHub Actions runs tests
    ↓
Tests FAIL
    ↓
PR shows "Checks failed"
    ↓
Merge button DISABLED
    ↓
Code CANNOT reach production
```

### 2. Render Rollback Protection
```
Good code merged to main
    ↓
Render starts deploy
    ↓
Build process FAILS (e.g., migration error)
    ↓
Health check FAILS
    ↓
Render automatically ROLLBACK to previous version
    ↓
Production STILL WORKING with old version
```

### 3. Combined Protection
```
GitHub Actions: Prevents bad code from reaching main
Render Rollback: Prevents bad deployments from staying live
```

---

## 📊 Monitoring & Notifications

### GitHub Actions Status
**Where to check**:
- PR page: Shows ✅ or ❌ next to each check
- Actions tab: https://github.com/zentala/game_player_nick_finder/actions
- Email: GitHub sends notification on failure

**Artifacts**:
- Test reports: Available for 30 days
- Screenshots (on failure): Available for 7 days
- Download from Actions tab → Workflow run → Artifacts section

### Render Deploy Status
**Where to check**:
- Render Dashboard: https://dashboard.render.com
- Deploy logs: Click on service → Logs tab
- Email: Render sends notification on deploy success/failure

---

## 🔧 Configuration Files

### GitHub Actions
**Location**: `.github/workflows/`

**Files**:
- `e2e-tests.yml` - E2E test workflow
- `django-ci.yml` - Django unit tests + linting

**To edit**:
```bash
# Edit workflow
nano .github/workflows/e2e-tests.yml

# Commit changes
git add .github/workflows/
git commit -m "ci: update E2E test workflow"
git push
```

### Render
**Location**: `render.yaml` (optional, for Blueprint deployment)

**Build Command** (in Render dashboard):
```bash
bash scripts/build.sh
```

**Start Command**:
```bash
gunicorn game_player_nick_finder.wsgi:application
```

---

## 💰 Cost Analysis

### GitHub Actions
**Free Tier**:
- 2000 minutes/month (public repo)
- ~15 minutes per E2E test run
- Can run ~133 times/month for free

**Usage Estimate**:
- 5 PRs/day × 15 min = 75 min/day
- 75 min/day × 22 work days = 1650 min/month
- **Fits in free tier** ✅

### Render
**Free Tier** (Web Service):
- Free tier available but limited (sleeps after 15 min inactivity)

**Paid Tier** (Recommended for production):
- $7/month (Starter plan)
- Always-on
- Auto-deploy from GitHub
- PostgreSQL database included

**Total Cost**: $7/month + $0 (GitHub Actions free)

---

## 🎯 Best Practices

### 1. Always Run Tests Locally First
```bash
# Before creating PR, run tests locally
pnpm load:fixtures
pnpm test:e2e

# If pass → create PR
# If fail → fix and repeat
```

### 2. Use Branch Protection Rules
**GitHub Settings → Branches → Add rule**:
- [x] Require status checks to pass before merging
- [x] Require branches to be up to date
- [x] Include administrators

**Effect**: Cannot merge PR if tests fail, even if you're admin.

### 3. Keep Workflows Fast
**Current speed**:
- E2E tests: ~15 minutes
- Django CI: ~5 minutes

**If too slow**:
- Run only critical tests on PR
- Run full test suite on main branch only
- Use test parallelization

### 4. Monitor Failure Patterns
**If tests fail frequently**:
- Check if flaky tests (sometimes pass, sometimes fail)
- Add explicit waits in tests
- Improve test stability

---

## 🚨 Troubleshooting

### Problem: GitHub Actions Fails but Tests Pass Locally

**Possible Causes**:
1. **Environment difference**: Local uses different Python/Node version
   - Solution: Match versions in workflow with local

2. **Timing issues**: GitHub Actions runners slower than local machine
   - Solution: Add longer timeouts in tests

3. **Fixture data**: Fixtures not loaded properly
   - Solution: Check workflow logs, verify fixture loading step

### Problem: Render Deploy Fails but GitHub Actions Pass

**Possible Causes**:
1. **Migration issue**: Production DB has different state
   - Solution: Check Render logs, may need manual migration

2. **Environment variables missing**: DJANGO_SECRET_KEY, etc.
   - Solution: Add in Render dashboard → Environment tab

3. **Static files**: collectstatic fails
   - Solution: Check build.sh script, verify static files config

### Problem: Tests Pass but Feature Broken in Production

**Possible Causes**:
1. **Environment-specific bug**: DEBUG=True vs DEBUG=False
   - Solution: Test with DEBUG=False locally

2. **Database difference**: SQLite (test) vs PostgreSQL (prod)
   - Solution: Run tests with PostgreSQL locally

3. **Static files not updating**: Browser cache
   - Solution: Hard refresh (Ctrl+Shift+R)

---

## 📚 Resources

**GitHub Actions**:
- Docs: https://docs.github.com/en/actions
- Marketplace: https://github.com/marketplace?type=actions

**Render**:
- Docs: https://render.com/docs
- Dashboard: https://dashboard.render.com

**Playwright**:
- CI/CD Guide: https://playwright.dev/docs/ci

---

## ✅ Summary

**GitHub Actions**:
- ✅ Tests quality BEFORE merge
- ✅ Blocks bad code from reaching main
- ✅ Multi-browser testing
- ✅ Free tier sufficient
- ✅ Artifacts for debugging

**Render**:
- ✅ Deploys AFTER tests pass
- ✅ Specialized for Django
- ✅ Auto rollback on failure
- ✅ Production-ready
- ✅ Simple configuration

**Together**:
- ✅ Complete CI/CD pipeline
- ✅ Quality gate + deployment
- ✅ Safe production updates
- ✅ Cost-effective
- ✅ **RECOMMENDED** ✅

---

**Strategy Owner**: Technical Project Manager (Claude Code)
**Implementation**: Ready to commit
**Status**: CONFIGURED and DOCUMENTED

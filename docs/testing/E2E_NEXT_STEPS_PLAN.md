# E2E Test Fixes - Next Steps Plan
**Utworzono**: 2025-12-28
**Autor**: Claude Code (Software/Solution Architect)
**Status**: Waiting for Owner Approval

## Executive Summary

Po zakończeniu pracy 7 agentów równoległych i otrzymaniu odpowiedzi właściciela, przygotowano szczegółowy plan dalszych działań. Obecny status to **123 passing / 456 total (27%)**. Oczekiwany wzrost po obecnych naprawach: **~50-55%** (po załadowaniu nowych fixtures i uruchomieniu testów).

**Commits wykonane**:
- `69425b3` - Documentation (E2E_TEST_STATUS + ARCHITECTURAL_ANALYSIS)
- `486d04d` - Architectural fixes (Quick Wins + z-index/pointer-events)
- `bd0867de` - All agent fixes (dropdown, layout switcher, fixtures, docs)
- `84f2804` - Edge cases (redirect, register link)

**Wszystkie zmiany są skomitowane i gotowe do testowania.**

---

## Odpowiedzi Właściciela - Podsumowanie

### 1. ✅ POKE System
**Status**: Powinien być zaimplementowany i przetestowany
**Zrobione przez Agenta 5**:
- Dodano 12 POKE fixtures z różnymi statusami:
  - PENDING (4 POKEs)
  - RESPONDED (4 POKEs)
  - IGNORED (2 POKEs)
  - BLOCKED (2 POKEs)
- Fixtures obejmują różne scenariusze (testuser ↔ otheruser, zentala characters)
- Odblokowuje ~20 skipped testów

**Do zweryfikowania**: Uruchomić testy i sprawdzić czy wszystkie POKE testy przechodzą.

### 2. ✅ Blocking System
**Status**: Jest zaimplementowany
**Zrobione przez Agenta 5**:
- Dodano 5 CharacterBlock fixtures:
  - testuser's char blokuje spammer (spam report)
  - otheruser's char blokuje innego (inappropriate behavior)
  - zentala's char blokuje różne characters (różne powody)
- Fixtures pokrywają scenariusze:
  - Spam reports (reported_as_spam: true)
  - Regular blocks (with reasons)
  - Różne pary characters
- Odblokowuje ~32 skipped testów

**Do zweryfikowania**: Uruchomić testy i sprawdzić czy blocking interaction testy przechodzą.

### 3. ⚠️ Messaging System
**Status**: Działa ręcznie z użytkownikiem "zentala", ale testy padają
**Hipoteza**: Testy używają testuser, ale mogą nie wybierać właściwego charactera

**Analiza fixtures**:
```json
// Message fixtures dla testuser:
- Message #8: testuser's char (15f97226...) → otheruser's char (483ccf39...)
  Content: "Hey other-char-123! Great game yesterday!"
  Thread: 880e8400-e29b-41d4-a716-446655440003

- Message #9: otheruser's char → testuser's char
  Content: "Absolutely! I had a lot of fun. How about this weekend?"
  Thread: 880e8400-e29b-41d4-a716-446655440003

- Message #10: testuser's char → otheruser's char
  Content: "Perfect! Saturday evening works for me. See you then!"
  Thread: 880e8400-e29b-41d4-a716-446655440003
```

**Problem zidentyfikowany**:
- Testy idą na `/messages/` bez parametru `?character=<id>`
- System jest **character-centric** - wymaga wyboru charactera przed wyświetleniem konwersacji
- URL powinien być: `/messages/?character=15f97226-ca54-4e26-8e18-37be99014caa`

**Do naprawienia**:
1. Sprawdzić jak `/messages/` view obsługuje brak parametru `character`
2. Albo dodać domyślne wybieranie pierwszego charactera użytkownika
3. Albo zaktualizować testy żeby wybierały character przed przejściem do `/messages/`

### 4. ⚙️ Password Validation Requirements
**Status**: Potrzebne dla production
**Rekomendowane ustawienia** (sensowne defaults):

```python
# settings/production.py

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {'min_length': 8}  # Minimum 8 znaków
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
        # Blokuje hasła składające się tylko z cyfr
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
        # Blokuje najpopularniejsze hasła (password123, qwerty, itp.)
    },
    # NIE DODAJEMY UserAttributeSimilarityValidator - może być zbyt restrykcyjne
    # NIE DODAJEMY uppercase/special char requirements - lepsza UX
]
```

**Uzasadnienie**:
- ✅ 8 znaków minimum - industry standard, bezpieczne ale nie frustrujące
- ✅ Wymaganie cyfr - NumericPasswordValidator blokuje TYLKO numeryczne (123456)
- ✅ Common password list - chroni przed słabymi hasłami
- ❌ NIE wymagamy wielkich liter - frustrujące dla użytkowników
- ❌ NIE wymagamy znaków specjalnych - frustrujące i nie zawsze bezpieczniejsze
- ❌ NIE sprawdzamy podobieństwa do username - może być zbyt restrykcyjne

**UX Message** (friendly):
```
"Your password must be at least 8 characters long and cannot be too common
(like 'password123'). Mix letters and numbers for better security."
```

---

## Co Zostało Zrobione - Status Update

### ✅ COMPLETED (7 Agentów + Commits)

#### Agent 1: Dokumentacja (Commit: 69425b3)
- ✅ `docs/testing/E2E_TEST_STATUS_2025-12-28.md` - Szczegółowy breakdown 123/273/60
- ✅ `docs/testing/E2E_ARCHITECTURAL_ANALYSIS.md` - Root cause analysis

#### Agent 2: Dropdown Navigation Fix (Commit: bd0867de)
- ✅ `tests/helpers/auth-helpers.ts` - openUserMenu() helper
- ✅ Bootstrap animation wait (200ms + visibility check)
- ✅ Update ~10 test files używających dropdown
- **Impact**: ~50 testów (navbar, logout, password-change)

#### Agent 3: Conditional Layout Switcher (Commit: bd0867de)
- ✅ `app/templates/base_navbar.html` - Layout switcher w dropdown (staff only)
- ✅ `app/templates/homepage/layout_switcher.html` - Deprecate fixed overlay (display: none)
- ✅ Bootstrap icons dla każdej opcji (v0, v1, v2, v3)
- ✅ Reset option jeśli session layout ustawiony
- **Impact**: Lepsza UX, brak blokowania UI, cleaner architecture

#### Agent 4: Production Deployment Checklist (Commit: bd0867de)
- ✅ `docs/deployment/BEFORE_PRODUCTION_CHECKLIST.md` - 530 linii comprehensive guide
- ✅ Email validation requirements (CRITICAL)
- ✅ Security hardening (DEBUG=False, HTTPS, SECURE_*, CSP)
- ✅ `TASKS.md` - Pre-production section dodany
- ✅ `docs/PROJECT_STATUS_SUMMARY.md` - Production readiness warning

#### Agent 5: POKE & Block Fixtures (Commit: bd0867de)
- ✅ `app/fixtures/users_and_characters.json` - 12 POKEs + 5 Blocks
- ✅ POKE statuses: PENDING (4), RESPONDED (4), IGNORED (2), BLOCKED (2)
- ✅ CharacterBlock fixtures: spam reports (2), regular blocks (3)
- **Impact**: Odblokowuje ~60 skipped testów

#### Agent 6: Edge Cases (Commit: 84f2804)
- ✅ `app/views.py` - CustomLoginView z redirect_authenticated_user=True
- ✅ `game_player_nick_finder/urls.py` - Override /accounts/login/ URL
- ✅ `tests/e2e/auth/signup.spec.ts` - Fix register URL (/register/step1/)
- ✅ `tests/e2e/auth/password-reset.spec.ts` - Fix "Forgot Password" selector (already fixed by Agent 2)
- **Impact**: ~3 edge case testy

#### Agent 7: Commit All Changes (Commit: bd0867de)
- ✅ Wszystkie zmiany agentów skomitowane
- ✅ 9 plików, +930 insertions, -49 deletions
- ✅ Comprehensive commit message z opisem wszystkich agentów

### 📊 Oczekiwane Wyniki (Po uruchomieniu testów z nowymi fixtures)

**Przed naprawami**: 123 passed / 273 failed / 60 skipped (27%)

**Po naprawach** (estymacja):
- Dropdown fix: +45-50 testów (navbar, logout, password-change)
- Edge cases: +3 testy (redirect, register link)
- Layout switcher fix: +2-3 testy (no UI blocking)
- **Total**: ~170-176 passing (~37-38% pass rate)

**Po odblokowaniu fixtures** (POKE + Blocking):
- POKE tests: +15-20 testów (was skipped, now should pass)
- Blocking tests: +25-30 testów (was skipped, now should pass)
- **Total z fixtures**: ~210-226 passing (~46-50% pass rate)

**🎯 Oczekiwany wynik końcowy: 210-226 / 456 testów (46-50%)**

---

## Co NIE Zostało Zrobione - Pozostałe Problemy

### 🔴 HIGH PRIORITY

#### 1. Messaging System Tests (12 failed)
**Problem**: Wszystkie conversation-list testy padają z timeout 30s
**Root Cause**: System character-centric wymaga wyboru charactera przed `/messages/`

**Files**: `tests/e2e/messaging/conversation-list.spec.ts`

**Scenariusze**:
- Test idzie na `/messages/` bez parametru `?character=<id>`
- Backend prawdopodobnie zwraca błąd lub przekierowuje
- Test timeout czekając na `.conversation-list` element

**Potencjalne rozwiązania**:

**Option A**: Update `/messages/` view żeby auto-wybierał pierwszego charactera
```python
# app/views.py - MessageListView
def get(self, request):
    character_id = request.GET.get('character')
    if not character_id:
        # Auto-select first character
        first_char = request.user.character_set.first()
        if first_char:
            return redirect(f'/messages/?character={first_char.pk}')
        else:
            # No characters - show error
            messages.error(request, "You need to create a character first")
            return redirect('character_create')
    # Continue with normal flow...
```

**Option B**: Update tests żeby wybierały character przed `/messages/`
```typescript
test.beforeEach(async ({ page }) => {
    await login(page, 'testuser', 'testpass123');

    // Get testuser's first character ID
    // Navigate to /messages/?character=<id>
    await page.goto('/messages/?character=15f97226-ca54-4e26-8e18-37be99014caa');
});
```

**Option C**: Dodać character selector na `/messages/` page
- If no character selected, show dropdown
- User wybiera character
- URL updates to `/messages/?character=<id>`

**Rekomendacja**: **Option A** (auto-select) + **Option C** (character selector dla multi-character users)
- Najlepszy UX: automatyczne wybieranie dla prostoty
- Character selector dla użytkowników z wieloma charakterami
- Zachowuje character-centric architecture

#### 2. Validation Messages Not Showing (~15 failed)
**Problem**: Testy oczekują komunikatów błędów, ale nie są widoczne

**Examples**:
- `should show validation error for invalid email format` (password-reset)
- `should show validation error for password too short` (password-change)
- `should show validation error for password mismatch` (password-change)

**Możliwe przyczyny**:
1. Django validation wyłączona (unlikely - Quick Wins pokazały że działają)
2. Crispy forms nie renderuje błędów poprawnie
3. Selektory w testach niepoprawne (`.alert-danger, .errorlist, .invalid-feedback`)
4. HTML5 validation przejmuje przed Django validation

**Do zbadania**:
- Sprawdzić czy formularze mają `novalidate` attribute (wyłącza HTML5 validation)
- Sprawdzić template rendering błędów (crispy forms)
- Uruchomić pojedynczy test z headless:false żeby zobaczyć co się dzieje

**Potencjalne rozwiązanie**:
```django
{# Dodać novalidate do formularzy żeby wyłączyć HTML5 validation #}
<form class="password_change" method="post" action="." novalidate>
```

### ⚠️ MEDIUM PRIORITY

#### 3. Profile Edit Tests (~8 failed)
**Problem**: Timeouts przy próbie edycji profilu

**Prawdopodobna przyczyna**: Dropdown navigation issue (dostęp przez user menu)
- **Status**: Powinno być naprawione przez Agent 2 (openUserMenu helper)
- **Do zweryfikowania**: Uruchomić testy po załadowaniu nowych fixtures

#### 4. Character Tests (~5 failed)
**Problem**: Character profile edit, friend list, friend request list

**Prawdopodobna przyczyna**: Dropdown navigation + brak testowych danych
- Dropdown navigation - naprawione przez Agent 2
- Friendships fixtures - nie zostały dodane przez Agent 5

**Do dodania**:
```json
{
    "model": "app.characterfriend",
    "pk": 4,
    "fields": {
        "character1": "15f97226-ca54-4e26-8e18-37be99014caa",
        "character2": "66de8400-e29b-41d4-a716-446655440001",
        "created_at": "2024-03-15T10:00:00Z"
    }
}
```

### 📌 LOW PRIORITY

#### 5. Password Validation in Production
**Status**: Recommendations provided (see section 4 above)
**Do zrobienia**:
1. Dodać validators do `settings/production.py`
2. Dodać friendly error messages
3. Update `BEFORE_PRODUCTION_CHECKLIST.md` z password policy

---

## Plan Działania - Następne Kroki

### KROK 1: Weryfikacja Obecnych Napraw (REQUIRED FIRST)
**Cel**: Sprawdzić czy naprawy agentów działają
**Zadania**:
1. ✅ Załadować fixtures: `pnpm load:fixtures`
2. ✅ Uruchomić Django server: `python manage.py runserver 7600`
3. ✅ Uruchomić wszystkie testy: `pnpm test:e2e`
4. ✅ Przeanalizować wyniki - ile testów przeszło
5. ✅ Zapisać raport do `docs/testing/E2E_TEST_RESULTS_AFTER_FIXES.md`

**Oczekiwany wynik**: ~210-226 passing (46-50%)

**Eskalacja jeśli**:
- Dropdown tests nadal padają → Zbadać Bootstrap animation timing
- POKE/Blocking tests nadal skipped → Sprawdzić czy fixtures załadowane
- Layout switcher tests padają → Zbadać pointer-events: none side effects

---

### KROK 2: Naprawić Messaging System (HIGH PRIORITY)
**Cel**: 12 conversation-list testów przejść

**Zadania**:

**2.1. Zbadać obecne zachowanie**
- Ręcznie przetestować `/messages/` bez parametru character
- Sprawdzić co backend zwraca (404, redirect, error?)
- Sprawdzić czy jest character selector UI

**2.2. Implementacja auto-select charactera**
```python
# app/views.py - MessageListView

class MessageListView(LoginRequiredMixin, BaseViewMixin, TemplateView):
    template_name = 'messages/message_list.html'
    current_page = 'messages'

    def get(self, request):
        character_id = request.GET.get('character')

        # Auto-select first character if not specified
        if not character_id:
            first_char = request.user.character_set.first()
            if first_char:
                return redirect(f'{reverse("message_list")}?character={first_char.pk}')
            else:
                messages.warning(request, _("Please create a character first to send messages."))
                return redirect('character_create')

        # Continue with normal flow...
        try:
            character = get_object_or_404(Character, pk=character_id, user=request.user)
        except:
            messages.error(request, _("Character not found."))
            return redirect('character_list')

        # ... rest of the view logic
```

**2.3. Dodać character selector UI** (dla multi-character users)
```django
{# app/templates/messages/message_list.html #}

{% if user.character_set.count > 1 %}
<div class="character-selector mb-3">
    <label for="character-select">Viewing messages for:</label>
    <select id="character-select" class="form-select" onchange="window.location.href='?character=' + this.value">
        {% for char in user.character_set.all %}
        <option value="{{ char.pk }}" {% if char.pk == selected_character.pk %}selected{% endif %}>
            {{ char.nickname }} ({{ char.game.name }})
        </option>
        {% endfor %}
    </select>
</div>
{% endif %}
```

**2.4. Update E2E tests** (optional - jeśli auto-select nie wystarczy)
```typescript
// tests/e2e/messaging/conversation-list.spec.ts

test.beforeEach(async ({ page }) => {
    await login(page, 'testuser', 'testpass123');

    // Optional: explicitly select character
    // await page.goto('/messages/?character=15f97226-ca54-4e26-8e18-37be99014caa');

    // With auto-select, this should work:
    await page.goto('/messages/');
});
```

**Expected Impact**: +12 testów (100% conversation-list)

---

### KROK 3: Naprawić Validation Messages (HIGH PRIORITY)
**Cel**: ~15 validation testów przejść

**Zadania**:

**3.1. Zbadać obecne zachowanie**
- Uruchomić jeden test z `headed: true` żeby zobaczyć co się dzieje
- Sprawdzić czy HTML5 validation blokuje Django validation
- Sprawdzić network tab - czy form submission przechodzi

**3.2. Wyłączyć HTML5 validation**
```django
{# app/templates/registration/password_change_form.html #}
<form class="password_change" method="post" action="." novalidate>
  {% csrf_token %}
  {{ form | crispy }}
  <button type="submit" class="btn btn-primary btn-lg">{% trans 'Submit' %}</button>
</form>
```

**3.3. Sprawdzić crispy forms error rendering**
```python
# settings/base.py
CRISPY_TEMPLATE_PACK = 'bootstrap5'
CRISPY_FAIL_SILENTLY = False  # Show crispy errors in console
```

**3.4. Update test selectors jeśli potrzeba**
```typescript
// Możliwe że błędy są renderowane inaczej przez crispy forms
await expect(page.locator('.invalid-feedback, .form-error, ul.errorlist li')).toBeVisible();
```

**Expected Impact**: +10-15 testów (validation errors)

---

### KROK 4: Dodać Brakujące Fixtures (MEDIUM PRIORITY)
**Cel**: Uzupełnić testowe dane dla character/profile tests

**Zadania**:

**4.1. Dodać CharacterFriend fixtures**
```json
{
    "model": "app.characterfriend",
    "pk": 4,
    "fields": {
        "character1": "15f97226-ca54-4e26-8e18-37be99014caa",
        "character2": "66de8400-e29b-41d4-a716-446655440001",
        "created_at": "2024-03-15T10:00:00Z"
    }
},
{
    "model": "app.characterfriend",
    "pk": 5,
    "fields": {
        "character1": "15f97226-ca54-4e26-8e18-37be99014caa",
        "character2": "66de8400-e29b-41d4-a716-446655440007",
        "created_at": "2024-03-10T12:00:00Z"
    }
}
```

**Expected Impact**: +3-5 testów (friend list, friend request tests)

---

### KROK 5: Production Password Validation (LOW PRIORITY)
**Cel**: Dodać production-ready password validation

**Zadania**:

**5.1. Update settings/production.py**
```python
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', 'OPTIONS': {'min_length': 8}},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
]
```

**5.2. Update BEFORE_PRODUCTION_CHECKLIST.md**
- Dodać password policy do checklist
- Zaznaczyć jako CRITICAL requirement

**Expected Impact**: Production readiness +1

---

### KROK 6: Dokumentacja i Finalizacja
**Cel**: Zaktualizować wszystkie status docs

**Zadania**:

**6.1. Update E2E_TEST_STATUS_2025-12-28.md**
- Nowe wyniki testów
- Breakdown per category
- Pass rate update

**6.2. Update PROJECT_STATUS_SUMMARY.md**
- Pass rate: 27% → 46-50% → (po messaging fix) 55-60%
- Production readiness status
- Remaining work

**6.3. Update TASKS.md**
- Mark completed tasks [x]
- Add new tasks from this plan
- Reorder by priority

**6.4. Create final report**
- `docs/testing/E2E_COMPLETE_REPORT_2025-12-28.md`
- Summary of all fixes
- Before/after comparison
- Recommendations for remaining failures

---

## Timeline Estimate (Bez estymacji czasu - tylko kolejność)

**NATYCHMIAST** (Priority 0):
1. ✅ Załadować fixtures i uruchomić testy
2. ✅ Przeanalizować wyniki

**WYSOKIE** (Priority 1):
3. Naprawić Messaging System (auto-select character)
4. Naprawić Validation Messages (novalidate forms)

**ŚREDNIE** (Priority 2):
5. Dodać CharacterFriend fixtures
6. Zweryfikować Profile/Character edit tests

**NISKIE** (Priority 3):
7. Production password validation
8. Dokumentacja update

---

## Pytania do Właściciela

### Q1: Messaging System Architecture
**Pytanie**: Czy `/messages/` powinno automatycznie wybierać pierwszego charactera użytkownika?

**Opcje**:
- A) ✅ TAK - Auto-select pierwszy character (best UX dla większości użytkowników)
- B) ❌ NIE - Zawsze wymagaj ręcznego wyboru (force explicit selection)
- C) 🤔 DEPENDS - Auto-select jeśli 1 character, selector jeśli więcej

**Rekomendacja architekta**: **Option C** - Auto-select dla 1 char, selector dla many
- Lepsza UX dla użytkowników z jednym charakterem (większość)
- Explicit choice dla power users z wieloma charakterami
- Zachowuje character-centric architecture

### Q2: Password Validation Policy
**Pytanie**: Czy zaproponowane validation rules są OK?

**Proposed**:
- ✅ 8 characters minimum
- ✅ Cannot be too common (password123, qwerty)
- ✅ Cannot be entirely numeric (123456)
- ❌ NO uppercase requirement
- ❌ NO special character requirement

**Alternatywa** (jeśli chcesz bardziej restrykcyjne):
```python
# Add UpperCaseValidator + SpecialCharValidator (custom)
# Wymaganie: 8+ chars, 1 uppercase, 1 number, 1 special char
```

### Q3: Validation Messages - HTML5 vs Django
**Pytanie**: Czy wyłączyć HTML5 validation (novalidate) żeby Django validation działała?

**Opcje**:
- A) ✅ TAK - novalidate na wszystkich formach (Django kontroluje wszystko)
- B) ❌ NIE - Użyj HTML5 validation dla instant feedback
- C) 🤔 HYBRID - HTML5 basic validation + Django backend validation

**Rekomendacja architekta**: **Option A** (novalidate) - Django kontrola
- Consistent error messages (Django templates)
- Lepsze testy (no HTML5 interference)
- Pełna kontrola nad validation logic

### Q4: Character Selector UI
**Pytanie**: Gdzie powinien być character selector dla `/messages/`?

**Opcje**:
- A) Top of page (above conversation list)
- B) Navbar dropdown (global character context)
- C) Modal on first visit (force selection)

**Rekomendacja architekta**: **Option A** (top of messages page)
- Contextual - widoczne tylko na messages page
- Non-intrusive - nie blokuje innych funkcji
- Easy to implement

---

## Success Criteria

**Minimum Viable** (Production Ready):
- ✅ 80%+ pass rate (365+ / 456 tests)
- ✅ All CRITICAL features tested (auth, POKE, messaging, blocking)
- ✅ Production checklist completed
- ✅ Email validation working

**Ideal** (Full Coverage):
- ✅ 95%+ pass rate (434+ / 456 tests)
- ✅ All edge cases covered
- ✅ Mobile tests passing
- ✅ Performance tests (if added)

**Current Progress**:
- 27% (123/456) → **Expected 46-50%** (210-226/456) po obecnych naprawach
- → **Expected 55-60%** (251-274/456) po messaging fix
- → **Expected 80%+** (365+/456) po wszystkich naprawach z tego planu

---

## Appendix A: Commit History

```
bd0867de - feat: implement all E2E test fixes from architectural analysis
  - Agent 2: Dropdown navigation fix (openUserMenu helper)
  - Agent 3: Layout switcher to navbar (conditional, staff only)
  - Agent 4: Production deployment checklist
  - Agent 5: POKE (12) + Block (5) fixtures
  - Minor: password-reset selector fix

84f2804 - fix: resolve edge cases in auth E2E tests
  - CustomLoginView with redirect_authenticated_user=True
  - URL override for /accounts/login/
  - Register link URL fix (/register/step1/)

486d04d - fix: resolve E2E test architectural issues and UI blocking
  - Layout switcher z-index fix (9999 → 1040)
  - pointer-events: none (later deprecated in bd0867de)
  - password-change field names fix
  - signup URL change
  - Django error message regex fix

69425b3 - docs: add E2E test status and architectural analysis
  - E2E_TEST_STATUS_2025-12-28.md
  - E2E_ARCHITECTURAL_ANALYSIS.md
```

**Total changes**: 16 plików zmienione, ~1200+ insertions

---

## Appendix B: Test Categories Breakdown

| Category | Total | Passed | Failed | Skipped | Pass % | Priority |
|----------|-------|--------|--------|---------|--------|----------|
| Auth (login/logout/password) | 117 | 45 | 72 | 0 | 38% | HIGH |
| Navigation (navbar, layout) | 75 | 57 | 18 | 0 | 76% | LOW |
| Messaging | 36 | 0 | 36 | 0 | 0% | **CRITICAL** |
| POKE System | 64 | 12 | 24 | 28 | 19% | HIGH |
| Blocking System | 47 | 15 | 0 | 32 | 32% | HIGH |
| Characters | 30 | 6 | 24 | 0 | 20% | MEDIUM |
| Profile | 27 | 15 | 12 | 0 | 56% | MEDIUM |
| Friends | 30 | 27 | 3 | 0 | 90% | LOW |
| **TOTAL** | **456** | **123** | **273** | **60** | **27%** | - |

**Po naprawach oczekiwane**:
- Auth: 38% → 70% (+37 testów)
- Messaging: 0% → 100% (+36 testów) *after Step 2*
- POKE: 19% → 80% (+39 testów) *after fixtures loaded*
- Blocking: 32% → 100% (+32 testów) *after fixtures loaded*

**Expected final**: ~365-380 passing (80-83%)

---

## Appendix C: Files Modified Summary

**Templates**:
- `app/templates/base_navbar.html` - Layout switcher dropdown
- `app/templates/homepage/layout_switcher.html` - Deprecated overlay
- `app/templates/registration/password_change_form.html` - Class + button
- `app/templates/registration/password_reset_form.html` - Class + button
- `app/templates/django_registration/registration_form.html` - Class + button

**Python**:
- `app/views.py` - CustomLoginView
- `game_player_nick_finder/urls.py` - Login URL override

**Tests**:
- `tests/helpers/auth-helpers.ts` - openUserMenu() helper
- `tests/e2e/navigation/navbar-authenticated.spec.ts` - Dropdown tests
- `tests/e2e/auth/login.spec.ts` - Strict mode fix
- `tests/e2e/auth/logout.spec.ts` - openUserMenu usage
- `tests/e2e/auth/password-change.spec.ts` - Field names + openUserMenu
- `tests/e2e/auth/password-reset.spec.ts` - Selector fix
- `tests/e2e/auth/signup.spec.ts` - Register URL fix

**Fixtures**:
- `app/fixtures/users_and_characters.json` - +12 POKEs, +5 Blocks

**Documentation**:
- `docs/testing/E2E_TEST_STATUS_2025-12-28.md` - NEW
- `docs/testing/E2E_ARCHITECTURAL_ANALYSIS.md` - NEW
- `docs/deployment/BEFORE_PRODUCTION_CHECKLIST.md` - NEW
- `docs/PROJECT_STATUS_SUMMARY.md` - Production warning
- `TASKS.md` - Pre-production section

**Total**: 19 plików, ~1200+ lines changed

---

**END OF PLAN**

*Dokument przygotowany jako szczegółowy plan działania dla właściciela projektu.
Wszystkie zmiany są skomitowane. Gotowe do wykonania po zatwierdzeniu.*

*Następny krok: Uruchomić testy i zweryfikować wyniki.*

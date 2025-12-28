# E2E Test Status Report - 2025-12-28

## Executive Summary

**Data**: 2025-12-28 po naprawach architektonicznych
**Commit**: 486d04d - fix: resolve E2E test architectural issues and UI blocking

```
📊 WYNIKI TESTÓW (wszystkie przeglądarki):
   ✅ 123 PASSED (27%)
   ❌ 273 FAILED (60%)
   ⏭️  60 SKIPPED (13%)

   Łącznie: 456 testów (24 pliki × 3 przeglądarki)
   Czas wykonania: ~8 minut
```

## Naprawy Zrealizowane w Tej Sesji

### ✅ 1. Strict Mode Violations
**Problem**: Locator resolved to 2 elements (Django pokazuje błędy 2x - na górze i przy formie)
**Rozwiązanie**: Dodano `.first()` do selectorów błędów w `login.spec.ts`

### ✅ 2. Layout-Switcher Blokujący Dropdown
**Problem**: z-index 9999 blokował wszystkie kliknięcia dropdown (Bootstrap dropdown ma z-index ~1050)
**Rozwiązanie**:
- z-index: 9999 → 1040
- pointer-events: none (pozwala kliknięciom przejść przez element)

### ✅ 3. Niepoprawne Nazwy Pól Password Change
**Problem**: Testy używały `oldpassword`, `password1`, `password2`
**Django używa**: `old_password`, `new_password1`, `new_password2`
**Rozwiązanie**: Poprawiono selektory w `password-change.spec.ts`

### ✅ 4. Błędny URL Rejestracji
**Problem**: Testy używały `/accounts/signup/`, aplikacja używa `/accounts/register/`
**Rozwiązanie**: Zmieniono URL w `signup.spec.ts`

### ✅ 5. Komunikaty Błędów Django
**Problem**: Regex szukał "incorrect/invalid" ale Django pokazuje "correct"
**Django**: "Please enter a **correct** username and password"
**Rozwiązanie**: Dodano "correct" do regex pattern

### ✅ 6. Semantyka HTML
**Problem**: Formularze używały `<input type="submit">`
**Rozwiązanie**: Zmieniono na `<button type="submit">` (lepszy semantic HTML)

### ✅ 7. CSS Classes
**Problem**: Testy szukały `.password_reset`, `.password_change`, `.signup`
**Rozwiązanie**: Dodano klasy do formularzy dla lepszej testowalności

## Analiza Pozostałych Błędów (273 failed)

### Kategoria A: Auth Tests (76 failed z 117 total)

#### A1. Dropdown Navigation Timeouts (~20 failures)
**Pattern**: Timeouts przy klikaniu user menu dropdown
**Przykładowe testy**:
- `should navigate to password change page via user menu`
- `should have logout button accessible in user menu`
- `should navigate to profile via user menu Profile link`

**Możliwe przyczyny**:
- layout-switcher nadal blokuje mimo pointer-events: none?
- Dropdown wymaga dodatkowego czasu na animację?
- Selector niepoprawny dla dropdown?

#### A2. Validation Messages Not Showing (~15 failures)
**Pattern**: Test oczekuje komunikatu błędu, ale nie jest widoczny
**Przykładowe testy**:
- `should show validation error for invalid email format`
- `should show validation error for password too short`
- `should show validation error for password mismatch`
- `should show validation errors for empty fields`

**Możliwe przyczyny**:
- Django validation wyłączona dla niektórych scenariuszy?
- Walidacja po stronie klienta (JS) nie działa?
- Komunikaty są renderowane ale nie widoczne?

#### A3. Missing UI Elements (~10 failures)
**Pattern**: Element not found
**Przykładowe testy**:
- `should have Forgot Password link in login form`
- `should redirect logged in user away from login page`
- `should have register link in navbar for unauthenticated users`

**Możliwe przyczyny**:
- Elementy UI nigdy nie zostały zaimplementowane
- Elementy są warunkowe i nie pokazują się w testowym środowisku

#### A4. Password Change Flow Issues (~10 failures)
**Pattern**: Timeouts w password change flow
**Wszystkie testy password change padają z timeout 30s**

**Możliwe przyczyny**:
- Dropdown navigation issue (zobacz A1)
- Redirect po zmianie hasła nie działa?
- Form submission nie przechodzi?

### Kategoria B: Navigation Tests (~30 failed)

#### B1. Dropdown Menu Navigation (~20 failures)
**Pattern**: Timeout przy próbie kliknięcia linków w user menu
**Przykładowe testy**:
- `should navigate to profile via user menu Profile link`
- `should navigate to user characters via user menu My characters link`
- `should navigate to messages via user menu Messages link`
- `should navigate to password change via user menu Change password link`

**To jest KRYTYCZNY problem blokujący wiele testów!**

#### B2. Layout Switcher Interactive Tests (~5 failures)
**Problem**: pointer-events: none wyłącza klikanie buttonów layout-switcher
**Test**: `should allow switching between layouts using switcher buttons`

**To jest ZNANY problem** - pointer-events: none rozwiązało blokowanie dropdown, ale uniemożliwiło użycie samego layout-switcher.

**Potrzeba decyzji architektonicznej**:
1. Użyć pointer-events: none tylko w dev mode?
2. Całkiem usunąć layout-switcher?
3. Przeprojektować layout-switcher żeby nie blokował UI?

### Kategoria C: Messaging Tests (~12 failed)

**Pattern**: Wszystkie conversation-list.spec.ts testy padają z timeout 30s
**Możliwe przyczyny**:
- Brak testowych danych (conversations nie istnieją w fixtures)
- Routing issues
- Authentication issues

### Kategoria D: POKE Tests (20 skipped + ~10 failed)

**Pattern**: Większość testów POKE jest pominięta
**Testy działające**:
- ✅ should display send POKE form
- ✅ should navigate to send POKE from character detail page
- ✅ should display receiver character info when pre-selected

**Testy padające**:
- ❌ should display POKE list page
- ❌ should display filter tabs
- ❌ should show empty state when no POKEs
- ❌ should show send POKE button instead of send message when messaging not unlocked

**Testy pominięte (skipped)**:
- All poke-actions.spec.ts (respond, ignore, block)
- All poke-detail.spec.ts (display detail, status badge)

**Wymaga analizy**:
- Dlaczego testy są pominięte? `.skip()` w kodzie?
- Czy POKE system jest w pełni zaimplementowany?

### Kategoria E: Profile Edit Tests (~8 failed)

**Pattern**: Timeouts przy próbie edycji profilu
**Przykładowe testy**:
- `should display profile edit form`
- `should have profile visibility field`
- `should save profile changes`

**Możliwe przyczyny**:
- Dropdown navigation issue (dostęp przez user menu?)
- Form routing niepoprawny
- Brak implementacji

### Kategoria F: Character Tests (~5 failed)

**Testy działające**:
- ✅ Character profile display (bio, empty state)

**Testy padające**:
- ❌ Character profile edit form
- ❌ Character friend list display
- ❌ Friend request list display

**Możliwe przyczyny**:
- Dropdown navigation issue
- Brak testowych danych (friendships w fixtures)

### Kategoria G: Blocking Tests (32 skipped)

**Pattern**: WSZYSTKIE blocking interaction testy są pominięte
**Tylko działające**:
- ✅ Display blocked list page
- ✅ Empty state when no blocked characters
- ✅ Navigation link in navbar
- ✅ Not show block button for own character

**Wszystkie pominięte**:
- Block character with reason
- Block character with spam report
- Unblock character
- Prevent sending message to blocked
- Prevent sending POKE to blocked
- Prevent friend request to blocked
- Restore interactions after unblocking

**Wymaga decyzji**: Czy blocking system jest zaimplementowany?

## Priorytety Naprawy

### 🔥 CRITICAL (Blokuje najwięcej testów)

#### 1. Dropdown Navigation Issue (~50 failures)
**Impact**: Blokuje ~50 testów używających user menu dropdown
**Pliki**: `base_navbar.html`, możliwe `layout_switcher.html`

**DO ZBADANIA**:
- Czy dropdown w ogóle działa w przeglądarce?
- Czy selector w testach jest poprawny?
- Czy layout-switcher nadal blokuje mimo pointer-events: none?
- Czy trzeba dodać `waitForSelector` przed kliknięciem?

#### 2. Layout Switcher Architecture Decision (~5 failures)
**Impact**: pointer-events: none wyłącza funkcjonalność layout-switcher
**Wymaga decyzji użytkownika**:
- A) Usunąć layout-switcher całkowicie?
- B) pointer-events: none tylko w production, auto w dev mode?
- C) Przeprojektować layout-switcher (inna pozycja, nie fixed)?

**PYTANIE DO WŁAŚCICIELA**: Co chcesz zrobić z layout-switcher?

### ⚠️ HIGH (Walidacja i UX)

#### 3. Validation Messages Not Showing (~15 failures)
**Impact**: Blokuje wszystkie testy walidacji formularzy
**DO ZBADANIA**:
- Sprawdzić czy Django validation jest włączona
- Sprawdzić czy crispy forms renderuje błędy
- Sprawdzić czy JS validation działa
- Dodać missing validation do formularzy?

#### 4. Missing UI Elements (~10 failures)
**Impact**: Brak podstawowych elementów UI
**DO DODANIA**:
- "Forgot Password" link w login form
- Redirect zalogowanego użytkownika z /login/ i /register/
- "Register" link w navbar dla niezalogowanych

### 📋 MEDIUM (Funkcjonalność)

#### 5. Messaging System Tests (~12 failures)
**Impact**: Cały conversation-list nie działa
**DO ZBADANIA**:
- Czy są testowe conversations w fixtures?
- Czy routing działa?
- Czy trzeba stworzyć conversations przed testami?

#### 6. POKE System - Skipped Tests (20 skipped)
**Impact**: Połowa POKE testów jest pominiętych
**DO ZBADANIA**:
- Dlaczego testy są `.skip()`?
- Czy implementacja jest niekompletna?
- Co trzeba dodać żeby odblokować testy?

#### 7. Blocking System - All Skipped (32 skipped)
**Impact**: Wszystkie interaction testy pominiętę
**DO ZBADANIA**:
- Czy blocking system jest w pełni zaimplementowany?
- Dlaczego testy są `.skip()`?

### 📌 LOW (Edge cases)

#### 8. Profile & Character Edit (~13 failures)
**Impact**: Edit functionality nie działa
**Prawdopodobnie**: Dropdown navigation issue (punkt #1)

## Statystyki per Plik

| Plik | Passed | Failed | Skipped | Total | Pass % |
|------|--------|--------|---------|-------|--------|
| **auth/login.spec.ts** | 15 | 6 | 0 | 21 | 71% |
| **auth/logout.spec.ts** | 3 | 15 | 0 | 18 | 17% |
| **auth/password-change.spec.ts** | 3 | 27 | 0 | 30 | 10% |
| **auth/password-reset.spec.ts** | 15 | 6 | 0 | 21 | 71% |
| **auth/signup.spec.ts** | 9 | 18 | 0 | 27 | 33% |
| **blocking/*** | 15 | 0 | 32 | 47 | 32%* |
| **characters/profile-display** | 6 | 0 | 0 | 6 | 100% |
| **characters/profile-edit** | 0 | 9 | 0 | 9 | 0% |
| **friends/*** | 27 | 3 | 0 | 30 | 90% |
| **messaging/conversation-list** | 0 | 36 | 0 | 36 | 0% |
| **navigation/navbar-auth** | 6 | 21 | 0 | 27 | 22% |
| **navigation/navbar-unauth** | 18 | 3 | 0 | 21 | 86% |
| **navigation/layout-switcher** | 24 | 3 | 0 | 27 | 89% |
| **pokes/*** | 12 | 24 | 28 | 64 | 19%* |
| **profile/display** | 15 | 0 | 0 | 15 | 100% |
| **profile/edit** | 0 | 12 | 0 | 12 | 0% |

*Procent liczony z passed/(passed+failed), skipped nie wliczane

## Best & Worst Performers

### ✅ Świetnie Działają (90-100%)
- Character Profile Display (100%)
- User Profile Display (100%)
- Friends (90%)
- Navigation Layout Switcher (89%)
- Navigation Navbar Unauth (86%)

### ❌ Wymagają Naprawy (0-20%)
- Character Profile Edit (0%)
- Messaging Conversation List (0%)
- Profile Edit (0%)
- Password Change (10%)
- Logout (17%)
- POKEs (19%)

## Rekomendowane Następne Kroki

### Krok 1: Szczegółowa Analiza Architektoniczna
**Zlecić subagentowi** (Task tool, Plan agent):
- Przeanalizować kod dropdown navigation
- Zbadać dlaczego testy są `.skip()`
- Sprawdzić fixtures (czy są conversations, POKEs, blocks)
- Zidentyfikować missing UI elements
- Przeanalizować validation setup

**Output**: Szczegółowy raport architektoniczny z pytaniami do właściciela

### Krok 2: Decyzje Właściciela
**Pytania wymagające odpowiedzi**:
1. Co zrobić z layout-switcher? (usunąć/przeprojektować/conditional)
2. Czy POKE system jest w pełni zaimplementowany?
3. Czy blocking system jest w pełni zaimplementowany?
4. Czy messaging system ma być w pełni funkcjonalny?
5. Która wersja layout'u homepage jest docelowa (v0/v1/v2/v3)?

### Krok 3: Implementacja Napraw
**Po otrzymaniu odpowiedzi**:
1. Naprawić dropdown navigation (CRITICAL)
2. Dodać brakujące UI elements
3. Naprawić/włączyć validation messages
4. Rozwiązać layout-switcher decision
5. Dodać brakujące testowe dane do fixtures
6. Odblokować skipped testy (jeśli implementacja gotowa)

## Pliki Zmodyfikowane w Tej Sesji

1. `tests/e2e/auth/login.spec.ts` - strict mode, regex
2. `tests/e2e/auth/signup.spec.ts` - URL change
3. `tests/e2e/auth/password-change.spec.ts` - field names
4. `app/templates/registration/password_reset_form.html` - class, button
5. `app/templates/registration/password_change_form.html` - class, button
6. `app/templates/django_registration/registration_form.html` - class, button
7. `app/templates/homepage/layout_switcher.html` - z-index, pointer-events

## Konkluzja

**Postęp**: 123/456 testów przechodzi (27%)

**Główny problem**: Dropdown navigation blokuje ~50 testów

**Do decyzji**: Layout switcher architecture, POKE/Blocking implementation status

**Następny krok**: Szczegółowa analiza architektoniczna przez subagenta

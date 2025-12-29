# Plan Przywrócenia Allauth Login - Architektura i Taski

**Data**: 2025-12-30  
**Typ**: Architectural Implementation Plan  
**Status**: Planning  
**Priorytet**: High

---

## 📋 EXECUTIVE SUMMARY

**Cel**: Przywrócenie systemu logowania allauth jako jedynej metody autentykacji, usunięcie standardowego Django login (CustomLoginView) i aktualizacja wszystkich testów E2E do allauth.

**Motywacja**: 
- Allauth jest już skonfigurowany w INSTALLED_APPS i settings
- Allauth zapewnia lepsze funkcje (social providers, email verification, etc.)
- Uproszczenie architektury - jeden system autentykacji zamiast dwóch

**Zakres zmian**:
- Backend: URLs, Views, Templates
- Frontend: Selektory CSS w testach
- Testy: Aktualizacja wszystkich E2E testów do allauth

---

## 🏗️ ARCHITEKTURA - OBECNY STAN vs DOCELOWY

### OBECNY STAN (Standardowy Django Login)

```
URLs:
  /accounts/login/ -> CustomLoginView (DjangoLoginView)
  
Template:
  registration/login.html
  - Base: base.html
  - Form field: username (id: #id_username)
  - Form action: action="."
  - URL name: login
  - Form: Django AuthenticationForm
  
View:
  CustomLoginView (app/views.py:1882)
  - redirect_authenticated_user = True
  - template_name = 'registration/login.html'
```

### DOCELOWY STAN (Allauth Login)

```
URLs:
  /accounts/login/ -> allauth LoginView (account_login)
  
Template:
  account/login.html
  - Base: account/base_display.html
  - Form field: login (id: #id_login) - może być username LUB email
  - Form action: {% url 'account_login' %}
  - URL name: account_login
  - Form: allauth LoginForm
  
View:
  allauth AccountLoginView (built-in)
  - redirect_authenticated_user = True (domyślnie w allauth)
  - template_name = 'account/login.html'
```

---

## 🔄 RÓŻNICE KRYTYCZNE DO ROZWAŻENIA

| Aspekt | Django Login (obecny) | Allauth Login (docelowy) |
|--------|----------------------|-------------------------|
| **Pole formularza** | `username` | `login` (może być username lub email) |
| **ID pola** | `#id_username` | `#id_login` |
| **Form action** | `action="."` | `action="{% url 'account_login' %}"` |
| **URL name** | `login` | `account_login` |
| **Template base** | `base.html` | `account/base_display.html` |
| **Form class** | `AuthenticationForm` | `LoginForm` (allauth) |
| **Redirect auth users** | `CustomLoginView.redirect_authenticated_user = True` | `ACCOUNT_EMAIL_VERIFICATION` setting |
| **Social providers** | ❌ Nie | ✅ Tak (jeśli skonfigurowane) |
| **Remember me** | Custom checkbox | Allauth remember field |

---

## 📦 TASKI IMPLEMENTACYJNE

### PHASE 1: Backend - Przywrócenie Allauth (PRIORITY: P0)

#### Task 1.1: Usunięcie CustomLoginView
**Developer**: Backend Developer  
**Estymacja**: 15 min  
**Status**: TODO

**Działania**:
1. Usunąć klasę `CustomLoginView` z `app/views.py` (linie 1879-1887)
2. Usunąć import `from django.contrib.auth.views import LoginView as DjangoLoginView` z `app/views.py`
3. Usunąć import `CustomLoginView` z `game_player_nick_finder/urls.py`

**Files to modify**:
- `app/views.py`
- `game_player_nick_finder/urls.py`

**Acceptance Criteria**:
- ✅ `CustomLoginView` nie istnieje w kodzie
- ✅ Import `CustomLoginView` usunięty z urls.py
- ✅ Brak błędów importu w aplikacji

---

#### Task 1.2: Odkomentowanie Allauth URLs
**Developer**: Backend Developer  
**Estymacja**: 5 min  
**Status**: TODO

**Działania**:
1. W `game_player_nick_finder/urls.py` odkomentować linię:
   ```python
   path('accounts/', include('allauth.urls')),
   ```
2. Usunąć komentarz z wyjaśnieniem konfliktu:
   ```python
   # DISABLED: allauth conflicts with django.contrib.auth
   ```
3. Usunąć override `/accounts/login/` z CustomLoginView (linia 73):
   ```python
   # USUŃ TĘ LINIĘ:
   path('accounts/login/', CustomLoginView.as_view(), name='login'),
   ```

**Files to modify**:
- `game_player_nick_finder/urls.py`

**Order of operations**:
1. Najpierw odkomentować `allauth.urls`
2. Potem usunąć CustomLoginView override
3. Upewnić się, że `django.contrib.auth.urls` jest PRZED `allauth.urls` (jeśli jest potrzebny dla innych URLi)

**Acceptance Criteria**:
- ✅ `path('accounts/', include('allauth.urls'))` jest aktywny
- ✅ Brak override `/accounts/login/` z CustomLoginView
- ✅ Aplikacja uruchamia się bez błędów URL conflicts

---

#### Task 1.3: Weryfikacja Allauth Settings
**Developer**: Backend Developer  
**Estymacja**: 10 min  
**Status**: TODO

**Działania**:
1. Sprawdzić `game_player_nick_finder/settings/base.py`:
   - ✅ `allauth` w INSTALLED_APPS (linia 17)
   - ✅ `allauth.account` w INSTALLED_APPS (linia 18)
   - ✅ `allauth.socialaccount` w INSTALLED_APPS (linia 19)
   - ✅ `allauth.account.middleware.AccountMiddleware` w MIDDLEWARE (linia 45)
   - ✅ `allauth.account.auth_backends.AuthenticationBackend` w AUTHENTICATION_BACKENDS (linia 105)
   - ✅ `ACCOUNT_EMAIL_VERIFICATION = 'none'` (linia 117)
   - ✅ `ACCOUNT_AUTHENTICATION_METHOD = 'username_email'` (linia 118)
   - ✅ `LOGIN_REDIRECT_URL = '/'` (linia 109)
   - ✅ `LOGIN_URL = '/accounts/login/'` (linia 110)

2. Sprawdzić czy `account/base_display.html` istnieje (wymagany przez `account/login.html`)

**Files to verify**:
- `game_player_nick_finder/settings/base.py`
- `app/templates/account/base_display.html`

**Acceptance Criteria**:
- ✅ Wszystkie wymagane allauth settings są skonfigurowane
- ✅ Template `account/base_display.html` istnieje
- ✅ Brak błędów konfiguracji przy starcie Django

---

#### Task 1.4: Usunięcie Standardowego Django Login Template
**Developer**: Backend Developer  
**Estymacja**: 5 min  
**Status**: TODO

**Działania**:
1. Usunąć plik `app/templates/registration/login.html`
2. Sprawdzić czy nie ma innych referencji do tego template w kodzie

**Files to delete**:
- `app/templates/registration/login.html`

**Files to check for references**:
- `app/views.py` (sprawdzić grep)
- `game_player_nick_finder/urls.py` (sprawdzić grep)
- Dokumentacja (opcjonalnie - można zostawić w historii)

**Acceptance Criteria**:
- ✅ Plik `registration/login.html` usunięty
- ✅ Brak referencji do `registration/login.html` w kodzie
- ✅ Brak broken imports/urls

---

#### Task 1.5: Weryfikacja Template account/login.html
**Developer**: Backend Developer  
**Estymacja**: 10 min  
**Status**: TODO

**Działania**:
1. Sprawdzić czy `app/templates/account/login.html` istnieje
2. Sprawdzić czy używa właściwych tagów:
   - ✅ `{% url 'account_login' %}` w form action
   - ✅ `{% extends "account/base_display.html" %}`
   - ✅ `{% load account %}` i `{% load socialaccount %}`
   - ✅ Form field z `id_login` (allauth używa `login`, nie `username`)
3. Przywrócić wersję z przed 28 grudnia jeśli została zmieniona (commit cb1a863)

**Files to verify**:
- `app/templates/account/login.html`

**Reference commit**: `cb1a863^` (wersja przed zmianami 28 grudnia)

**Acceptance Criteria**:
- ✅ Template `account/login.html` istnieje i jest poprawny
- ✅ Używa `{% url 'account_login' %}`
- ✅ Form field ma id `id_login` (nie `id_username`)
- ✅ Template extends `account/base_display.html`

---

### PHASE 2: Testy E2E - Aktualizacja Selektorów (PRIORITY: P0)

#### Task 2.1: Aktualizacja auth-helpers.ts
**Developer**: Frontend/QA Developer  
**Estymacja**: 30 min  
**Status**: TODO

**Działania**:
1. Zaktualizować selektory w `tests/helpers/auth-helpers.ts`:
   - Zmienić `#id_username` → `#id_login`
   - Zaktualizować komentarze (usunąć wzmianki o CustomLoginView)
   - Sprawdzić czy form action to `{% url 'account_login' %}` (nie `action="."`)

2. Zaktualizować logikę sprawdzania redirect:
   - Allauth ma `redirect_authenticated_user = True` domyślnie
   - Usunąć komentarze o CustomLoginView

**Files to modify**:
- `tests/helpers/auth-helpers.ts`

**Changes**:
```typescript
// BEFORE:
await expect(page.locator('#id_username')).toBeVisible({ timeout: 5000 });
await page.fill('#id_username', username);

// AFTER:
await expect(page.locator('#id_login')).toBeVisible({ timeout: 5000 });
await page.fill('#id_login', username);
```

**Acceptance Criteria**:
- ✅ Wszystkie selektory używają `#id_login` zamiast `#id_username`
- ✅ Komentarze o CustomLoginView usunięte
- ✅ Komentarze zaktualizowane do allauth
- ✅ Helper działa poprawnie (test manualny)

---

#### Task 2.2: Aktualizacja login.spec.ts
**Developer**: Frontend/QA Developer  
**Estymacja**: 45 min  
**Status**: TODO

**Działania**:
1. Zaktualizować wszystkie selektory w `tests/e2e/auth/login.spec.ts`:
   - `#id_username` → `#id_login`
   - `input[name="username"]` → `input[name="login"]`
   - Sprawdzić selektor formularza (`form.login` powinien działać dla allauth)

2. Zaktualizować test "Remember me":
   - Allauth używa `#id_remember` (sprawdzić w template)
   - Może być inne zachowanie niż standardowy Django

3. Zaktualizować test "redirect logged in user":
   - Allauth ma redirect_authenticated_user domyślnie
   - Upewnić się, że test działa poprawnie

**Files to modify**:
- `tests/e2e/auth/login.spec.ts`

**Changes**:
```typescript
// BEFORE:
await expect(page.locator('#id_username')).toBeVisible();
await page.fill('#id_username', TEST_USERS.main.username);

// AFTER:
await expect(page.locator('#id_login')).toBeVisible();
await page.fill('#id_login', TEST_USERS.main.username);
```

**Acceptance Criteria**:
- ✅ Wszystkie selektory używają `#id_login`
- ✅ Wszystkie testy w login.spec.ts przechodzą
- ✅ Test "Remember me" działa poprawnie
- ✅ Test "redirect logged in user" działa poprawnie

---

#### Task 2.3: Aktualizacja password-reset.spec.ts
**Developer**: Frontend/QA Developer  
**Estymacja**: 20 min  
**Status**: TODO

**Działania**:
1. Sprawdzić czy `tests/e2e/auth/password-reset.spec.ts` używa selektorów związanych z loginem
2. Zaktualizować selektory jeśli potrzeba:
   - Sprawdzić czy password reset używa allauth (`account_reset_password`)
   - Sprawdzić czy linki "Forgot Password" używają `{% url 'account_reset_password' %}`

**Files to modify**:
- `tests/e2e/auth/password-reset.spec.ts` (jeśli potrzeba)

**Acceptance Criteria**:
- ✅ Password reset testy używają właściwych URL names (account_reset_password)
- ✅ Wszystkie testy w password-reset.spec.ts przechodzą

---

#### Task 2.4: Aktualizacja password-change.spec.ts
**Developer**: Frontend/QA Developer  
**Estymacja**: 20 min  
**Status**: TODO

**Działania**:
1. Sprawdzić czy `tests/e2e/auth/password-change.spec.ts` używa selektorów związanych z loginem
2. Zaktualizować selektory jeśli potrzeba
3. Sprawdzić czy używa allauth URL names (`account_change_password`)

**Files to modify**:
- `tests/e2e/auth/password-change.spec.ts` (jeśli potrzeba)

**Acceptance Criteria**:
- ✅ Password change testy używają właściwych URL names
- ✅ Wszystkie testy w password-change.spec.ts przechodzą

---

#### Task 2.5: Aktualizacja signup.spec.ts
**Developer**: Frontend/QA Developer  
**Estymacja**: 20 min  
**Status**: TODO

**Działania**:
1. Sprawdzić czy `tests/e2e/auth/signup.spec.ts` używa linków do login
2. Zaktualizować jeśli potrzeba:
   - Sprawdzić czy link "Log in" prowadzi do `/accounts/login/` (allauth)
   - Sprawdzić czy używa właściwych selektorów

**Files to modify**:
- `tests/e2e/auth/signup.spec.ts` (jeśli potrzeba)

**Acceptance Criteria**:
- ✅ Signup testy używają właściwych URL names
- ✅ Wszystkie testy w signup.spec.ts przechodzą

---

#### Task 2.6: Aktualizacja navigation testów
**Developer**: Frontend/QA Developer  
**Estymacja**: 30 min  
**Status**: TODO

**Działania**:
1. Sprawdzić `tests/e2e/navigation/navbar-unauthenticated.spec.ts`:
   - Sprawdzić czy link "Log in" prowadzi do `/accounts/login/`
   - Sprawdzić czy używa właściwych selektorów

2. Sprawdzić `tests/e2e/navigation/navbar-authenticated.spec.ts`:
   - Sprawdzić czy logout działa poprawnie z allauth
   - Sprawdzić czy używa właściwych URL names (`account_logout`)

**Files to modify**:
- `tests/e2e/navigation/navbar-unauthenticated.spec.ts` (jeśli potrzeba)
- `tests/e2e/navigation/navbar-authenticated.spec.ts` (jeśli potrzeba)

**Acceptance Criteria**:
- ✅ Navigation testy używają właściwych URL names
- ✅ Wszystkie testy w navigation/*.spec.ts przechodzą

---

#### Task 2.7: Uruchomienie pełnej suity testów
**Developer**: QA Developer / DevOps  
**Estymacja**: 60 min  
**Status**: TODO

**Działania**:
1. Uruchomić pełną suitę testów E2E:
   ```bash
   npm run test:e2e
   # lub
   npx playwright test
   ```

2. Sprawdzić wyniki:
   - Sprawdzić ile testów przechodzi
   - Sprawdzić czy są błędy związane z selektorami login
   - Naprawić wszystkie błędy związane z allauth

3. Zweryfikować wszystkie auth-related testy:
   - `auth/login.spec.ts`
   - `auth/logout.spec.ts`
   - `auth/password-change.spec.ts`
   - `auth/password-reset.spec.ts`
   - `auth/signup.spec.ts`
   - `navigation/*.spec.ts`

**Acceptance Criteria**:
- ✅ Wszystkie auth-related testy przechodzą (100%)
- ✅ Brak błędów związanych z selektorami `#id_username`
- ✅ Brak błędów związanych z URL names (`login` vs `account_login`)

---

### PHASE 3: Cleanup i Dokumentacja (PRIORITY: P1)

#### Task 3.1: Usunięcie starych dokumentów
**Developer**: Technical Writer / Developer  
**Estymacja**: 15 min  
**Status**: TODO

**Działania**:
1. Przeszukać dokumentację i usunąć/przeaktualizować:
   - Wzmianki o CustomLoginView
   - Wzmianki o `registration/login.html`
   - Wzmianki o konfliktach allauth vs django.contrib.auth
   - Dokumenty które opisują standardowy Django login jako główny

2. Przeszukać komentarze w kodzie:
   - Usunąć komentarze `# rmme` związane z login
   - Usunąć komentarze o "DISABLED: allauth conflicts"

**Files to check**:
- `docs/testing/*.md`
- `docs/STATUS_REPORT.md`
- `game_player_nick_finder/urls.py` (komentarze)
- `app/views.py` (komentarze)

**Acceptance Criteria**:
- ✅ Brak wzmianek o CustomLoginView w dokumentacji (lub są oznaczone jako deprecated)
- ✅ Dokumentacja opisuje allauth jako główny system autentykacji
- ✅ Komentarze w kodzie są aktualne

---

#### Task 3.2: Aktualizacja LOGIN_REGISTRATION_CHANGES_ANALYSIS.md
**Developer**: Technical Writer  
**Estymacja**: 10 min  
**Status**: TODO

**Działania**:
1. Zaktualizować `LOGIN_REGISTRATION_CHANGES_ANALYSIS.md`:
   - Dodać sekcję "RESTORED" na końcu
   - Opisać że allauth został przywrócony
   - Dodać datę przywrócenia

**Files to modify**:
- `LOGIN_REGISTRATION_CHANGES_ANALYSIS.md`

**Acceptance Criteria**:
- ✅ Dokument opisuje przywrócenie allauth
- ✅ Historia zmian jest kompletna

---

#### Task 3.3: Weryfikacja importów i zależności
**Developer**: Backend Developer  
**Estymacja**: 10 min  
**Status**: TODO

**Działania**:
1. Sprawdzić czy wszystkie importy są poprawne:
   - Brak importów `CustomLoginView`
   - Brak nieużywanych importów `django.contrib.auth.views`

2. Sprawdzić czy `django.contrib.auth.urls` jest nadal potrzebny:
   - Jeśli używany tylko dla password reset/change, zostawić
   - Jeśli nieużywany, można usunąć (ale tylko jeśli na pewno nie jest potrzebny)

**Files to check**:
- `game_player_nick_finder/urls.py`
- `app/views.py`

**Acceptance Criteria**:
- ✅ Brak nieużywanych importów
- ✅ Wszystkie importy są poprawne
- ✅ Brak błędów lint/type checking

---

## 🔍 KRYTYCZNE PUNKTY DO SPRAWDZENIA

### 1. Konflikty URL
**Problem**: `django.contrib.auth.urls` i `allauth.urls` mogą mieć konfliktujące URL names.

**Rozwiązanie**:
- `allauth.urls` powinien być PO `django.contrib.auth.urls` jeśli oba są potrzebne
- Albo całkowicie usunąć `django.contrib.auth.urls` jeśli nie jest potrzebny
- Sprawdzić które URL names są używane w kodzie

**URL names do sprawdzenia**:
- `login` vs `account_login` ✅ (allauth używa `account_login`)
- `logout` vs `account_logout` ✅ (allauth używa `account_logout`)
- `password_reset` vs `account_reset_password` ✅ (allauth używa `account_reset_password`)
- `password_change` vs `account_change_password` ✅ (allauth używa `account_change_password`)

**Action**: Sprawdzić wszystkie użycia URL names w kodzie i templates.

---

### 2. Redirect Authenticated Users
**Problem**: CustomLoginView miał `redirect_authenticated_user = True`, trzeba upewnić się że allauth też to robi.

**Rozwiązanie**:
- Allauth ma `redirect_authenticated_user = True` domyślnie
- Sprawdzić czy działa poprawnie po przywróceniu

**Test**: Zalogować się i próbować wejść na `/accounts/login/` - powinien być redirect.

---

### 3. Form Field Name
**Problem**: Django używa `username`, allauth używa `login`.

**Rozwiązanie**:
- Wszystkie selektory w testach muszą używać `#id_login`
- Sprawdzić czy template używa właściwego field name

**Critical**: To jest najważniejsza zmiana w testach!

---

### 4. Template Base
**Problem**: `registration/login.html` używa `base.html`, `account/login.html` używa `account/base_display.html`.

**Rozwiązanie**:
- Upewnić się, że `account/base_display.html` istnieje
- Sprawdzić czy wszystkie bloki są poprawnie zdefiniowane

---

### 5. Social Providers
**Problem**: Allauth ma obsługę social providers, standardowy Django nie.

**Rozwiązanie**:
- Sprawdzić czy social providers są skonfigurowane (Google w settings)
- Sprawdzić czy template obsługuje social providers poprawnie
- Jeśli nie używamy social providers, można je wyłączyć w template

---

## 📊 TESTING CHECKLIST

### Manual Testing
- [ ] Login z prawidłowymi danymi działa
- [ ] Login z nieprawidłowymi danymi pokazuje błąd
- [ ] Redirect authenticated users z `/accounts/login/` działa
- [ ] Logout działa poprawnie
- [ ] Password reset działa (jeśli używany)
- [ ] Password change działa (jeśli używany)
- [ ] Social providers działają (jeśli włączone)

### Automated Testing
- [ ] `auth/login.spec.ts` - wszystkie testy przechodzą
- [ ] `auth/logout.spec.ts` - wszystkie testy przechodzą
- [ ] `auth/password-change.spec.ts` - wszystkie testy przechodzą
- [ ] `auth/password-reset.spec.ts` - wszystkie testy przechodzą
- [ ] `auth/signup.spec.ts` - wszystkie testy przechodzą
- [ ] `navigation/*.spec.ts` - wszystkie testy przechodzą
- [ ] Pełna suita E2E - brak regresji

---

## 🚀 DEPLOYMENT CONSIDERATIONS

### Database Migrations
- ✅ **Brak** - zmiany są tylko w kodzie, nie w modelach

### Settings Changes
- ✅ **Brak** - allauth jest już w INSTALLED_APPS

### Template Changes
- ✅ **Wymagane** - przywrócenie `account/login.html` jako głównego template
- ✅ **Usunięcie** - `registration/login.html`

### URL Changes
- ✅ **Wymagane** - przywrócenie `allauth.urls`
- ✅ **Usunięcie** - CustomLoginView override

### Testing
- ✅ **Krytyczne** - wszystkie E2E testy muszą przejść przed deploy

---

## 📝 NOTES

### Order of Implementation
1. **Najpierw backend** (Tasks 1.1-1.5) - przywrócić allauth
2. **Potem testy** (Tasks 2.1-2.7) - zaktualizować selektory
3. **Na końcu cleanup** (Tasks 3.1-3.3) - usunąć stare kody

### Rollback Plan
Jeśli coś pójdzie nie tak:
1. Revert commitów związanych z przywróceniem allauth
2. Przywrócić CustomLoginView
3. Przywrócić `registration/login.html`
4. Przywrócić stare selektory w testach

### Dependencies
- Allauth jest już zainstalowany (sprawdzić Pipfile/Pipfile.lock)
- Wszystkie wymagane settings są skonfigurowane
- Template `account/login.html` istnieje (lub trzeba przywrócić)

---

## ✅ FINAL ACCEPTANCE CRITERIA

- ✅ Allauth jest jedynym systemem autentykacji (brak CustomLoginView)
- ✅ Template `account/login.html` jest używany
- ✅ Template `registration/login.html` jest usunięty
- ✅ Wszystkie testy E2E przechodzą (100% auth-related tests)
- ✅ Wszystkie selektory używają `#id_login` (nie `#id_username`)
- ✅ Wszystkie URL names używają allauth (`account_login`, `account_logout`, etc.)
- ✅ Brak regresji w innych testach
- ✅ Dokumentacja jest zaktualizowana
- ✅ Kod jest czysty (brak starych komentarzy, nieużywanych importów)

---

**Document Owner**: Senior Software Architect  
**Review Date**: 2025-12-30  
**Next Review**: After implementation completion


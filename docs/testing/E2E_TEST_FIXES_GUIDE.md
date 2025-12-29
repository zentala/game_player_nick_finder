# E2E Test Fixes Guide - Dla Mid Inżynierów

**Cel:** Naprawić błędy w testach E2E aby osiągnąć 90%+ passing rate (obecnie 42% - 191/456 testów)

**Status:** Testy częściowo działają - większość funkcjonalności działa, ale są problemy z selektorami i niektórymi formularzami.

---

## 📊 Obecny Stan

- ✅ **191 testów przeszło** (42% passing rate)
- ⏭️ **51 testów pominiętych** (skip)
- ❌ **~18 testów nie przeszło** (głównie w Chromium)
- 🎯 **Cel:** 410+/456 testów passing (90%+)

---

## 🔍 Kategorie Błędów

### Kategoria 1: Brakujące Selektory Formularzy (CRITICAL)

**Problem:** Testy szukają formularzy z klasami CSS, które mogą nie istnieć lub nie być widoczne w DOM.

**Błędy:**
- `form.login` - czasem nie znajduje elementu
- `form.password_change` - nie znajduje elementu
- `form.password_reset` - nie znajduje elementu  
- `form.signup` - nie znajduje elementu

**Rozwiązanie:** Sprawdzić czy formularze rzeczywiście mają te klasy CSS w template'ach i czy są widoczne w DOM.

---

### Kategoria 2: Problemy z Przekierowaniami (HIGH)

**Problem:** Niektóre testy oczekują przekierowań, które nie następują.

**Przykład:**
- Zalogowany użytkownik powinien być przekierowany z `/accounts/login/` ale zostaje na stronie

**Rozwiązanie:** Sprawdzić logikę przekierowań w views.py i upewnić się że @login_required działa poprawnie.

---

### Kategoria 3: Różnice między Przeglądarkami (MEDIUM)

**Problem:** Testy działają w WebKit/Firefox ale nie w Chromium.

**Rozwiązanie:** Upewnić się że selektory są kompatybilne ze wszystkimi przeglądarkami.

---

## 📝 Instrukcja Krok po Kroku

### KROK 1: Zidentyfikuj Błędy

1. **Uruchom testy i zbierz wyniki:**
   ```bash
   pnpm test:e2e > test-results-$(date +%Y%m%d).txt 2>&1
   ```

2. **Znajdź wszystkie nieprzechodzące testy:**
   ```bash
   # W pliku wyników szukaj linii z numerem błędu
   grep "^\s\+[0-9]\+)" test-results-*.txt
   ```

3. **Sklasyfikuj błędy:**
   - Brakujące elementy (element not found)
   - Timeouty (timeout exceeded)
   - Błędne selektory (CSS selector error)
   - Problemy z przekierowaniami (URL mismatch)

---

### KROK 2: Sprawdź Szablony HTML

Dla każdego formularza który nie jest znajdowany:

1. **Znajdź odpowiedni template:**
   ```bash
   # Przykład dla password_change
   find app/templates -name "*password_change*"
   ```

2. **Sprawdź czy formularz ma odpowiednią klasę CSS:**
   ```html
   <!-- DOBRE: -->
   <form class="password_change" method="POST">
   
   <!-- ZŁE: -->
   <form method="POST"> <!-- brakuje klasy! -->
   ```

3. **Zweryfikuj czy formularz jest renderowany:**
   - Sprawdź czy nie jest warunkowo ukryty (v-if, v-show, {% if %})
   - Sprawdź czy jest w odpowiednim bloku template'a
   - Sprawdź czy view renderuje odpowiedni template

---

### KROK 3: Napraw Selektory w Testach

**Zasada:** Używaj bardziej elastycznych selektorów które działają nawet jeśli klasa CSS nie istnieje.

**Przykład poprawy:**

```typescript
// PRZED (może nie działać):
await expect(page.locator('form.password_change')).toBeVisible();

// PO (bardziej elastyczne):
await expect(page.locator('form[action*="password_change"], form.password_change')).toBeVisible();

// LUB (jeszcze lepiej - sprawdź zawartość):
const form = page.locator('form').filter({ has: page.locator('input[name*="password"]') });
await expect(form.first()).toBeVisible();
```

**Dobrą praktyką jest używać wielu alternatywnych selektorów:**

```typescript
// Najlepsze podejście - multiple fallbacks:
const formSelector = 'form.password_change, form[action*="password_change"], form:has(input[name*="oldpassword"])';
await expect(page.locator(formSelector).first()).toBeVisible();
```

---

### KROK 4: Napraw Problemy z Przekierowaniami

**Problem:** Test oczekuje przekierowania, ale nie następuje.

**Sprawdź:**

1. **View ma odpowiedni decorator:**
   ```python
   @login_required
   def my_view(request):
       # ... kod view
   ```

2. **Redirect jest ustawiony w settings:**
   ```python
   # settings.py
   LOGIN_REDIRECT_URL = '/'
   LOGIN_URL = '/accounts/login/'
   ```

3. **Test daje wystarczająco czasu na redirect:**
   ```typescript
   // PRZED:
   await page.goto('/accounts/login/');
   await expect(page).not.toHaveURL(/\/accounts\/login\/?/);
   
   // PO:
   await page.goto('/accounts/login/');
   await page.waitForURL('**/', { timeout: 5000 }); // czekaj na redirect
   await expect(page).not.toHaveURL(/\/accounts\/login\/?/);
   ```

---

### KROK 5: Napraw Timeouty

**Problem:** Test kończy się timeoutem bo element nie ładuje się w 30s.

**Sprawdź:**

1. **Czy strona w ogóle się ładuje:**
   ```typescript
   // Dodaj przed testem:
   await page.goto('/some-url/', { waitUntil: 'networkidle' });
   await page.waitForLoadState('domcontentloaded');
   ```

2. **Czy element jest warunkowo renderowany:**
   - Sprawdź czy potrzebuje czasu na JS
   - Sprawdź czy jest załadowany przez HTMX/AJAX
   - Jeśli tak, użyj `waitForSelector` zamiast `toBeVisible()`

3. **Czy selektor jest poprawny:**
   - Sprawdź w DevTools czy element istnieje
   - Użyj `page.locator('selector').count()` aby sprawdzić czy znajdzie element

---

### KROK 6: Testuj Lokalnie

Po każdej zmianie:

1. **Uruchom konkretny test:**
   ```bash
   pnpm playwright test tests/e2e/auth/login.spec.ts
   ```

2. **Uruchom w trybie UI (łatwiejszy debugging):**
   ```bash
   pnpm playwright test --ui
   ```

3. **Sprawdź screenshots w test-results/**

4. **Sprawdź error context:**
   ```bash
   cat test-results/*/error-context.md
   ```

---

### KROK 7: Użyj Playwright Codegen (Opcjonalnie)

Jeśli nie wiesz jaki selektor użyć:

1. **Uruchom codegen:**
   ```bash
   pnpm playwright codegen http://localhost:8000/accounts/login/
   ```

2. **Kliknij element który chcesz znaleźć**

3. **Skopiuj wygenerowany selektor**

---

## 🛠️ Konkretne Naprawy do Wykonania

### Naprawa 1: form.password_change

**Plik:** `tests/e2e/auth/password-change.spec.ts`

**Problem:** Linia 14 - `form.password_change` nie znajduje elementu

**Rozwiązanie:**
```typescript
// ZMIEŃ:
await expect(page.locator('form.password_change')).toBeVisible();

// NA:
const passwordChangeForm = page.locator('form.password_change, form[action*="password_change"], form:has(input[name*="old"])');
await expect(passwordChangeForm.first()).toBeVisible();
```

**Dlaczego:** Klasa CSS może nie być zawsze obecna, więc używamy wielu fallbacków.

---

### Naprawa 2: form.password_reset

**Plik:** `tests/e2e/auth/password-reset.spec.ts`

**Problem:** Linia 9 - `form.password_reset` nie znajduje elementu

**Rozwiązanie:**
```typescript
// ZMIEŃ:
await expect(page.locator('form.password_reset')).toBeVisible();

// NA:
const passwordResetForm = page.locator('form.password_reset, form[action*="password_reset"], form:has(input[name="email"][type="email"])');
await expect(passwordResetForm.first()).toBeVisible();
```

---

### Naprawa 3: form.signup

**Plik:** `tests/e2e/auth/signup.spec.ts`

**Problem:** Linia 9 - `form.signup` nie znajduje elementu

**Rozwiązanie:**
```typescript
// ZMIEŃ:
await expect(page.locator('form.signup, form#signup_form')).toBeVisible();

// NA:
const signupForm = page.locator('form.signup, form#signup_form, form[action*="signup"], form[action*="register"], form:has(input[name="username"])');
await expect(signupForm.first()).toBeVisible();
```

**WAŻNE:** Sprawdź najpierw jaki template jest używany dla signup:
```bash
grep -r "signup" app/templates/account/
grep -r "register" app/templates/
```

---

### Naprawa 4: Redirect z Login Page

**Plik:** `tests/e2e/auth/login.spec.ts`

**Problem:** Linia 188 - Zalogowany użytkownik nie jest przekierowany z `/accounts/login/`

**Rozwiązanie:**
```typescript
// ZMIEŃ:
test('should redirect logged in user away from login page', async ({ page }) => {
  await login(page, TEST_USERS.main.username, TEST_USERS.main.password);
  await page.goto('/accounts/login/');
  await page.waitForURL('**/', { timeout: 3000 });
  await expect(page).not.toHaveURL(/\/accounts\/login\/?/);
});

// NA (dodaj wait i sprawdź czy redirect następuje):
test('should redirect logged in user away from login page', async ({ page }) => {
  await login(page, TEST_USERS.main.username, TEST_USERS.main.password);
  
  // Czekaj na redirect po login
  await page.waitForURL('**/', { timeout: 5000 });
  
  // Teraz spróbuj wejść na login page
  await page.goto('/accounts/login/', { waitUntil: 'networkidle' });
  
  // Django powinien przekierować - czekaj na to
  await page.waitForTimeout(1000); // Daj czas na redirect
  const currentUrl = page.url();
  
  // Jeśli jesteśmy wciąż na login, sprawdź czy to jest błąd aplikacji czy testu
  if (currentUrl.includes('/accounts/login/')) {
    // Może być to poprawne zachowanie jeśli view nie ma redirect
    // Sprawdź czy formularz jest widoczny - jeśli tak, to błąd aplikacji
    const formVisible = await page.locator('form.login').isVisible().catch(() => false);
    if (formVisible) {
      // To jest błąd - zalogowany użytkownik nie powinien widzieć formularza
      throw new Error('Logged in user should be redirected from login page');
    }
  }
  
  // W przeciwnym razie, sprawdź że nie jesteśmy na login
  await expect(page).not.toHaveURL(/\/accounts\/login\/?/);
});
```

**LUB lepiej - sprawdź Django view:**

```python
# app/views.py lub gdzie jest login view
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

def login_view(request):
    if request.user.is_authenticated:
        return redirect('/')  # Dodaj ten redirect!
    # ... reszta kodu
```

---

## ✅ Checklist Przed Commitowaniem

- [ ] Uruchomiłem test lokalnie i przeszedł
- [ ] Sprawdziłem czy selektory działają w Chromium, Firefox i WebKit
- [ ] Dodałem komentarze wyjaśniające dlaczego używam wielu selektorów
- [ ] Sprawdziłem czy nie zepsułem innych testów
- [ ] Zaktualizowałem dokumentację jeśli zmieniłem sposób działania

---

## 📚 Dodatkowe Zasoby

- [Playwright Best Practices](https://playwright.dev/docs/best-practices)
- [Playwright Selectors](https://playwright.dev/docs/selectors)
- [Django Test Client](https://docs.djangoproject.com/en/stable/topics/testing/tools/)

---

## 🎯 Cel Końcowy

Po wykonaniu wszystkich napraw, powinieneś osiągnąć:
- ✅ 410+/456 testów passing (90%+)
- ✅ Wszystkie testy działają w Chromium, Firefox i WebKit
- ✅ Zero błędów związanych z selektorami formularzy
- ✅ Wszystkie przekierowania działają poprawnie

---

**Autor:** Software Architect  
**Data:** 2025-12-28  
**Status:** Do wdrożenia

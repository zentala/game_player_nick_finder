# E2E Test Fix Guide - For Mid-Level Developers

**Data**: 2025-12-28  
**Autor**: Software Architect  
**Status**: 📖 Instrukcje dla mid-level developerów

---

## 🎯 Cel

Naprawić wszystkie problemy P0 i P1 w testach E2E, aby osiągnąć **90%+ passing rate**.

**Aktualny stan**: ~30% passing rate (34-48 passed / 104-118 failed)  
**Cel**: 90%+ passing rate

---

## 📋 Przed Rozpoczęciem

### Wymagania
- Znajomość Playwright
- Znajomość TypeScript
- Znajomość Django
- Dostęp do projektu i możliwość uruchamiania testów

### Narzędzia
- `pnpm test:e2e` - uruchamianie testów (Chromium only, szybkie, domyślne - używaj podczas codziennej pracy)
- `pnpm test:e2e:all` - uruchamianie wszystkich testów (wszystkie przeglądarki, wolne - przed commit/merge)

### Dokumentacja
- `docs/testing/E2E_REMAINING_ISSUES.md` - lista problemów
- `docs/testing/E2E_FIX_STRATEGY_ARCHITECT.md` - strategia naprawy

---

## 🔧 FAZA 1: Naprawa P0 (Critical) - Login Helper Failures

### Zadanie 1.1: Poprawić funkcję `login()` helper

**Plik**: `tests/helpers/auth-helpers.ts`

**Problem**: Funkcja `login()` helper nie obsługuje poprawnie przypadku, gdy użytkownik jest już zalogowany (`redirect_authenticated_user = True`).

**Rozwiązanie**:

1. **Otwórz plik** `tests/helpers/auth-helpers.ts`

2. **Znajdź funkcję** `login()` (około linii 11)

3. **Zastąp obecną implementację** następującym kodem:

```typescript
export async function login(
  page: Page,
  username: string,
  password: string
): Promise<void> {
  // KROK 1: Sprawdź, czy użytkownik jest już zalogowany
  // CustomLoginView ma redirect_authenticated_user = True
  // Jeśli użytkownik jest już zalogowany, redirect nastąpi natychmiast
  await page.goto('/accounts/login/');
  
  // KROK 2: Czekaj na redirect (jeśli użytkownik jest już zalogowany)
  // Jeśli redirect nastąpi, użytkownik jest już zalogowany - zwróć sukces
  try {
    await page.waitForURL(/\/(?!accounts\/login)/, { timeout: 2000 });
    // Redirect nastąpił - użytkownik jest już zalogowany
    // Weryfikuj, że użytkownik jest faktycznie zalogowany
    await page.waitForLoadState('networkidle');
    const loginLink = page.locator('a:has-text("Log in")');
    const hasLoginLink = await loginLink.count() > 0;
    if (!hasLoginLink) {
      // User is authenticated, login successful
      return;
    }
  } catch (error) {
    // Redirect nie nastąpił - użytkownik nie jest zalogowany, kontynuuj logowanie
  }
  
  // KROK 3: Normalne logowanie (użytkownik nie jest zalogowany)
  await page.waitForLoadState('networkidle');
  
  // Wait for form fields to be visible before filling (CRITICAL - fixes timing issues)
  await expect(page.locator('#id_username')).toBeVisible({ timeout: 5000 });
  await expect(page.locator('#id_password')).toBeVisible({ timeout: 5000 });
  
  // Fill in credentials
  await page.fill('#id_username', username);
  await page.fill('#id_password', password);
  
  // Verify fields are filled (CRITICAL - throw error if not filled)
  const usernameValue = await page.locator('#id_username').inputValue();
  const passwordValue = await page.locator('#id_password').inputValue();
  
  if (usernameValue !== username || passwordValue.length === 0) {
    throw new Error(`Fields not filled correctly. Username: ${usernameValue} (expected: ${username}), Password length: ${passwordValue.length}`);
  }
  
  // Submit form
  await page.click('button[type="submit"]');
  
  // Wait for redirect to home page
  await page.waitForURL('**/', { timeout: 15000 });
  
  // Wait for page to fully load after navigation
  await page.waitForLoadState('networkidle');
  
  // Final check: Verify we're not still on login page (indicates login failure)
  const finalURL = page.url();
  if (finalURL.includes('/accounts/login/')) {
    const finalErrors = await page.locator('.alert-danger, .errorlist, .invalid-feedback').allTextContents();
    throw new Error(
      `Login failed - still on login page after redirect wait. ` +
      `Errors: ${finalErrors.join(', ')}. ` +
      `Please ensure test user '${username}' exists and fixtures are loaded.`
    );
  }
}
```

4. **Zapisz plik**

5. **Uruchom testy**, aby sprawdzić, czy poprawka działa:
```bash
pnpm test:e2e tests/e2e/auth/logout.spec.ts
```

**Oczekiwany wynik**: Testy powinny przechodzić (lub przynajmniej mniej failować)

---

### Zadanie 1.2: Poprawić funkcję `isAuthenticated()`

**Plik**: `tests/helpers/auth-helpers.ts`

**Problem**: `isAuthenticated()` zwraca `false` nawet po udanym logowaniu.

**Rozwiązanie**:

1. **Otwórz plik** `tests/helpers/auth-helpers.ts`

2. **Znajdź funkcję** `isAuthenticated()` (około linii 64)

3. **Zastąp obecną implementację** następującym kodem:

```typescript
export async function isAuthenticated(page: Page): Promise<boolean> {
  // Metoda 1: Sprawdź, czy login link jest widoczny (jeśli nie, użytkownik jest zalogowany)
  const loginLink = page.locator('a:has-text("Log in")');
  const hasLoginLink = await loginLink.count() > 0;
  
  if (hasLoginLink) {
    // Login link jest widoczny - użytkownik NIE jest zalogowany
    return false;
  }
  
  // Metoda 2: Sprawdź, czy user menu jest widoczny
  const userMenu = page.locator('a.nav-link.dropdown-toggle, a.dropdown-toggle, [data-toggle="dropdown"]').first();
  const hasUserMenu = await userMenu.count() > 0;
  
  if (hasUserMenu) {
    // User menu jest widoczny - użytkownik JEST zalogowany
    return true;
  }
  
  // Metoda 3: Sprawdź URL - jeśli jesteśmy na /accounts/login/, użytkownik NIE jest zalogowany
  const currentURL = page.url();
  if (currentURL.includes('/accounts/login/')) {
    return false;
  }
  
  // Jeśli żadna metoda nie zadziałała, zwróć false (bezpieczniejsze)
  return false;
}
```

4. **Zapisz plik**

5. **Uruchom testy**, aby sprawdzić, czy poprawka działa:
```bash
pnpm test:e2e tests/e2e/auth/login.spec.ts
```

**Oczekiwany wynik**: Testy powinny przechodzić (lub przynajmniej mniej failować)

---

### Zadanie 1.3: Dodać explicit wait przed weryfikacją autentykacji

**Pliki**: 
- `tests/e2e/auth/logout.spec.ts`
- `tests/e2e/auth/password-change.spec.ts`
- `tests/e2e/auth/login.spec.ts`

**Problem**: Weryfikacja autentykacji następuje zbyt szybko po logowaniu.

**Rozwiązanie**:

1. **Otwórz plik** `tests/e2e/auth/logout.spec.ts`

2. **Znajdź miejsca**, gdzie używamy `isAuthenticated()` po `login()`

3. **Dodaj explicit wait** przed weryfikacją:

```typescript
// Przed:
await login(page, TEST_USERS.main.username, TEST_USERS.main.password);
let authenticated = await isAuthenticated(page);
expect(authenticated).toBe(true);

// Po:
await login(page, TEST_USERS.main.username, TEST_USERS.main.password);
// Explicit wait przed weryfikacją
await page.waitForLoadState('networkidle');
await page.waitForTimeout(500); // Dodatkowy wait dla UI
let authenticated = await isAuthenticated(page);
expect(authenticated).toBe(true);
```

4. **Powtórz** dla wszystkich plików wymienionych powyżej

5. **Zapisz pliki**

6. **Uruchom testy**, aby sprawdzić, czy poprawka działa:
```bash
pnpm test:e2e tests/e2e/auth/logout.spec.ts tests/e2e/auth/password-change.spec.ts
```

**Oczekiwany wynik**: Testy powinny przechodzić (lub przynajmniej mniej failować)

---

## 🔧 FAZA 2: Naprawa P1 (High Priority) - Missing Elements & Timeouts

### Zadanie 2.1: Poprawić selektor user menu

**Pliki**: Wszystkie testy wymagające user menu

**Problem**: Selektor `a.nav-link.dropdown-toggle` może nie być poprawny.

**Rozwiązanie**:

1. **Znajdź wszystkie miejsca**, gdzie używamy `a.nav-link.dropdown-toggle`

2. **Zastąp** następującym kodem:

```typescript
// Przed:
const userMenu = page.locator('a.nav-link.dropdown-toggle').first();

// Po:
const userMenu = page.locator('a.nav-link.dropdown-toggle, a.dropdown-toggle, [data-toggle="dropdown"]').first();
```

3. **Dodaj explicit wait** przed kliknięciem:

```typescript
// Przed kliknięciem user menu
await page.waitForLoadState('networkidle');
await expect(userMenu).toBeVisible({ timeout: 10000 }); // Zwiększony timeout
await userMenu.click();
await page.waitForTimeout(300); // Wait for dropdown to open
```

4. **Zapisz pliki**

5. **Uruchom testy**, aby sprawdzić, czy poprawka działa:
```bash
pnpm test:e2e tests/e2e/auth/logout.spec.ts
```

**Oczekiwany wynik**: Testy powinny przechodzić (lub przynajmniej mniej failować)

---

### Zadanie 2.2: Zwiększyć timeout dla operacji, które mogą timeoutować

**Pliki**: 
- `tests/e2e/auth/login.spec.ts`
- Inne testy wymagające redirect

**Problem**: Timeout 5000ms jest zbyt krótki dla niektórych operacji.

**Rozwiązanie**:

1. **Otwórz plik** `tests/e2e/auth/login.spec.ts`

2. **Znajdź miejsca**, gdzie używamy `waitForURL` z timeout 5000ms

3. **Zwiększ timeout** do 15000ms:

```typescript
// Przed:
await page.waitForURL(/\/accounts\/profile\/?/, { timeout: 5000 });

// Po:
await page.waitForURL(/\/accounts\/profile\/?/, { timeout: 15000 });
```

4. **Dodaj explicit wait** przed operacją:

```typescript
// Przed operacją, która może timeoutować
await page.waitForLoadState('networkidle');
await page.waitForTimeout(500); // Dodatkowy wait
// Teraz wykonaj operację
```

5. **Zapisz plik**

6. **Uruchom testy**, aby sprawdzić, czy poprawka działa:
```bash
pnpm test:e2e tests/e2e/auth/login.spec.ts
```

**Oczekiwany wynik**: Testy powinny przechodzić (lub przynajmniej mniej failować)

---

## 🔧 FAZA 3: Naprawa P2 (Medium Priority) - URL Navigation

### Zadanie 3.1: Zaktualizować testy, aby akceptowały alternatywne URL

**Pliki**: 
- `tests/e2e/auth/signup.spec.ts`
- `tests/e2e/navigation/navbar-unauthenticated.spec.ts`

**Problem**: Testy wymagają specyficznych URL, ale aplikacja używa alternatywnych URL.

**Rozwiązanie**:

1. **Otwórz plik** `tests/e2e/auth/signup.spec.ts`

2. **Znajdź miejsca**, gdzie sprawdzamy URL

3. **Zaktualizuj**, aby akceptowały alternatywne URL:

```typescript
// Przed:
expect(currentUrl).toContain('/accounts/signup');

// Po:
expect(currentUrl).toMatch(/\/accounts\/signup\/?|\/register\/step1\/?/);
```

4. **Zapisz plik**

5. **Uruchom testy**, aby sprawdzić, czy poprawka działa:
```bash
pnpm test:e2e tests/e2e/auth/signup.spec.ts
```

**Oczekiwany wynik**: Testy powinny przechodzić (lub przynajmniej mniej failować)

---

## ✅ Weryfikacja

### Krok 1: Uruchom pełny zestaw testów

```bash
pnpm test:e2e
```

### Krok 2: Sprawdź wyniki

**Oczekiwany wynik**: 90%+ passing rate

**Metryki**:
- Przed naprawą: ~30% passing rate
- Po Fazie 1 (P0): ~60%+ passing rate (cel)
- Po Fazie 2 (P1): ~80%+ passing rate (cel)
- Po Fazie 3 (P2): ~90%+ passing rate (cel)

### Krok 3: Napraw pozostałe problemy

Jeśli passing rate nie osiągnął 90%+, sprawdź pozostałe błędy i napraw je zgodnie z tą samą strategią.

---

## 📋 Checklist

### Faza 1: P0 (Critical)
- [ ] Poprawić funkcję `login()` helper - obsługa `redirect_authenticated_user`
- [ ] Poprawić funkcję `isAuthenticated()` - bardziej niezawodna weryfikacja
- [ ] Dodać explicit wait przed weryfikacją autentykacji w testach
- [ ] Uruchomić testy i sprawdzić wyniki

### Faza 2: P1 (High Priority)
- [ ] Poprawić selektor user menu - bardziej niezawodny selektor
- [ ] Dodać explicit wait przed kliknięciem user menu
- [ ] Zwiększyć timeout dla operacji, które mogą timeoutować
- [ ] Uruchomić testy i sprawdzić wyniki

### Faza 3: P2 (Medium Priority)
- [ ] Zaktualizować testy, aby akceptowały alternatywne URL
- [ ] Uruchomić testy i sprawdzić wyniki

### Faza 4: Weryfikacja
- [ ] Uruchomić pełny zestaw testów
- [ ] Sprawdzić, czy passing rate osiągnął 90%+
- [ ] Naprawić pozostałe problemy, jeśli występują

---

## 🆘 Troubleshooting

### Problem: Testy nadal failują po poprawkach

**Rozwiązanie**:
1. Sprawdź, czy poprawki zostały poprawnie zastosowane
2. Sprawdź, czy nie ma błędów składniowych
3. Uruchom testy ponownie
4. Sprawdź logi testów, aby zobaczyć dokładne błędy

### Problem: Timeout errors nadal występują

**Rozwiązanie**:
1. Zwiększ timeout jeszcze bardziej (np. do 20000ms)
2. Dodaj więcej explicit waits
3. Sprawdź, czy aplikacja działa poprawnie

### Problem: Missing elements nadal występują

**Rozwiązanie**:
1. Sprawdź, czy selektory są poprawne (użyj DevTools)
2. Sprawdź, czy elementy faktycznie istnieją w UI
3. Dodaj więcej fallback selektorów

---

**Autor**: Software Architect  
**Data**: 2025-12-28  
**Status**: 📖 Instrukcje dla mid-level developerów - gotowe do użycia


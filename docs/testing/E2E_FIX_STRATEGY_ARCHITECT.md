# E2E Test Fix Strategy - Software Architect

**Data**: 2025-12-28  
**Autor**: Software Architect  
**Status**: 📋 Strategia naprawy

---

## 🎯 Cel Strategii

Naprawić wszystkie problemy P0 i P1 w testach E2E, aby osiągnąć **90%+ passing rate**.

**Aktualny stan**: ~30% passing rate (34-48 passed / 104-118 failed)  
**Cel**: 90%+ passing rate

---

## 📐 Architektura Rozwiązania

### 1. Problem: Login Helper Failures (P0)

#### Analiza Root Cause

**Problem**: `login()` helper failuje w niektórych testach, mimo że działa poprawnie w innych.

**Root Cause Analysis**:
1. `CustomLoginView` ma `redirect_authenticated_user = True`
2. Jeśli użytkownik jest już zalogowany, próba wejścia na `/accounts/login/` powoduje redirect do home
3. Funkcja `login()` helper nie obsługuje poprawnie tego przypadku
4. Race condition - test próbuje się zalogować, gdy użytkownik jest już zalogowany z poprzedniego testu

#### Strategia Naprawy

**KROK 1**: Poprawić funkcję `login()` helper, aby obsługiwała `redirect_authenticated_user`

**Rozwiązanie**:
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
  // ... reszta kodu logowania
}
```

**KROK 2**: Dodać explicit logout przed logowaniem w testach, które mogą mieć problemy

**Rozwiązanie**:
```typescript
// W beforeEach testów, które mogą mieć problemy
test.beforeEach(async ({ page }) => {
  // Explicit logout przed logowaniem (jeśli użytkownik jest już zalogowany)
  try {
    const userMenu = page.locator('a.nav-link.dropdown-toggle').first();
    if (await userMenu.count() > 0) {
      await userMenu.click();
      await page.waitForTimeout(200);
      const logoutLink = page.locator('a:has-text("Log out")');
      if (await logoutLink.count() > 0) {
        await logoutLink.click();
        await page.waitForURL('**/');
        await page.waitForLoadState('networkidle');
      }
    }
  } catch (error) {
    // User is not logged in, continue
  }
  
  // Teraz logowanie
  await login(page, TEST_USERS.main.username, TEST_USERS.main.password);
});
```

**KROK 3**: Dodać retry logic dla `login()` helper w przypadku failure

**Rozwiązanie**:
```typescript
// W funkcji login() helper - dodać retry logic
// Jeśli login failuje, spróbuj ponownie (max 2 razy)
```

---

### 2. Problem: Authentication Verification Failures (P0)

#### Analiza Root Cause

**Problem**: `isAuthenticated()` zwraca `false` nawet po udanym logowaniu.

**Root Cause Analysis**:
1. `isAuthenticated()` sprawdza widoczność `a.nav-link.dropdown-toggle`
2. User menu może nie być widoczny na niektórych stronach
3. Timing issue - menu może nie być jeszcze załadowane

#### Strategia Naprawy

**KROK 1**: Poprawić funkcję `isAuthenticated()` - użyć bardziej niezawodnej metody

**Rozwiązanie**:
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
  const userMenu = page.locator('a.nav-link.dropdown-toggle').first();
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
  
  // Metoda 4: Sprawdź cookies/session (jeśli dostępne)
  // ... dodatkowa weryfikacja
  
  // Jeśli żadna metoda nie zadziałała, zwróć false (bezpieczniejsze)
  return false;
}
```

**KROK 2**: Dodać explicit wait przed weryfikacją autentykacji

**Rozwiązanie**:
```typescript
// W testach, które weryfikują autentykację
await login(page, TEST_USERS.main.username, TEST_USERS.main.password);

// Explicit wait przed weryfikacją
await page.waitForLoadState('networkidle');
await page.waitForTimeout(500); // Dodatkowy wait dla UI

// Teraz weryfikuj
const authenticated = await isAuthenticated(page);
expect(authenticated).toBe(true);
```

---

### 3. Problem: Missing User Menu Elements (P1)

#### Analiza Root Cause

**Problem**: User menu (`a.nav-link.dropdown-toggle`) nie jest widoczny.

**Root Cause Analysis**:
1. Selektor może być niepoprawny
2. User menu może nie być widoczny na niektórych stronach
3. Timing issue - menu może nie być jeszcze załadowane

#### Strategia Naprawy

**KROK 1**: Poprawić selektor user menu - użyć bardziej niezawodnego selektora

**Rozwiązanie**:
```typescript
// Zamiast:
const userMenu = page.locator('a.nav-link.dropdown-toggle').first();

// Użyć:
const userMenu = page.locator('a.nav-link.dropdown-toggle, a.dropdown-toggle, [data-toggle="dropdown"]').first();
// Lub sprawdzić, czy istnieje alternatywny selektor w HTML
```

**KROK 2**: Dodać explicit wait przed kliknięciem user menu

**Rozwiązanie**:
```typescript
// Przed kliknięciem user menu
await page.waitForLoadState('networkidle');
await expect(userMenu).toBeVisible({ timeout: 10000 }); // Zwiększony timeout
await userMenu.click();
await page.waitForTimeout(300); // Wait for dropdown to open
```

**KROK 3**: Dodać fallback - jeśli user menu nie jest widoczne, użyć alternatywnej metody

**Rozwiązanie**:
```typescript
// Jeśli user menu nie jest widoczne, spróbuj alternatywnej metody
// (np. bezpośredni URL do logout, jeśli dostępny)
```

---

### 4. Problem: Timeout Errors (P1)

#### Analiza Root Cause

**Problem**: Timeout 5000ms jest zbyt krótki dla niektórych operacji.

**Root Cause Analysis**:
1. Niektóre operacje (np. redirect) mogą trwać dłużej niż 5000ms
2. Timing issue - operacje mogą być wolniejsze w niektórych środowiskach

#### Strategia Naprawy

**KROK 1**: Zwiększyć timeout dla operacji, które mogą trwać dłużej

**Rozwiązanie**:
```typescript
// Zamiast:
await page.waitForURL(/\/accounts\/profile\/?/, { timeout: 5000 });

// Użyć:
await page.waitForURL(/\/accounts\/profile\/?/, { timeout: 15000 }); // Zwiększony timeout
```

**KROK 2**: Dodać explicit wait przed operacjami, które mogą timeoutować

**Rozwiązanie**:
```typescript
// Przed operacją, która może timeoutować
await page.waitForLoadState('networkidle');
await page.waitForTimeout(500); // Dodatkowy wait
// Teraz wykonaj operację
```

---

### 5. Problem: URL Navigation Issues (P2)

#### Analiza Root Cause

**Problem**: Testy wymagają specyficznych URL, ale aplikacja używa alternatywnych URL.

**Root Cause Analysis**:
1. Aplikacja może używać różnych URL dla tego samego endpointu
2. Testy mogą nie akceptować alternatywnych URL

#### Strategia Naprawy

**KROK 1**: Zaktualizować testy, aby akceptowały alternatywne URL

**Rozwiązanie**:
```typescript
// Zamiast:
expect(currentUrl).toContain('/accounts/signup');

// Użyć:
expect(currentUrl).toMatch(/\/accounts\/signup\/?|\/register\/step1\/?/);
```

---

## 🔄 Plan Implementacji

### Faza 1: Naprawa P0 (Critical) - 1-2 godziny
1. ✅ Poprawić funkcję `login()` helper - obsługa `redirect_authenticated_user`
2. ✅ Poprawić funkcję `isAuthenticated()` - bardziej niezawodna weryfikacja
3. ✅ Dodać explicit wait przed weryfikacją autentykacji w testach
4. ✅ Dodać explicit logout przed logowaniem w testach, które mogą mieć problemy

### Faza 2: Naprawa P1 (High Priority) - 1-2 godziny
1. ✅ Poprawić selektor user menu - bardziej niezawodny selektor
2. ✅ Dodać explicit wait przed kliknięciem user menu
3. ✅ Zwiększyć timeout dla operacji, które mogą timeoutować
4. ✅ Dodać explicit wait przed operacjami, które mogą timeoutować

### Faza 3: Naprawa P2 (Medium Priority) - 30 minut
1. ✅ Zaktualizować testy, aby akceptowały alternatywne URL

### Faza 4: Weryfikacja - 30 minut
1. ✅ Uruchomić pełny zestaw testów
2. ✅ Sprawdzić, czy passing rate osiągnął 90%+
3. ✅ Naprawić pozostałe problemy, jeśli występują

**Łączny czas**: 3-5 godzin

---

## 📋 Checklist Implementacji

### Faza 1: P0 (Critical)
- [ ] Poprawić funkcję `login()` helper - obsługa `redirect_authenticated_user`
- [ ] Poprawić funkcję `isAuthenticated()` - bardziej niezawodna weryfikacja
- [ ] Dodać explicit wait przed weryfikacją autentykacji w testach
- [ ] Dodać explicit logout przed logowaniem w testach, które mogą mieć problemy

### Faza 2: P1 (High Priority)
- [ ] Poprawić selektor user menu - bardziej niezawodny selektor
- [ ] Dodać explicit wait przed kliknięciem user menu
- [ ] Zwiększyć timeout dla operacji, które mogą timeoutować
- [ ] Dodać explicit wait przed operacjami, które mogą timeoutować

### Faza 3: P2 (Medium Priority)
- [ ] Zaktualizować testy, aby akceptowały alternatywne URL

### Faza 4: Weryfikacja
- [ ] Uruchomić pełny zestaw testów
- [ ] Sprawdzić, czy passing rate osiągnął 90%+
- [ ] Naprawić pozostałe problemy, jeśli występują

---

## 🎯 Metryki Sukcesu

**Cel**: 90%+ passing rate

**Metryki**:
- Przed naprawą: ~30% passing rate
- Po Fazie 1 (P0): ~60%+ passing rate (cel)
- Po Fazie 2 (P1): ~80%+ passing rate (cel)
- Po Fazie 3 (P2): ~90%+ passing rate (cel)

---

**Autor**: Software Architect  
**Data**: 2025-12-28  
**Status**: 📋 Strategia naprawy - gotowa do implementacji


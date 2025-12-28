# Kategoryzacja Błędów E2E (214 failed)

## Kategoria 1: CSS Selector Errors (KRYTYCZNE) ⚠️

**Problem:** Playwright nie akceptuje regex w CSS selektorach
**Przykład błędu:**
```
Unexpected token "=" while parsing css selector 
".alert-danger, .errorlist, .invalid-feedback, text=/invalid/i"
```

**Dotyczy:** ~50-60 testów
**Kategorie testów:**
- Login validation errors
- Signup validation errors  
- Password change validation
- Form field validation

**Rozwiązanie:**
Zamienić selektory CSS+regex na Playwright locators:

```typescript
// BŁĄD:
await expect(page.locator('.alert-danger, text=/invalid/i')).toBeVisible();

// POPRAWNE:
await expect(page.locator('.alert-danger').filter({ hasText: /invalid/i })).toBeVisible();
// LUB:
await expect(page.getByText(/invalid/i)).toBeVisible();
```

**Priorytet:** P0 (CRITICAL) - to blokuje wszystkie testy walidacji

---

## Kategoria 2: Timeouts (30s) ⏱️

**Problem:** Elementy nie ładują się w czasie 30s
**Przykład błędu:**
```
Error: page.fill: Test timeout of 30000ms exceeded.
Call log: waiting for locator('#id_username')
```

**Dotyczy:** ~80-100 testów
**Główne przyczyny:**
1. Strony nie loadują się (404/500)
2. JavaScript errors blokują renderowanie
3. Fixture data nie załadowane
4. Selektory niepoprawne

**Badanie wymagane:**
- Sprawdzić Django logs
- Sprawdzić browser console errors
- Zweryfikować fixture data

**Priorytet:** P1 (HIGH) - może wskazywać na problemy backendowe

---

## Kategoria 3: Missing Elements ❌

**Problem:** Element nie istnieje w DOM
**Przykład błędu:**
```
Error: element(s) not found
Locator: locator('.some-class')
```

**Dotyczy:** ~40-50 testów
**Przyczyny:**
1. Template różni się od oczekiwanego przez test
2. Element behind auth/permissions
3. Conditional rendering (if/else)
4. HTMX partial load issues

**Analiza wymagana:**
- Porównać templates z oczekiwaniami testów
- Sprawdzić czy auth/permissions są spełnione
- Zweryfikować HTMX endpoints

**Priorytet:** P2 (MEDIUM) - może być OK (feature nie zaimplementowane)

---

## Kategoria 4: Strict Mode Violations 🔒

**Problem:** Locator znalazł >1 element
**Przykład błędu:**
```
strict mode violation: locator('h1, h2, h5:has-text("Blocked Characters")') 
resolved to 2 elements
```

**Dotyczy:** ~10-15 testów
**Rozwiązanie:**
- Użyć `.first()` / `.last()` / `.nth()`
- Lub zmienić selector na bardziej specific

```typescript
// BŁĄD:
await expect(page.locator('h1, h2, h5:has-text("Blocked")')).toBeVisible();

// POPRAWNE:
await expect(page.locator('h1, h2, h5:has-text("Blocked")').first()).toBeVisible();
```

**Priorytet:** P2 (MEDIUM) - łatwe do naprawy

---

## Kategoria 5: URL Navigation Issues 🔀

**Problem:** Redirect nie działa jak oczekiwano
**Przykład błędu:**
```
Error: expect(page).not.toHaveURL(expected) failed
Expected pattern: not /\/accounts\/login\/?/
Received string: "http://localhost:7600/accounts/login/"
```

**Dotyczy:** ~20-30 testów
**Przyczyny:**
1. Django nie przekierowuje zalogowanych userów
2. Login required decorators missing
3. POST redirect chain broken

**Analiza wymagana:**
- Sprawdzić views.py redirects
- Zweryfikować @login_required decorators
- Sprawdzić MIDDLEWARE ordering

**Priorytet:** P1 (HIGH) - security/UX concern

---

## Podsumowanie Priorytetów

### P0 - CRITICAL (Blokery masowe):
- ✅ **CSS Selector Errors** (~60 testów) - NAJPIERW TO!

### P1 - HIGH (Problemy funkcjonalne):
- ⏱️ **Timeouts** (~100 testów)
- 🔀 **URL Navigation** (~30 testów)

### P2 - MEDIUM (Łatwe naprawy):
- ❌ **Missing Elements** (~50 testów)
- 🔒 **Strict Mode Violations** (~15 testów)

## Plan Działania

### Faza 1: Quick Wins (1-2h)
1. Naprawić CSS selector errors (global search/replace)
2. Naprawić strict mode violations (dodać .first())

**Oczekiwany wynik:** +70 testów passing (261/456 = 57%)

### Faza 2: Debug Timeouts (2-4h)
1. Włączyć Django debug logging
2. Sprawdzić browser console w failed tests
3. Naprawić routing/template issues

**Oczekiwany wynik:** +80 testów passing (341/456 = 75%)

### Faza 3: Deep Dive (4-8h)
1. Naprawić missing elements (feature gaps)
2. Naprawić URL navigation (redirects)

**Oczekiwany wynik:** +60 testów passing (401/456 = 88%)

### Cel Końcowy:
**90%+ passing rate** (410+/456 testów)

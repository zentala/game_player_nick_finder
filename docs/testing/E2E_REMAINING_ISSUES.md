# E2E Test Issues - Remaining Problems to Fix

**Data**: 2025-12-28  
**Status**: ⚠️ Wymaga naprawy  
**Passing Rate**: ~30% (34-48 passed / 104-118 failed)

---

## 📊 Aktualny Stan

### Statystyki
- **Przed naprawami**: 59 passed / 93 failed (39% passing rate)
- **Po naprawach**: 34-48 passed / 104-118 failed (~30% passing rate)
- **Cel**: 90%+ passing rate

### Co Zostało Naprawione ✅
1. ✅ Funkcja `login()` helper - działa poprawnie (potwierdzone logami)
2. ✅ Testy używające bezpośredniego logowania - zmienione na `login()` helper
3. ✅ Timing checks w testach logowania
4. ✅ URL mismatch w navbar-unauthenticated

---

## ❌ Problemy Do Naprawienia

### KATEGORIA 1: Login Helper Failures (P0 - Critical)

#### Problem 1.1: "Login failed - still on login page after redirect wait"
**Lokalizacja**: Wiele testów używających `login()` helper w `beforeEach`

**Dotknięte pliki**:
- `tests/e2e/auth/logout.spec.ts` - wszystkie testy (5 testów)
- `tests/e2e/auth/password-change.spec.ts` - wszystkie testy w `beforeEach` (7+ testów)
- `tests/e2e/auth/login.spec.ts` - test "should redirect logged in user away from login page"
- Inne testy używające `login()` helper w `beforeEach`

**Objawy**:
```
Error: Login failed - still on login page after redirect wait. Errors: 
```

**Przyczyna**:
- `CustomLoginView` ma `redirect_authenticated_user = True`
- Jeśli użytkownik jest już zalogowany, próba wejścia na `/accounts/login/` powoduje redirect
- Funkcja `login()` helper może nie obsługiwać poprawnie tego przypadku
- Możliwy race condition - test próbuje się zalogować, gdy użytkownik jest już zalogowany z poprzedniego testu

**Priorytet**: P0 (Critical) - blokuje ~12+ testów

---

#### Problem 1.2: "expect(authenticated).toBe(true)" failures
**Lokalizacja**: Testy weryfikujące autentykację po logowaniu

**Dotknięte pliki**:
- `tests/e2e/auth/login.spec.ts:200` - "should redirect logged in user away from login page"
- `tests/e2e/auth/logout.spec.ts` - weryfikacja autentykacji
- `tests/e2e/auth/password-change.spec.ts:12` - weryfikacja autentykacji w `beforeEach`

**Objawy**:
```
Error: expect(received).toBe(expected) // Object.is equality
> 200 |       expect(authenticated).toBe(true);
```

**Przyczyna**:
- `isAuthenticated()` może zwracać `false` nawet po udanym logowaniu
- Timing issue - weryfikacja następuje zbyt szybko po logowaniu
- Problem z selektorem `a.nav-link.dropdown-toggle` - może nie być widoczny

**Priorytet**: P0 (Critical) - blokuje weryfikację autentykacji

---

### KATEGORIA 2: Missing Elements (P1 - High Priority)

#### Problem 2.1: "expect(locator).toBeVisible() failed" - User Menu
**Lokalizacja**: Testy wymagające user menu dropdown

**Dotknięte pliki**:
- `tests/e2e/auth/logout.spec.ts:61` - "should successfully logout user"
- `tests/e2e/auth/password-change.spec.ts:49` - "should navigate to password change page via user menu"
- Inne testy wymagające user menu

**Objawy**:
```
Error: expect(locator).toBeVisible() failed
Timeout: 5000ms
> 61 |     await expect(page.locator('a.nav-link.dropdown-toggle').first()).toBeVisible();
```

**Przyczyna**:
- Selektor `a.nav-link.dropdown-toggle` może nie być poprawny
- User menu może nie być widoczny na niektórych stronach
- Timing issue - menu może nie być jeszcze załadowane

**Priorytet**: P1 (High Priority) - blokuje testy wymagające user menu

---

#### Problem 2.2: "element(s) not found" - Various Elements
**Lokalizacja**: Różne testy wymagające specyficznych elementów

**Objawy**:
```
Error: element(s) not found
- Expect "toBeVisible" with timeout 5000ms
```

**Przyczyna**:
- Niepoprawne selektory
- Elementy mogą nie istnieć w UI
- Timing issues - elementy mogą nie być jeszcze załadowane

**Priorytet**: P1 (High Priority) - blokuje wiele testów

---

### KATEGORIA 3: Timeout Errors (P1 - High Priority)

#### Problem 3.1: "page.waitForURL: Timeout 5000ms exceeded"
**Lokalizacja**: Testy wymagające redirect

**Dotknięte pliki**:
- `tests/e2e/auth/login.spec.ts:148` - "should redirect to originally requested page after login"
- Inne testy wymagające redirect

**Objawy**:
```
TimeoutError: page.waitForURL: Timeout 5000ms exceeded.
> 148 |     await page.waitForURL(/\/accounts\/profile\/?/, { timeout: 5000 });
```

**Przyczyna**:
- Timeout 5000ms może być zbyt krótki
- Redirect może nie nastąpić z powodu problemów z logowaniem
- Timing issue - redirect może nastąpić później

**Priorytet**: P1 (High Priority) - blokuje testy wymagające redirect

---

### KATEGORIA 4: URL Navigation Issues (P2 - Medium Priority)

#### Problem 4.1: "expect(currentUrl).toContain('/accounts/signup')" failures
**Lokalizacja**: Testy wymagające specyficznych URL

**Dotknięte pliki**:
- `tests/e2e/auth/signup.spec.ts:105` - testy wymagające `/accounts/signup`
- `tests/e2e/navigation/navbar-unauthenticated.spec.ts` - testy wymagające signup URL

**Objawy**:
```
Error: expect(received).toContain(expected) // indexOf
> 105 |       expect(currentUrl).toContain('/accounts/signup');
```

**Przyczyna**:
- URL może być inny niż oczekiwany (np. `/register/step1/` zamiast `/accounts/signup/`)
- Testy mogą nie akceptować alternatywnych URL

**Priorytet**: P2 (Medium Priority) - blokuje testy signup

---

## 📋 Podsumowanie Problemów

### Według Priorytetu

**P0 (Critical) - 2 problemy**:
1. Login Helper Failures - ~12+ testów
2. Authentication Verification Failures - ~5+ testów

**P1 (High Priority) - 3 problemy**:
1. Missing User Menu Elements - ~5+ testów
2. Missing Various Elements - ~10+ testów
3. Timeout Errors - ~3+ testów

**P2 (Medium Priority) - 1 problem**:
1. URL Navigation Issues - ~2+ testów

### Według Kategorii

**Login/Authentication Issues**: ~17+ testów (P0)
**Missing Elements**: ~15+ testów (P1)
**Timeout Errors**: ~3+ testów (P1)
**URL Navigation**: ~2+ testów (P2)

**Łącznie**: ~37+ testów wymaga naprawy

---

## 🎯 Cel

**Cel**: Naprawić wszystkie problemy P0 i P1, aby osiągnąć 90%+ passing rate

**Szacowany czas**: 2-4 godziny dla mid-level developera

---

**Autor**: Software Architect  
**Data**: 2025-12-28  
**Status**: ⚠️ Wymaga naprawy


# Przewodnik Testowania E2E

**Data**: 2025-12-29  
**Cel**: Optymalizacja workflow testowania E2E - szybkie iteracje lokalnie, pełne testy przed commitem

---

## 🚀 Szybkie Testowanie (Domyślne - Lokalne)

### Podstawowe komendy:

```bash
# Testuj tylko na Chromium (najszybsze, domyślne)
pnpm test:e2e
```

**Co to robi:**
- ✅ Testuje tylko na **Chromium** (najszybsze)
- ✅ Używa prostego reportera `line` (krótkie komunikaty)
- ✅ **3x szybsze** niż testowanie na wszystkich przeglądarkach
- ✅ Idealne do szybkich iteracji podczas naprawiania testów
- ✅ **Używaj zawsze podczas codziennej pracy na komputerze**

**VSCode Task**: `Run E2E Tests` (Ctrl+Shift+P → Tasks: Run Task)

---

## 📊 Testowanie Wszystkich Przeglądarek (Przed Commitem/Merge)

### Kiedy potrzebne:
- **Przed commitem** do `dev` branch (jeśli robisz większe zmiany)
- **Przed merge** do `main` branch (OBOWIĄZKOWE)
- W CI/CD pipeline (automatycznie)
- Gdy chcesz sprawdzić kompatybilność między przeglądarkami

### Komendy:

```bash
# Testuj wszystkie przeglądarki (Chromium, Firefox, WebKit) - WOLNE (~7-9 min)
pnpm test:e2e:all

# Lub użyj aliasu:
pnpm test:e2e:slow
```

**Co to robi:**
- ✅ Testuje na **wszystkich przeglądarkach** (Chromium, Firefox, WebKit)
- ✅ Używa HTML reportera (szczegółowe raporty)
- ✅ **Wolniejsze** (~7-9 min) ale zapewnia pełną kompatybilność
- ✅ **OBOWIĄZKOWE przed merge do main**

**VSCode Task**: `Run E2E Tests (All Browsers)` (Ctrl+Shift+P → Tasks: Run Task)

**⚠️ WAŻNE**: Testy oznaczone tagiem `@allbrowsers` w komentarzach będą testowane we wszystkich przeglądarkach.

---

## 🎯 Testowanie Konkretnej Przeglądarki

### Komendy:

```bash
# Tylko Chromium
pnpm test:e2e:chromium

# Tylko Firefox
pnpm test:e2e:firefox

# Tylko WebKit (Safari)
pnpm test:e2e:webkit
```

---

## 🔍 Testowanie Konkretnych Testów

### Szybkie sprawdzenie jednego testu:

```bash
# Testuj tylko jeden plik testowy
pnpm test:e2e tests/e2e/auth/login.spec.ts

# Testuj tylko jeden konkretny test (użyj .only w kodzie lub):
pnpm test:e2e -g "should successfully login"

# Testuj tylko testy z określonego folderu
pnpm test:e2e tests/e2e/auth/
```

---

## ⚡ Najszybsze Iteracje

### Workflow dla szybkich napraw:

1. **Napraw kod/selektory**
2. **Uruchom szybki test (domyślne):**
   ```bash
   pnpm test:e2e tests/e2e/auth/login.spec.ts
   ```
3. **Sprawdź wyniki** (krótkie komunikaty)
4. **Jeśli działa, przed commitem testuj wszystkie przeglądarki:**
   ```bash
   pnpm test:e2e:all tests/e2e/auth/login.spec.ts
   ```

### Przykład:

```bash
# Szybka iteracja - tylko Chromium, jeden test (domyślne, szybkie)
pnpm test:e2e tests/e2e/auth/login.spec.ts

# Jeśli działa, przed commitem sprawdź wszystkie przeglądarki (wolne)
pnpm test:e2e:all tests/e2e/auth/login.spec.ts
```

---

## 📝 Różnice w Reporterach

### `line` (domyślny dla lokalnego developmentu):
```
✓ tests/e2e/auth/login.spec.ts:34:7 › Login Flow › should successfully login (2.1s)
✗ tests/e2e/auth/login.spec.ts:60:7 › Login Flow › should show error for invalid credentials (1.5s)
```

**Zalety:**
- ✅ Krótkie komunikaty
- ✅ Szybkie wyświetlanie wyników
- ✅ Idealne do szybkich iteracji

### `html` (domyślny dla CI):
```
Test Results: 151 passed, 305 failed
Detailed report: playwright-report/index.html
```

**Zalety:**
- ✅ Szczegółowe raporty
- ✅ Screenshoty błędów
- ✅ Trace viewer
- ✅ Idealne do analizy błędów

### Przełączanie reporterów:

```bash
# Użyj HTML reportera (szczegółowy)
pnpm test:e2e --reporter=html

# Użyj line reportera (szybki)
pnpm test:e2e --reporter=line

# Użyj list reportera (lista testów)
pnpm test:e2e --reporter=list
```

---

## 🎓 Najlepsze Praktyki

### Podczas Developmentu (Na Komputerze):
1. ✅ Używaj `pnpm test:e2e` (domyślne, szybkie) dla szybkich iteracji
2. ✅ Testuj tylko zmienione pliki
3. ✅ Używa automatycznie `line` reportera (prostsze komunikaty)
4. ✅ Testuje tylko na Chromium (najszybsze)
5. ✅ **Zawsze używaj tego podczas codziennej pracy**

### Przed Commitem/Merge:
1. ✅ **Przed commitem do dev**: Uruchom `pnpm test:e2e:all` (jeśli robisz większe zmiany)
2. ✅ **Przed merge do main**: **OBOWIĄZKOWE** - uruchom `pnpm test:e2e:all` (wszystkie przeglądarki)
3. ✅ Sprawdź HTML report jeśli są błędy
4. ✅ Napraw wszystkie błędy przed commitem/merge

### W CI/CD:
1. ✅ Automatycznie testuje wszystkie przeglądarki
2. ✅ Używa HTML reportera
3. ✅ Uploaduje raporty jako artifacts

---

## ⏱️ Oszczędność Czasu

### Porównanie:

| Konfiguracja | Czas wykonania | Użycie |
|-------------|----------------|--------|
| **Chromium tylko** (`pnpm test:e2e` - domyślne) | ~2-3 min | **Development, szybkie iteracje, codzienna praca** |
| **Wszystkie przeglądarki** (`pnpm test:e2e:all` - wolne) | ~7-9 min | **Przed commit/merge do main, CI/CD** |
| **Jeden test, Chromium** | ~5-10 sek | Szybkie sprawdzenie naprawy |

### Przykład oszczędności:

**Przed zmianami:**
- Testowanie wszystkich przeglądarek: **~7 minut**
- Iteracja: napraw → test → napraw → test = **~14 minut**

**Po zmianach:**
- Testowanie tylko Chromium: **~2 minuty**
- Iteracja: napraw → test → napraw → test = **~4 minuty**

**Oszczędność: ~10 minut na iterację!** 🎉

---

## 🔧 Konfiguracja

### `playwright.config.ts`:

```typescript
// Domyślnie tylko Chromium (szybkie)
projects: process.env.CI || process.env.TEST_ALL_BROWSERS
  ? [chromium, firefox, webkit]  // Wszystkie dla CI
  : [chromium]                   // Tylko Chromium lokalnie

// Domyślnie line reporter (szybki)
reporter: process.env.CI ? 'html' : 'line'
```

### Zmienne środowiskowe:

```bash
# Testuj wszystkie przeglądarki (użyj zamiast tego: pnpm test:e2e:all)
TEST_ALL_BROWSERS=true pnpm test:e2e

# Użyj HTML reportera
pnpm test:e2e --reporter=html
```

---

## 📝 Tagi w Testach (@allbrowsers)

Testy mogą być oznaczone komentarzem `@allbrowsers` w kodzie, co oznacza że **powinny** być testowane we wszystkich przeglądarkach przed commitem/merge. Jednak wszystkie testy powinny działać we wszystkich przeglądarkach.

**Przykład w teście:**
```typescript
// @allbrowsers - This test should be verified on all browsers before merge
test('should handle cross-browser compatibility', async ({ page }) => {
  // Test code...
});
```

**Uwaga**: Tag `@allbrowsers` jest tylko informacyjny - wszystkie testy są automatycznie testowane we wszystkich przeglądarkach gdy używasz `pnpm test:e2e:all`.

---

## 🎯 Podsumowanie Workflow

### Codzienna Praca (Na Komputerze):
```bash
# Zawsze używaj szybkiego testowania (tylko Chromium)
pnpm test:e2e
```

### Przed Commitem/Merge:
```bash
# Przed merge do main - OBOWIĄZKOWE (wszystkie przeglądarki)
pnpm test:e2e:all
```

### W CI/CD:
- Automatycznie testuje wszystkie przeglądarki
- Używa HTML reportera
- Uploaduje raporty jako artifacts

---

**Autor**: Software Architect  
**Data**: 2025-12-29  
**Status**: ✅ Gotowe do użycia


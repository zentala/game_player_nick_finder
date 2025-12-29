# Przewodnik Szybkiego Testowania E2E

**Data**: 2025-12-28  
**Cel**: Szybsze iteracje podczas naprawiania testów E2E

---

## 🚀 Szybkie Testowanie (Domyślne)

### Podstawowe komendy:

```bash
# Testuj tylko na Chromium (najszybsze, domyślne)
pnpm test:e2e

# Lub jawnie:
pnpm test:e2e:fast
```

**Co to robi:**
- ✅ Testuje tylko na **Chromium** (najszybsze)
- ✅ Używa prostego reportera `line` (krótkie komunikaty)
- ✅ **3x szybsze** niż testowanie na wszystkich przeglądarkach
- ✅ Idealne do szybkich iteracji podczas naprawiania testów

---

## 📊 Testowanie Wszystkich Przeglądarek

### Kiedy potrzebne:
- Przed commit/merge
- W CI/CD pipeline
- Gdy chcesz sprawdzić kompatybilność między przeglądarkami

### Komendy:

```bash
# Testuj wszystkie przeglądarki (Chromium, Firefox, WebKit)
pnpm test:e2e:all

# Lub ustaw zmienną środowiskową:
TEST_ALL_BROWSERS=true pnpm test:e2e
```

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
2. **Uruchom szybki test:**
   ```bash
   pnpm test:e2e:fast tests/e2e/auth/login.spec.ts
   ```
3. **Sprawdź wyniki** (krótkie komunikaty)
4. **Jeśli działa, testuj wszystkie przeglądarki:**
   ```bash
   pnpm test:e2e:all
   ```

### Przykład:

```bash
# Szybka iteracja - tylko Chromium, jeden test
pnpm test:e2e:fast tests/e2e/auth/login.spec.ts

# Jeśli działa, sprawdź wszystkie przeglądarki
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

### Podczas Developmentu:
1. ✅ Używaj `pnpm test:e2e:fast` dla szybkich iteracji
2. ✅ Testuj tylko zmienione pliki
3. ✅ Używaj `line` reportera (domyślny)
4. ✅ Testuj tylko na Chromium

### Przed Commitem:
1. ✅ Uruchom `pnpm test:e2e:all` (wszystkie przeglądarki)
2. ✅ Sprawdź HTML report jeśli są błędy
3. ✅ Napraw wszystkie błędy przed commitem

### W CI/CD:
1. ✅ Automatycznie testuje wszystkie przeglądarki
2. ✅ Używa HTML reportera
3. ✅ Uploaduje raporty jako artifacts

---

## ⏱️ Oszczędność Czasu

### Porównanie:

| Konfiguracja | Czas wykonania | Użycie |
|-------------|----------------|--------|
| **Chromium tylko** (domyślne) | ~2-3 min | Development, szybkie iteracje |
| **Wszystkie przeglądarki** | ~6-9 min | Przed commit, CI/CD |
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
# Testuj wszystkie przeglądarki
TEST_ALL_BROWSERS=true pnpm test:e2e

# Użyj HTML reportera
pnpm test:e2e --reporter=html
```

---

**Autor**: Software Architect  
**Data**: 2025-12-28  
**Status**: ✅ Gotowe do użycia


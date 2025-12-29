# Automatyczne Ustawianie Haseł dla Użytkowników Testowych

**Data**: 2025-12-28  
**Cel**: Automatyczne ustawianie haseł dla użytkowników testowych z fixtures

---

## 🎯 Problem

Fixtures zawierają użytkowników z **zahashowanymi hasłami**. Hasła w fixtures mogą nie odpowiadać hasłom używanym w testach (`testpass123`, `pass`), co powoduje, że logowanie nie działa.

## ✅ Rozwiązanie

Stworzone zostały skrypty, które **automatycznie ustawiają hasła** dla użytkowników testowych zgodnie z `TEST_USERS` z `tests/helpers/auth-helpers.ts`.

---

## 📋 Użytkownicy Testowi

Hasła są ustawiane dla następujących użytkowników:

| Username | Password | Źródło |
|----------|----------|--------|
| `testuser` | `testpass123` | `tests/helpers/auth-helpers.ts` |
| `otheruser` | `pass` | `tests/helpers/auth-helpers.ts` |
| `privateuser` | `testpass123` | `tests/helpers/auth-helpers.ts` |

---

## 🚀 Jak Użyć

### **Opcja 1: Automatycznie (Rekomendowane)**

Skrypty `load_fixtures.ps1` i `load_fixtures.sh` **automatycznie** ustawiają hasła po załadowaniu fixtures:

```bash
# Windows
.\load_fixtures.ps1

# Unix/Linux/MacOS
./load_fixtures.sh
```

**To jest najlepsze rozwiązanie** - wszystko dzieje się automatycznie!

---

### **Opcja 2: Ręcznie (Jeśli potrzebujesz tylko ustawić hasła)**

Możesz też uruchomić skrypty osobno:

#### Windows (PowerShell):
```powershell
.\setup_test_users.ps1
```

#### Unix/Linux/MacOS (Bash):
```bash
chmod +x setup_test_users.sh
./setup_test_users.sh
```

#### Przez npm/pnpm:
```bash
# Windows
pnpm setup:test-users

# Unix/Linux/MacOS
pnpm setup:test-users:unix
```

---

## 📝 Co Robią Skrypty

1. **Sprawdzają czy użytkownicy istnieją** w bazie danych
2. **Ustawiają hasła** zgodnie z `TEST_USERS`
3. **Ustawiają `is_active = True`** dla wszystkich użytkowników testowych
4. **Wyświetlają status** dla każdego użytkownika:
   - ✓ Password set for user: `username` - jeśli sukces
   - ✗ User not found: `username` - jeśli użytkownik nie istnieje
   - ✗ Error for `username`: `error` - jeśli wystąpił błąd

---

## 🔍 Przykładowe Wyjście

```
Setting passwords for test users...

Updating test user passwords...
✓ Password set for user: testuser
✓ Password set for user: otheruser
✓ Password set for user: privateuser

✓ All test user passwords set successfully!

Test users ready:
  - testuser / testpass123
  - otheruser / pass
  - privateuser / testpass123
```

---

## ⚠️ Wymagania

1. **Fixtures muszą być załadowane** przed uruchomieniem skryptu:
   ```bash
   .\load_fixtures.ps1
   # lub
   ./load_fixtures.sh
   ```

2. **pipenv musi być zainstalowany**:
   ```bash
   pip install pipenv
   ```

3. **Django musi być skonfigurowany** i działać

---

## 🐛 Rozwiązywanie Problemów

### Problem: "User not found: testuser"

**Przyczyna**: Fixtures nie są załadowane

**Rozwiązanie**:
```bash
# Załaduj fixtures najpierw
.\load_fixtures.ps1
# Potem ustaw hasła
.\setup_test_users.ps1
```

### Problem: "Error: pipenv is not installed"

**Przyczyna**: pipenv nie jest zainstalowany lub nie jest w PATH

**Rozwiązanie**:
```bash
pip install pipenv
```

### Problem: "Permission denied" (Unix/Linux/MacOS)

**Przyczyna**: Skrypt nie ma uprawnień do wykonania

**Rozwiązanie**:
```bash
chmod +x setup_test_users.sh
./setup_test_users.sh
```

---

## 📂 Pliki

- `setup_test_users.ps1` - Skrypt PowerShell dla Windows
- `setup_test_users.sh` - Skrypt Bash dla Unix/Linux/MacOS
- `load_fixtures.ps1` - Zaktualizowany, automatycznie ustawia hasła
- `load_fixtures.sh` - Zaktualizowany, automatycznie ustawia hasła

---

## 🎓 Wnioski

1. **Automatyzacja**: Hasła są ustawiane automatycznie przy ładowaniu fixtures
2. **Bezpieczeństwo**: Skrypty używają Django's `set_password()` - bezpieczne hashowanie
3. **Niezawodność**: Sprawdzają czy użytkownicy istnieją przed ustawieniem hasła
4. **Informacyjność**: Wyświetlają szczegółowy status dla każdego użytkownika

---

## ✅ Checklist Przed Uruchomieniem Testów

- [ ] Fixtures załadowane: `.\load_fixtures.ps1` lub `./load_fixtures.sh`
- [ ] Hasła ustawione automatycznie (przez load_fixtures) lub ręcznie
- [ ] Wszyscy użytkownicy testowi mają status "✓ Password set"
- [ ] Serwer Django działa na `http://localhost:7600`
- [ ] Możesz uruchomić testy: `pnpm test:e2e`

---

**Autor**: Software Architect  
**Data**: 2025-12-28  
**Status**: ✅ Gotowe do użycia


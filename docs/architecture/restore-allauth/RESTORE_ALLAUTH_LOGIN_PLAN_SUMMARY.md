# Podsumowanie Planu Przywrócenia Allauth Login

**Data**: 2025-12-30  
**Dla**: Development Team  
**Status**: Ready for Implementation

---

## 🎯 CEL

Przywrócenie allauth jako jedynego systemu logowania i usunięcie standardowego Django login (CustomLoginView).

---

## 📋 GŁÓWNE ZMIANY

### Backend (5 tasków)
1. ✅ Usunięcie `CustomLoginView` z `app/views.py`
2. ✅ Odkomentowanie `path('accounts/', include('allauth.urls'))` w `urls.py`
3. ✅ Usunięcie override `/accounts/login/` z CustomLoginView
4. ✅ Usunięcie template `registration/login.html`
5. ✅ Weryfikacja template `account/login.html` i settings

### Testy E2E (7 tasków)
1. ✅ Aktualizacja `auth-helpers.ts`: `#id_username` → `#id_login`
2. ✅ Aktualizacja `login.spec.ts`: wszystkie selektory
3. ✅ Aktualizacja `password-reset.spec.ts` (jeśli potrzeba)
4. ✅ Aktualizacja `password-change.spec.ts` (jeśli potrzeba)
5. ✅ Aktualizacja `signup.spec.ts` (jeśli potrzeba)
6. ✅ Aktualizacja `navigation/*.spec.ts` (jeśli potrzeba)
7. ✅ Uruchomienie pełnej suity testów

### Cleanup (3 taski)
1. ✅ Usunięcie starych dokumentów i komentarzy
2. ✅ Aktualizacja dokumentacji zmian
3. ✅ Weryfikacja importów i zależności

---

## 🔑 KLUCZOWE RÓŻNICE

| Aspekt | Obecny (Django) | Docelowy (Allauth) |
|--------|----------------|-------------------|
| **Pole formularza** | `username` | `login` |
| **ID pola** | `#id_username` | `#id_login` |
| **URL name** | `login` | `account_login` |
| **Template** | `registration/login.html` | `account/login.html` |
| **View** | `CustomLoginView` | `allauth LoginView` |

---

## ⚠️ KRYTYCZNE PUNKTY

1. **Selektory w testach**: Wszystkie `#id_username` → `#id_login`
2. **URL names**: Wszystkie `login` → `account_login` (w kodzie/testach)
3. **Template**: Upewnić się, że `account/login.html` używa `{% url 'account_login' %}`
4. **Redirect**: Allauth ma `redirect_authenticated_user = True` domyślnie

---

## 📝 ORDER OF IMPLEMENTATION

1. **Backend** (Tasks 1.1-1.5) - najpierw przywrócić allauth
2. **Testy** (Tasks 2.1-2.7) - potem zaktualizować selektory
3. **Cleanup** (Tasks 3.1-3.3) - na końcu usunąć stare kody

---

## ✅ FINAL CHECKLIST

- [ ] CustomLoginView usunięty
- [ ] Allauth URLs odkomentowane
- [ ] Template `registration/login.html` usunięty
- [ ] Template `account/login.html` zweryfikowany
- [ ] Wszystkie selektory używają `#id_login`
- [ ] Wszystkie testy E2E przechodzą
- [ ] Brak regresji w innych testach
- [ ] Dokumentacja zaktualizowana

---

**Szczegóły**: Zobacz `RESTORE_ALLAUTH_LOGIN_PLAN.md` dla pełnego planu z taskami.


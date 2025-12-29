# Rozwiązanie Problemu z PowerShell Terminal

**Problem**: `System.ArgumentOutOfRangeException` w PSReadLine - terminal za mały dla prediction view

**Rozwiązanie**: Wyłącz prediction view w PowerShell

## Szybkie Rozwiązanie (Tymczasowe)

Uruchom komendę z wyłączonym prediction view:

```powershell
$env:PSReadLinePredictionViewStyle = 'None'; pnpm test:e2e tests/e2e/auth/login.spec.ts
```

## Trwałe Rozwiązanie

Dodaj do swojego PowerShell profile (`$PROFILE`):

```powershell
# Wyłącz prediction view (rozwiązuje problem z małym terminalem)
$env:PSReadLinePredictionViewStyle = 'None'

# Lub użyj innego stylu (mniej miejsca)
# $env:PSReadLinePredictionViewStyle = 'InlineView'
```

**Jak edytować profile**:
```powershell
# Sprawdź lokalizację profilu
$PROFILE

# Edytuj profil
notepad $PROFILE

# Jeśli plik nie istnieje, utwórz go:
New-Item -Path $PROFILE -Type File -Force
notepad $PROFILE
```

## Alternatywne Rozwiązania

### 1. Zwiększ rozmiar terminala
- Zwiększ szerokość terminala (min. 80 kolumn)
- Zwiększ wysokość terminala (min. 40 linii)

### 2. Użyj innego terminala
- Windows Terminal (zalecane)
- CMD (nie ma prediction view)
- Git Bash

### 3. Wyłącz prediction view globalnie
```powershell
Set-PSReadLineOption -PredictionViewStyle None
```

## Uwaga

**Błąd PowerShell NIE blokuje testów** - testy się uruchamiają poprawnie, tylko wyświetlanie może być problematyczne. Możesz bezpiecznie ignorować błąd PSReadLine jeśli testy działają.

---

**Autor**: Software Architect  
**Data**: 2025-12-28


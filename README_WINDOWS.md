# Uruchamianie na Windows (PowerShell)

## Wymagania
- Python 3.11+ (sprawdź: `python --version`)
- pipenv (zainstaluj: `pip install pipenv`)

## Szybki start

### 1. Instalacja zależności
```powershell
pipenv install
```

Lub użyj skryptu pomocniczego:
```powershell
.\setup_env.ps1
```

### 2. Uruchomienie serwera Django
```powershell
.\start_django.ps1
```

Lub bezpośrednio:
```powershell
pipenv run python manage.py runserver
```

### 3. Pierwsza konfiguracja (tylko raz)

#### Migracje bazy danych:
```powershell
pipenv run python manage.py migrate sites
pipenv run python manage.py migrate
```

#### Utworzenie użytkownika administratora:
```powershell
pipenv run python manage.py createsuperuser
```

#### Załadowanie danych testowych (opcjonalnie):
```powershell
pipenv run python manage.py loaddata app/fixtures/categories_fixtures.json
pipenv run python manage.py loaddata app/fixtures/games_fixtures.json
```

## Dostępne skrypty PowerShell

- `start_django.ps1` - Uruchamia serwer deweloperski Django
- `setup_env.ps1` - Konfiguruje środowisko i wykonuje migracje

## Rozwiązywanie problemów

### Problem: pipenv nie znajduje Python 3.11
**Rozwiązanie**: 
```powershell
pipenv install --python 3.11
```

### Problem: Błędy związane z migracjami
**Rozwiązanie**:
```powershell
pipenv run python manage.py migrate sites
pipenv run python manage.py migrate
```

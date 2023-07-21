# Player Finder - Aplikacja webowa oparta o Django

Player Finder to aplikacja webowa napisana w Django, która umożliwia użytkownikom wyszukiwanie starych znajomych z gier online na podstawie ich nicków oraz rejestrowanie się w serwisie, aby być znalezionym przez innych graczy. Użytkownicy mogą również dodawać swoje postacie z różnych gier, definiować opis i zakres dat, kiedy grali pod danym nickiem. Dodatkowo istnieje funkcjonalność wysyłania wiadomości i notyfikacji email.

## Instalacja i uruchomienie aplikacji

Najpierw upewnij się, że Twój system ma zainstalowane:

- Python (wersja 3.6 lub nowsza)
- pip (narzędzie do zarządzania pakietami Python)

## Krok 1: Sklonuj repozytorium

Sklonuj repozytorium na swój lokalny komputer za pomocą polecenia git:

```bash
git clone https://github.com/TWOJE_REPOZYTORIUM
cd PlayerFinder
```

## Krok 2: Instalacja zależności

Aby zainstalować wymagane zależności Python, wykonaj poniższą komendę:

```bash
pip install -r requirements.txt
```

## Krok 3: Konfiguracja bazy danych

Aplikacja używa domyślnie bazy danych SQLite, więc nie musisz konfigurować dodatkowej bazy. Możesz jedynie wykonać migrację bazy danych:

```bash
python manage.py migrate
```

## Krok 4: Uruchomienie serwera

Aby uruchomić serwer deweloperski Django, wykonaj następującą komendę:

```bash
python manage.py runserver
```

Teraz aplikacja powinna być dostępna pod adresem http://localhost:8000/

# Homepage Layout Switcher Architecture

**Status**: 📋 Design  
**Last Updated**: 2024-12-19  
**Author**: Solution Architect

## Overview

System przełączania między różnymi wariantami layoutu strony głównej do testów UX. Pozwala na szybkie porównanie różnych podejść do designu bez implementacji pełnej funkcjonalności.

## Architecture Design

### Layout Variants

1. **v0 (default/original)** - Obecny layout (zachowany)
2. **v1** - Vertical Step-by-Step Flow (rekomendowany)
3. **v2** - Horizontal Card Layout
4. **v3** - Wizard/Stepper Flow

### Switching Mechanism

**Priority System** (highest to lowest):
1. **URL Parameter** - `?layout=v0`, `?layout=v1`, `?layout=v2`, `?layout=v3`
   - Automatycznie zapisuje wybór do sesji użytkownika
   - `?layout=reset` - resetuje do domyślnego (v0)
2. **Session Storage** - zapamiętany wybór użytkownika
   - Zapisuje się automatycznie przy wyborze przez URL param
   - Trwa przez całą sesję użytkownika
3. **Default** - v0 (original layout) jeśli brak preferencji

**Fallback**: Jeśli brak parametru, sesji lub nieprawidłowy → v0 (default)

### Implementation Structure

```
app/
├── templates/
│   ├── index.html (main template with switcher)
│   └── homepage/
│       ├── layout_v0.html (original)
│       ├── layout_v1.html (vertical step-by-step)
│       ├── layout_v2.html (horizontal cards)
│       └── layout_v3.html (wizard/stepper)
├── views.py (IndexView with layout switching)
└── static/
    └── app/
        └── homepage-switcher.js (layout switcher UI)
```

## View Implementation

### IndexView Modification

```python
class IndexView(BaseViewMixin, TemplateView):
    current_page = 'home'
    template_name = 'index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get layout with priority: URL param > Session > Default
        layout = self.get_user_layout()
        
        context['layout'] = layout
        context['layout_variants'] = ['v0', 'v1', 'v2', 'v3']
        context['show_layout_switcher'] = self.should_show_switcher()
        
        # Mock data for testing (only for v1-v3)
        if layout != 'v0':
            context['mock_games'] = self.get_mock_games()
            context['mock_years'] = self.get_mock_years()
        
        return context
    
    def get_user_layout(self):
        """
        Get layout for user with priority:
        1. URL param (highest priority, saves to session)
        2. Session storage (if user has saved preference)
        3. Default (v0)
        """
        # Check URL param first
        url_layout = self.request.GET.get('layout', None)
        
        if url_layout:
            # Handle reset
            if url_layout == 'reset':
                self.request.session.pop('homepage_layout', None)
                return 'v0'
            
            # Validate and save to session
            if url_layout in ['v0', 'v1', 'v2', 'v3']:
                self.request.session['homepage_layout'] = url_layout
                return url_layout
        
        # Check session storage
        session_layout = self.request.session.get('homepage_layout', None)
        if session_layout and session_layout in ['v0', 'v1', 'v2', 'v3']:
            return session_layout
        
        # Default layout
        return 'v0'
    
    def should_show_switcher(self):
        """
        Determine if layout switcher should be visible.
        Show switcher if:
        - URL param is present (user is actively switching)
        - User has saved layout preference (not default)
        """
        # Always show if URL param is present
        if self.request.GET.get('layout'):
            return True
        
        # Show if user has saved preference (not default)
        saved_layout = self.request.session.get('homepage_layout', None)
        if saved_layout and saved_layout != 'v0':
            return True
        
        return False
    
    def get_mock_games(self):
        """Return mock games data for testing"""
        return [
            {'id': 1, 'name': 'Counter-Strike', 'slug': 'counter-strike'},
            {'id': 2, 'name': 'World of Warcraft', 'slug': 'world-of-warcraft'},
            {'id': 3, 'name': 'League of Legends', 'slug': 'league-of-legends'},
            {'id': 4, 'name': 'Minecraft', 'slug': 'minecraft'},
            {'id': 5, 'name': 'Diablo II', 'slug': 'diablo-ii'},
        ]
    
    def get_mock_years(self):
        """Return years for Time Machine slider"""
        return list(range(1990, 2025))  # 1990-2024
```

## Template Structure

### Main Template (index.html)

```django
{% extends "base.html" %}
{% load i18n %}

{% block content %}
  {# Layout Switcher (only visible in development/testing) #}
  {% if layout != 'v0' or request.GET.layout %}
    {% include "homepage/layout_switcher.html" %}
  {% endif %}
  
  {# Render selected layout #}
  {% if layout == 'v0' %}
    {% include "homepage/layout_v0.html" %}
  {% elif layout == 'v1' %}
    {% include "homepage/layout_v1.html" %}
  {% elif layout == 'v2' %}
    {% include "homepage/layout_v2.html" %}
  {% elif layout == 'v3' %}
    {% include "homepage/layout_v3.html" %}
  {% endif %}
{% endblock %}
```

## Layout Variants Specification

### Layout v0 (Original)
- **File**: `homepage/layout_v0.html`
- **Description**: Obecny layout (bez zmian)
- **Status**: ✅ Implemented

### Layout v1 (Vertical Step-by-Step)
- **File**: `homepage/layout_v1.html`
- **Structure**:
  1. Hero section z tytułem
  2. Game selector (searchable select)
  3. Time Machine (horizontal slider)
  4. Friendship (tag-based input)
  5. Join button
- **Mock Data**: Games, years, placeholder nicknames
- **Status**: ⏳ To implement

### Layout v2 (Horizontal Cards)
- **File**: `homepage/layout_v2.html`
- **Structure**:
  - Hero section
  - 3 cards w rzędzie (desktop): Game | Time Machine | Friendship
  - Stack na mobile
- **Mock Data**: Games, years, placeholder nicknames
- **Status**: ⏳ To implement

### Layout v3 (Wizard/Stepper)
- **File**: `homepage/layout_v3.html`
- **Structure**:
  - Progress indicator (Step X of 3)
  - Step 1: Game selection
  - Step 2: Year selection
  - Step 3: Nickname input
  - Navigation buttons (Back/Next)
- **Mock Data**: Games, years, placeholder nicknames
- **Status**: ⏳ To implement

## Layout Switcher UI

### Component: layout_switcher.html

Switcher pokazuje:
- **4 przyciski** do wyboru layoutu (v0-v3)
- **Status zapisanego layoutu** (badge z informacją)
- **Przycisk Reset** (tylko gdy użytkownik ma zapisany layout)
- **Informację** o zapisaniu preferencji w sesji

**Visibility**: Kontrolowane przez `show_layout_switcher` context variable:
- Zawsze widoczny gdy jest parametr `?layout=` w URL
- Widoczny gdy użytkownik ma zapisany layout (nie domyślny)
- Można włączyć zawsze w development (opcjonalnie)

**Features**:
- Automatyczne zapisywanie wyboru do sesji
- Wizualne oznaczenie aktywnego layoutu
- Możliwość resetu do domyślnego
- Informacja o zapisanym layoutcie

## Mock Data Structure

### Games
```python
[
    {'id': 1, 'name': 'Counter-Strike', 'slug': 'counter-strike'},
    {'id': 2, 'name': 'World of Warcraft', 'slug': 'world-of-warcraft'},
    # ... more games
]
```

### Years
```python
[1990, 1991, ..., 2024]  # Range 1990-2024
```

### Sample Nicknames (for placeholder)
```python
['PlayerOne', 'GamerPro', 'OldFriend', 'GamingBuddy']
```

## CSS/JavaScript Requirements

### CSS
- Custom styles dla każdego layoutu w `static/app/homepage-layouts.css`
- Time Machine slider styles
- Tag input styles
- Wizard progress indicator styles

### JavaScript
- Layout switcher (optional, can be pure HTML links)
- Time Machine slider interaction (mock)
- Tag input functionality (mock)
- Wizard step navigation (mock)

**Note**: Wszystko mockowane - nie łączy się z backendem!

## Testing Strategy

### Manual Testing
1. Przełączanie między layoutami przez URL
2. Sprawdzanie zapamiętywania preferencji (odświeżenie strony)
3. Testowanie resetu do domyślnego
4. Sprawdzanie responsywności każdego layoutu
5. Weryfikacja mock data display
6. Testowanie na różnych urządzeniach

### User Testing / A/B Testing
1. **Przypisanie layoutów do użytkowników**:
   - Różni użytkownicy mogą mieć różne layouty
   - Layout zapisuje się w sesji użytkownika
   - Możliwość testowania z różnymi grupami

2. **Zbieranie feedbacku**:
   - Pokazać użytkownikom różne warianty
   - Zbierać feedback na każdy layout
   - Porównać UX między wariantami
   - Wybrać najlepszy wariant do implementacji

3. **Analiza użycia**:
   - Śledzić, który layout jest najczęściej wybierany
   - Monitorować konwersje dla każdego layoutu
   - Analizować czas spędzony na stronie

### Session Management
- Layout zapisuje się w `request.session['homepage_layout']`
- Trwa przez całą sesję użytkownika (domyślnie 1 godzina)
- Można rozszerzyć o zapis do bazy danych dla zalogowanych użytkowników
- Można dodać przypisanie layoutu przez admin panel

## Usage Examples

### Basic Usage
```
# Wybierz layout v1 (zapisze się w sesji)
http://127.0.0.1:7600/?layout=v1

# Po odświeżeniu strony, layout v1 będzie nadal aktywny
http://127.0.0.1:7600/

# Reset do domyślnego
http://127.0.0.1:7600/?layout=reset
```

### A/B Testing Scenario
1. Użytkownik A otrzymuje link: `/?layout=v1`
2. Layout v1 zapisuje się w jego sesji
3. Wszystkie kolejne wizyty użytkownika A będą używać v1
4. Użytkownik B otrzymuje link: `/?layout=v2`
5. Layout v2 zapisuje się w jego sesji
6. Można porównać zachowanie obu grup

### Future Enhancements

**Możliwe rozszerzenia**:
1. **Database Storage** - zapis preferencji dla zalogowanych użytkowników
2. **Admin Panel** - przypisywanie layoutów do użytkowników/grup
3. **Feature Flags** - integracja z systemem feature flags
4. **Analytics** - śledzenie użycia każdego layoutu
5. **User Preferences** - panel ustawień użytkownika do wyboru layoutu

Po wybraniu najlepszego layoutu:
1. Implementacja pełnej funkcjonalności
2. Integracja z backendem (search API)
3. Usunięcie mock data
4. Usunięcie nieużywanych layoutów (opcjonalnie)

## Security Considerations

- Layout switcher tylko w development/testing
- W production można ukryć switcher
- URL param validation (tylko v0-v3)
- No sensitive data in mock data

## Performance

- Layout templates cached
- Mock data generated in view (lightweight)
- No database queries for mock layouts
- Static assets optimized

---

**Document Version**: 1.0  
**Last Updated**: 2024-12-19  
**Maintained By**: Solution Architect


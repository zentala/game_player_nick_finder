# Homepage Search Redesign - UX/UI Proposal

**Status**: 📋 Proposal  
**Last Updated**: 2024-12-19  
**Author**: UX Engineer + Development Team

## Overview

Redesign strony głównej z interaktywnym wyszukiwaniem znajomych. Wszystko na jednej stronie z sekwencyjnym flow: **Gra → Rok → Nicki → Rejestracja/Logowanie**.

## User Flow

```
1. Użytkownik wchodzi na stronę główną
2. Wybiera GRĘ (select/input z autocomplete)
3. Wybiera ROK w Time Machine (poziomy przewijany select)
4. Wpisuje NICKI w Friendship (input, oddzielone spacją)
5. Klika "Join" / "Search"
6. Jeśli NIE jest zalogowany → Formularz rejestracji (imię, login, hasło)
7. Jeśli JEST zalogowany → Przekierowanie do wyników wyszukiwania
8. Nicki trafiają do bazy jako "poszukiwani" (search queries)
```

## Design Proposals

### Proposal 1: Vertical Step-by-Step Flow (Recommended)

**Layout**: Pionowy flow, każdy krok w osobnej sekcji

```
┌─────────────────────────────────────────┐
│  Reconnect with Old Gaming Buddies      │
│                                         │
│  [Select Game ▼]  [Search icon]        │
│  ─────────────────────────────────────  │
│                                         │
│  ┌───────────────────────────────────┐ │
│  │  Time Machine                     │ │
│  │  [← 1990] [1995] [2000] [2005] →] │ │
│  │  (poziomy przewijany slider)      │ │
│  └───────────────────────────────────┘ │
│                                         │
│  ┌───────────────────────────────────┐ │
│  │  Friendship                       │ │
│  │  [Nick1 Nick2 Nick3 ...]         │ │
│  │  (input z placeholder)            │ │
│  └───────────────────────────────────┘ │
│                                         │
│  [Join Now] [Already have account?]    │
└─────────────────────────────────────────┘
```

**Pros**:
- ✅ Czytelny, sekwencyjny flow
- ✅ Łatwy do zrozumienia
- ✅ Mobile-friendly (pionowy layout)
- ✅ Każdy krok jest wyraźnie widoczny

**Cons**:
- ⚠️ Wymaga scrollowania na mobile
- ⚠️ Więcej miejsca wertykalnego

---

### Proposal 2: Horizontal Card Layout

**Layout**: Wszystko w jednym rzędzie (desktop), stack na mobile

```
┌─────────────────────────────────────────────────────────┐
│  Reconnect with Old Gaming Buddies                      │
│                                                         │
│  [Select Game ▼]                                        │
│                                                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │
│  │ Time Machine │  │  Friendship  │  │   Actions    │ │
│  │              │  │              │  │              │ │
│  │ [← 2000 →]   │  │ [Nick input] │  │ [Join]       │ │
│  │              │  │              │  │ [Login]      │ │
│  └──────────────┘  └──────────────┘  └──────────────┘ │
└─────────────────────────────────────────────────────────┘
```

**Pros**:
- ✅ Kompaktowy, wszystko widoczne na raz
- ✅ Szybki dostęp do wszystkich opcji
- ✅ Nowoczesny wygląd

**Cons**:
- ⚠️ Może być za ciasno na mobile
- ⚠️ Trudniejsze do zrozumienia flow

---

### Proposal 3: Wizard/Stepper Flow (Most Interactive)

**Layout**: Krok po kroku z progress indicator

```
┌─────────────────────────────────────────┐
│  Step 1 of 3: Select Game              │
│  [████████░░░░░░░░] 33%                 │
│                                         │
│  [Select Game ▼]                        │
│                                         │
│  [Next →]                               │
└─────────────────────────────────────────┘

Po kliknięciu "Next":
┌─────────────────────────────────────────┐
│  Step 2 of 3: Choose Year               │
│  [████████████████░░] 66%               │
│                                         │
│  Time Machine                           │
│  [← 1990] [1995] [2000] [2005] →]       │
│                                         │
│  [← Back]  [Next →]                     │
└─────────────────────────────────────────┘
```

**Pros**:
- ✅ Najbardziej interaktywny
- ✅ Jasny progress
- ✅ Focus na jednym kroku na raz
- ✅ Możliwość cofania

**Cons**:
- ⚠️ Więcej kliknięć
- ⚠️ Więcej JavaScript do implementacji
- ⚠️ Może być frustrujące dla użytkowników chcących szybko wyszukać

---

## Time Machine - Year Selector Design

### Option A: Horizontal Slider with Years

```
[←]  1990  1995  2000  2005  2010  2015  2020  [→]
      └─────────────┘
      Selected: 2000
```

**Features**:
- Smooth scroll horizontal
- Click on year to select
- Arrow buttons for navigation
- Highlight selected year
- Years 2000-2010 more prominent (bigger, centered)

### Option B: Year Picker with Decade Groups

```
┌─────────────────────────────────┐
│  1990s  [1990] [1991] ... [1999]│
│  2000s  [2000] [2001] ... [2009]│ ← Prominent
│  2010s  [2010] [2011] ... [2019]│
│  2020s  [2020] [2021] ... [2024]│
└─────────────────────────────────┘
```

### Option C: Circular/Radial Year Selector

```
        [1995]
    [1990]  [2000] ← Selected
[1985]          [2005]
    [1990]  [2010]
        [2015]
```

**Recommendation**: **Option A** - Horizontal slider jest najbardziej intuicyjny i mobile-friendly.

---

## Friendship - Nickname Input Design

### Option A: Single Input with Space Separation

```
┌─────────────────────────────────────────┐
│  Enter nicknames (separated by space)    │
│  [Nick1 Nick2 Nick3 ...]                │
│  └─────────────────────────────────────┘ │
└─────────────────────────────────────────┘
```

**Features**:
- Placeholder: "Enter nicknames separated by space"
- Real-time validation (max 10 nicknames?)
- Show count: "3 nicknames entered"
- Auto-suggest from database (optional)

### Option B: Tag-based Input (like email tags)

```
┌─────────────────────────────────────────┐
│  Enter nicknames                        │
│  [Nick1 ×] [Nick2 ×] [Nick3 ×] [  ]    │
│  └─────────────────────────────────────┘ │
└─────────────────────────────────────────┘
```

**Features**:
- Each nickname as removable tag
- Click × to remove
- Visual feedback
- Better UX for managing multiple nicknames

**Recommendation**: **Option B** - Tag-based input jest bardziej user-friendly i pozwala łatwo usuwać nicki.

---

## Game Selector Design

### Option A: Dropdown Select

```
┌─────────────────────────────────┐
│  [Select Game ▼]                │
│  ─────────────────────────────── │
│  Counter-Strike                 │
│  World of Warcraft              │
│  League of Legends              │
│  ...                            │
└─────────────────────────────────┘
```

### Option B: Searchable Select (Select2-like)

```
┌─────────────────────────────────┐
│  [Search game...]               │
│  ─────────────────────────────── │
│  🔍 Counter-Strike              │
│  🔍 World of Warcraft         │
│  🔍 League of Legends           │
│  ...                            │
└─────────────────────────────────┘
```

**Recommendation**: **Option B** - Searchable select jest lepszy gdy mamy dużo gier.

---

## Registration/Login Integration

### Option A: Modal/Dropdown after "Join"

```
Po kliknięciu "Join":
┌─────────────────────────────────┐
│  Create Account                 │
│  ────────────────────────────── │
│  Username: [________]            │
│  Email:    [________]           │
│  Password: [________]           │
│                                 │
│  [Register] [Already have?]     │
└─────────────────────────────────┘
```

### Option B: Expandable Section

```
Po kliknięciu "Join":
┌─────────────────────────────────┐
│  [Username: ________]            │
│  [Email:    ________]           │
│  [Password: ________]           │
│                                 │
│  [Register] [Login instead]     │
└─────────────────────────────────┘
```

### Option C: Separate Page (Current)

```
Po kliknięciu "Join":
→ Redirect to /register/
→ Pre-fill search params in session
→ After registration → redirect to search results
```

**Recommendation**: **Option C** - Separate page jest najczystsze i pozwala na pełny formularz rejestracji.

---

## Technical Implementation

### Backend: Search Query Model

```python
class SearchQuery(models.Model):
    """Store user search queries (poszukiwani)"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    session_id = models.CharField(max_length=255, null=True, blank=True)  # For non-logged users
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    year = models.IntegerField(null=True, blank=True)
    nicknames = models.JSONField(default=list)  # Array of nicknames
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
```

### Frontend: JavaScript Flow

```javascript
// 1. Game selection
const gameSelect = document.getElementById('game-select');
gameSelect.addEventListener('change', () => {
    enableTimeMachine();
});

// 2. Year selection
const yearSlider = document.getElementById('year-slider');
yearSlider.addEventListener('change', () => {
    enableFriendship();
});

// 3. Nickname input
const nicknameInput = document.getElementById('nickname-input');
nicknameInput.addEventListener('input', () => {
    enableJoinButton();
});

// 4. Join button
const joinButton = document.getElementById('join-button');
joinButton.addEventListener('click', () => {
    if (user.isAuthenticated) {
        performSearch();
    } else {
        redirectToRegister();
    }
});
```

### API Endpoint

```python
# POST /api/v1/search-queries/
{
    "game": "counter-strike",
    "year": 2005,
    "nicknames": ["Nick1", "Nick2", "Nick3"]
}
```

---

## Recommended Final Design

**Combination of best options**:

1. **Layout**: Proposal 1 (Vertical Step-by-Step) - najczytelniejszy
2. **Time Machine**: Option A (Horizontal Slider) - najbardziej intuicyjny
3. **Friendship**: Option B (Tag-based Input) - najlepszy UX
4. **Game Selector**: Option B (Searchable Select) - najlepszy dla wielu gier
5. **Registration**: Option C (Separate Page) - najczystsze rozwiązanie

---

## Mobile Considerations

- Time Machine slider: Touch-friendly, swipe gestures
- Tag input: Easy to remove tags on mobile
- Game selector: Full-screen modal on mobile
- Vertical layout works better on mobile

---

## Next Steps

1. ✅ Review proposals with team
2. ⏳ Create mockup/wireframe
3. ⏳ Implement backend (SearchQuery model)
4. ⏳ Implement frontend (HTML/CSS/JS)
5. ⏳ Test on mobile devices
6. ⏳ User testing

---

**Document Version**: 1.0  
**Last Updated**: 2024-12-19  
**Maintained By**: UX Engineer, Development Team


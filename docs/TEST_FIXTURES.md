# Test Fixtures Documentation

## Overview

This document describes the test fixtures used for E2E testing. All fixtures must be loaded before running Playwright E2E tests.

## Loading Fixtures

### Windows (PowerShell)
```powershell
.\load_fixtures.ps1
```

### Unix/Linux/MacOS
```bash
./load_fixtures.sh
```

### Using npm/pnpm script
```bash
pnpm load:fixtures
```

### Manual loading
```bash
pipenv run python manage.py loaddata app/fixtures/categories_fixtures.json
pipenv run python manage.py loaddata app/fixtures/games_fixtures.json
pipenv run python manage.py loaddata app/fixtures/users_and_characters.json
```

## Test Users

### testuser
- **Username**: `testuser`
- **Password**: `testpass123`
- **Email**: testuser@example.com
- **Profile Visibility**: PUBLIC
- **Description**: Main test user for E2E testing
- **Characters**:
  - `my-character-123` (hash: `myhash`) - World of Warcraft
  - `test-character-123` (hash: `testhash`) - The Elder Scrolls Online
  - `character-with-bio-123` (hash: `hash`) - World of Warcraft (has CharacterProfile)
  - `new-character-123` (hash: `newhash`) - Final Fantasy XIV

### otheruser
- **Username**: `otheruser`
- **Password**: `pass`
- **Email**: otheruser@example.com
- **Profile Visibility**: FRIENDS_ONLY
- **Description**: Secondary test user for E2E testing
- **Characters**:
  - `other-char-123` (hash: `otherhash`) - World of Warcraft

### privateuser
- **Username**: `privateuser`
- **Password**: `testpass123`
- **Email**: privateuser@example.com
- **Profile Visibility**: PRIVATE
- **Description**: User with private profile for testing access restrictions
- **Characters**:
  - `private-char-123` (hash: `privatehash`) - Final Fantasy XIV

## Test Data Structure

### Users
- 7 users total including test users and existing users (oldschool_gamer, pro_gamer_girl, zentala, casual_bob, testuser, otheruser, privateuser)

### Characters
- Multiple characters per user
- Characters span different games (World of Warcraft, Final Fantasy XIV, The Elder Scrolls Online, Agar.io, Europa Universalis IV, etc.)

### Character Profiles
- 2 character profiles with custom bios:
  - `character-with-bio-123` - Has custom bio
  - `Zentaur` (zentala's character) - Has custom bio

### Character Friend Requests
- **PENDING**: 
  - DragonSlayer2000 → my-character-123 (testuser)
  - ShadowHunter → my-character-123 (testuser)
- **ACCEPTED**: 
  - test-character-123 → SpeedRunner (converted to friendship)
- **DECLINED**: 
  - ZenMage → my-character-123 (testuser)

### Character Friendships
- 3 active friendships:
  - Zentaur ↔ HealingMaster
  - PolandMafia* ↔ BobTheBlob
  - my-character-123 (testuser) ↔ other-char-123 (otheruser)

### Messages
- 11 messages in various conversation threads
- Different privacy modes (ANONYMOUS, REVEAL_IDENTITY)
- Mix of read/unread messages
- Conversations between:
  - Zentaur ↔ HealingMaster (3 messages, identity revealed)
  - PolandMafia* ↔ BobTheBlob (2 messages, mixed privacy)
  - ZenMage ↔ SpeedRunner (2 messages, mixed privacy)
  - my-character-123 (testuser) ↔ other-char-123 (otheruser) (3 messages, identity revealed)
  - DragonSlayer2000 → my-character-123 (testuser) (1 message, anonymous, unread)

## Testing Scenarios Covered

### Profile Testing
- Public profile display
- Friends-only profile access
- Private profile access restrictions
- Profile with bio
- Profile without bio
- Profile with social media links

### Character Testing
- Character detail page
- Character with custom profile/bio
- Character without profile
- Character edit functionality
- Character friend list
- Own characters vs other characters

### Friend Request Testing
- Send friend request
- View pending friend requests
- Accept friend request
- Decline friend request
- Friend request button visibility (own character, already friends, pending request)
- Friend request modal with character selector

### Messaging Testing
- Message list/conversations
- Send message
- Read/unread status
- Privacy modes (anonymous vs identity revealed)
- Message threads
- Conversations between different character pairs

### Friendship Testing
- Friend list display
- Friend cards
- Navigation to friend character detail
- Empty state when no friends
- Existing friendship badge

## Important Notes

1. **Database State**: Fixtures should be loaded on a clean database. If you encounter unique constraint errors, flush the database first:
   ```bash
   pipenv run python manage.py flush --noinput
   ```

2. **Test Dependencies**: All E2E tests assume fixtures are loaded. Tests will fail if data is missing.

3. **UUID Consistency**: CharacterFriend entries have character1.id < character2.id (enforced by model's save method).

4. **Password Hashes**: Passwords are properly hashed using Django's password hashing system.

5. **Date Consistency**: All dates are set to recent past to ensure they appear in relevant queries (messages, friend requests, etc.).

## Fixture Files

- `categories_fixtures.json` - Game categories (7 objects)
- `games_fixtures.json` - Games (17 objects)
- `users_and_characters.json` - Users, Characters, Profiles, Friend Requests, Friendships, Messages (comprehensive test data)


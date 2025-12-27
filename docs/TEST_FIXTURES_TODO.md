# Test Fixtures - TODO / Issues to Fix

## Test Results Summary
- ✅ 38 tests passing
- ❌ 52 tests failing (mostly timeout issues during login)

## Known Issues

### 1. Timeout Issues During Login
**Problem**: Most tests are timing out when trying to log in (waiting for `#id_login`).

**Possible Causes**:
- Django server not running during tests
- Server not accessible at `http://localhost:8000`
- Login page structure changed

**Solution Needed**:
- Ensure Django server is running before running tests
- Add server health check in test setup
- Consider using Playwright's `webServer` configuration in `playwright.config.ts`

### 2. User Profile Display Test
**Test**: `tests/e2e/profile/user-profile-display.spec.ts` - "should display public profile"

**Error**: `expect(locator).toBeVisible() failed` for `h2:has-text("testuser")`

**Possible Causes**:
- Template doesn't have `h2` with username text
- Template structure changed
- Username displayed differently (e.g., in `h1` or different element)

**Solution Needed**:
- Check actual template structure (`app/templates/profile/user_profile_display_content.html`)
- Update test selector to match actual template

### 3. Character Profile Edit URL Pattern
**Fixed**: Updated regex pattern in `character-profile-edit.spec.ts` to handle URLs with or without trailing slash.

### 4. Strict Mode Violation in Friend List Test
**Fixed**: Added `.first()` to viewButton locator to handle multiple matching elements.

### 5. Character Friend List - Multiple Friends
**Test**: `tests/e2e/friends/character-friend-list.spec.ts` - "should navigate to friend character detail"

**Fixed**: Added `.first()` to handle strict mode violation when multiple friend cards exist.

## Next Steps

1. **Ensure Django Server Running**:
   - Add server startup to test setup
   - Or configure Playwright's `webServer` in `playwright.config.ts`

2. **Fix Template Selectors**:
   - Review actual template HTML structure
   - Update test selectors to match templates

3. **Add Missing Tests**:
   - Message functionality tests
   - More comprehensive friendship tests
   - Profile visibility tests
   - Character profile display tests with different scenarios

4. **Improve Test Robustness**:
   - Add retry logic for flaky tests
   - Improve error messages
   - Add more detailed assertions

## Test Data Coverage

Current fixtures provide:
- ✅ 3 test users (testuser, otheruser, privateuser)
- ✅ Multiple characters per user
- ✅ Character profiles with custom bios
- ✅ Friend requests in different states (PENDING, ACCEPTED, DECLINED)
- ✅ Active friendships
- ✅ Messages in various conversation threads

## Fixture Loading

Fixtures loaded successfully:
- Categories: 7 objects
- Games: 17 objects  
- Users, Characters, Messages, Friend Requests, Friendships: 43 objects

All fixture data is correctly structured and loads without errors.


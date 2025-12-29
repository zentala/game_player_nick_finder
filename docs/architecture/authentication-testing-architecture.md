# Authentication & Navigation Testing Architecture

**Status**: 📋 Design Document - Ready for Implementation  
**Last Updated**: 2024-12-19  
**Audience**: Mid-level Developers, QA Engineers  
**Story Points Estimate**: 13 SP (3-4 days)

## Document Purpose

This document describes the test architecture for authentication flows and navigation menu links in the Game Player Nick Finder application. It provides a comprehensive testing strategy and implementation guide for mid-level developers.

## Current Test Coverage Analysis

### ✅ Existing Test Coverage

The following features currently have E2E tests:
- ✅ Character profiles (display, edit)
- ✅ Friend system (requests, lists)
- ✅ User profiles (display, edit)

### ❌ Missing Test Coverage

The following critical authentication flows are **NOT covered** by tests:
- ❌ User login flow
- ❌ User logout flow
- ❌ User registration (signup) flow
- ❌ Password reset flow
- ❌ Password change flow
- ❌ Navigation menu links (all)
- ❌ Protected route access (authentication required)
- ❌ Redirect after login/logout

## Testing Architecture Overview

### Test Structure

```
tests/
├── e2e/
│   ├── auth/                          # NEW: Authentication tests
│   │   ├── login.spec.ts              # Login flow tests
│   │   ├── logout.spec.ts             # Logout flow tests
│   │   ├── signup.spec.ts             # Registration flow tests
│   │   ├── password-reset.spec.ts     # Password reset flow tests
│   │   ├── password-change.spec.ts    # Password change flow tests
│   │   └── auth-helpers.ts            # Helper functions for auth
│   ├── navigation/                    # NEW: Navigation tests
│   │   ├── navbar-authenticated.spec.ts    # Navbar links for logged-in users
│   │   ├── navbar-unauthenticated.spec.ts  # Navbar links for guests
│   │   └── menu-navigation.spec.ts         # Menu navigation flows
│   ├── friends/                       # EXISTING
│   ├── profile/                       # EXISTING
│   └── characters/                    # EXISTING
└── helpers/                           # NEW: Shared test utilities
    └── auth-helpers.ts                # Authentication helper functions
```

### Test Helper Functions

**CRITICAL**: Create shared helper functions to avoid code duplication and improve maintainability.

**Location**: `tests/helpers/auth-helpers.ts`

```typescript
import { Page } from '@playwright/test';

/**
 * Login helper function
 * Logs in a user and waits for redirect to home page
 */
export async function login(
  page: Page,
  username: string,
  password: string
): Promise<void> {
  await page.goto('/accounts/login/');
  await page.fill('#id_login', username);
  await page.fill('#id_password', password);
  await page.click('button[type="submit"]');
  await page.waitForURL('**/');
}

/**
 * Logout helper function
 * Logs out current user and waits for redirect
 */
export async function logout(page: Page): Promise<void> {
  // Click user menu dropdown
  await page.click('nav .dropdown-toggle');
  // Click logout link
  await page.click('a:has-text("Log out")');
  // Wait for redirect (usually to home page)
  await page.waitForURL('**/');
}

/**
 * Check if user is authenticated
 * Verifies presence of user menu in navbar
 */
export async function isAuthenticated(page: Page): Promise<boolean> {
  const userMenu = page.locator('nav .dropdown-toggle');
  return (await userMenu.count()) > 0;
}

/**
 * Check if user is not authenticated
 * Verifies presence of login/register links in navbar
 */
export async function isNotAuthenticated(page: Page): Promise<boolean> {
  const loginLink = page.locator('a:has-text("Log in")');
  return (await loginLink.count()) > 0;
}

/**
 * Test user credentials from fixtures
 */
export const TEST_USERS = {
  main: { username: 'testuser', password: 'testpass123' },
  secondary: { username: 'otheruser', password: 'pass' },
  private: { username: 'privateuser', password: 'testpass123' },
} as const;
```

## Implementation Tasks

### Task 1: Create Authentication Helper Functions

**Story Points**: 2  
**Priority**: High  
**Estimated Time**: 2-3 hours

#### Description

Create shared helper functions for authentication operations that will be reused across all authentication tests.

#### Steps

1. **Create helpers directory**:
   ```bash
   mkdir -p tests/helpers
   ```

2. **Create `tests/helpers/auth-helpers.ts`**:
   - Implement `login()` function
   - Implement `logout()` function
   - Implement `isAuthenticated()` function
   - Implement `isNotAuthenticated()` function
   - Define `TEST_USERS` constant
   - Export all functions

3. **Verify helper functions**:
   - Test each function manually in a simple test
   - Ensure functions work correctly with test fixtures

#### Acceptance Criteria

- [ ] `tests/helpers/auth-helpers.ts` file created
- [ ] All helper functions implemented and exported
- [ ] Helper functions tested and working
- [ ] Functions handle errors gracefully (timeouts, element not found)
- [ ] Code follows TypeScript best practices
- [ ] Functions have JSDoc comments

---

### Task 2: Login Flow Tests

**Story Points**: 3  
**Priority**: High  
**Estimated Time**: 4-5 hours

#### Description

Create comprehensive tests for the user login flow covering successful login, failed login, and edge cases.

#### Test File

`tests/e2e/auth/login.spec.ts`

#### Test Cases to Implement

1. **Successful Login**:
   - Navigate to login page
   - Fill in valid credentials
   - Submit form
   - Verify redirect to home page
   - Verify user menu appears in navbar
   - Verify user is authenticated

2. **Failed Login - Invalid Username**:
   - Navigate to login page
   - Fill in invalid username with valid password
   - Submit form
   - Verify error message displayed
   - Verify still on login page
   - Verify user is NOT authenticated

3. **Failed Login - Invalid Password**:
   - Navigate to login page
   - Fill in valid username with invalid password
   - Submit form
   - Verify error message displayed
   - Verify still on login page
   - Verify user is NOT authenticated

4. **Failed Login - Empty Fields**:
   - Navigate to login page
   - Submit form without filling fields
   - Verify validation errors displayed
   - Verify form is not submitted

5. **Login Form Elements**:
   - Navigate to login page
   - Verify login form is present
   - Verify username/email field is present
   - Verify password field is present
   - Verify "Remember me" checkbox is present (if applicable)
   - Verify "Forgot Password?" link is present
   - Verify submit button is present

6. **Login Redirect After Authentication**:
   - Navigate to protected page (e.g., `/accounts/profile/`)
   - Verify redirect to login page
   - Login with valid credentials
   - Verify redirect back to originally requested page

7. **Login with "Remember Me"**:
   - Navigate to login page
   - Fill in credentials
   - Check "Remember me" checkbox (if exists)
   - Submit form
   - Verify login successful
   - Close browser
   - Reopen browser and navigate to site
   - Verify user is still logged in (session persists)

8. **Already Logged In User**:
   - Login as user
   - Navigate to login page
   - Verify redirect to home page (or appropriate page)
   - Verify appropriate message displayed (if any)

#### Implementation Steps

1. Create `tests/e2e/auth/login.spec.ts`
2. Import necessary Playwright functions and auth helpers
3. Write test cases following existing test patterns
4. Use helper functions from `auth-helpers.ts`
5. Use test users from fixtures (`testuser`, `otheruser`)
6. Run tests and fix any issues

#### Acceptance Criteria

- [ ] All 8 test cases implemented
- [ ] Tests use helper functions (no code duplication)
- [ ] Tests pass with fixtures loaded
- [ ] Tests handle edge cases (element not found, timeouts)
- [ ] Tests follow existing code style
- [ ] Tests are readable and well-commented

---

### Task 3: Logout Flow Tests

**Story Points**: 2  
**Priority**: High  
**Estimated Time**: 2-3 hours

#### Description

Create tests for the user logout flow.

#### Test File

`tests/e2e/auth/logout.spec.ts`

#### Test Cases to Implement

1. **Successful Logout**:
   - Login as user
   - Click user menu dropdown
   - Click "Log out" link
   - Verify redirect (usually to home page)
   - Verify user menu no longer visible
   - Verify login/register links visible
   - Verify user is NOT authenticated

2. **Logout Button Accessibility**:
   - Login as user
   - Verify user menu dropdown is visible
   - Click dropdown to open menu
   - Verify "Log out" link is visible
   - Verify "Log out" link is clickable

3. **Logout from Different Pages**:
   - Login as user
   - Navigate to profile page
   - Logout
   - Verify logout successful
   - Repeat for other pages (characters, games, messages)

4. **Logout and Re-login**:
   - Login as user
   - Logout
   - Verify user is logged out
   - Login again with same credentials
   - Verify login successful

5. **Unauthenticated User Cannot Logout**:
   - Navigate to site without logging in
   - Verify logout link is NOT visible
   - Try to access logout URL directly
   - Verify appropriate response (redirect or error)

#### Implementation Steps

1. Create `tests/e2e/auth/logout.spec.ts`
2. Import necessary Playwright functions and auth helpers
3. Write test cases following existing test patterns
4. Use `login()` and `logout()` helper functions
5. Test logout from various pages
6. Run tests and fix any issues

#### Acceptance Criteria

- [ ] All 5 test cases implemented
- [ ] Tests use helper functions
- [ ] Tests pass with fixtures loaded
- [ ] Tests verify logout from multiple pages
- [ ] Tests follow existing code style

---

### Task 4: Registration (Signup) Flow Tests

**Story Points**: 3  
**Priority**: High  
**Estimated Time**: 4-5 hours

#### Description

Create comprehensive tests for the user registration (signup) flow.

#### Test File

`tests/e2e/auth/signup.spec.ts`

#### Test Cases to Implement

1. **Successful Registration**:
   - Navigate to signup page (`/accounts/signup/`)
   - Fill in all required fields with valid data
   - Submit form
   - Verify redirect to appropriate page (usually home or profile)
   - Verify user is authenticated
   - Verify user menu appears in navbar
   - Verify success message displayed (if any)

2. **Registration Form Elements**:
   - Navigate to signup page
   - Verify all form fields are present:
     - Username field
     - Email field (if required)
     - Password field
     - Password confirmation field (if exists)
   - Verify submit button is present
   - Verify "Already have an account? Sign in" link is present

3. **Registration Validation - Empty Fields**:
   - Navigate to signup page
   - Submit form without filling fields
   - Verify validation errors displayed
   - Verify form is not submitted

4. **Registration Validation - Invalid Email**:
   - Navigate to signup page
   - Fill in fields with invalid email format
   - Submit form
   - Verify email validation error displayed

5. **Registration Validation - Password Too Short**:
   - Navigate to signup page
   - Fill in fields with password shorter than minimum length
   - Submit form
   - Verify password validation error displayed

6. **Registration Validation - Password Mismatch**:
   - Navigate to signup page
   - Fill in password and different password confirmation
   - Submit form
   - Verify password mismatch error displayed

7. **Registration Validation - Username Already Exists**:
   - Navigate to signup page
   - Fill in username that already exists (e.g., `testuser`)
   - Fill in other valid fields
   - Submit form
   - Verify username already exists error displayed

8. **Registration Validation - Email Already Exists**:
   - Navigate to signup page
   - Fill in email that already exists
   - Fill in other valid fields
   - Submit form
   - Verify email already exists error displayed (if email uniqueness is enforced)

9. **Registration Redirect After Login**:
   - Login as existing user
   - Navigate to signup page
   - Verify redirect to home page (or appropriate page)
   - Verify appropriate message displayed (if any)

10. **Registration Link in Navbar**:
    - Navigate to site without logging in
    - Verify "Register" link is visible in navbar
    - Click "Register" link
    - Verify navigation to signup page

#### Implementation Steps

1. Create `tests/e2e/auth/signup.spec.ts`
2. Import necessary Playwright functions and auth helpers
3. Write test cases following existing test patterns
4. Use helper functions where applicable
5. Generate unique test usernames/emails for successful registration tests (to avoid conflicts)
6. Run tests and fix any issues

#### Acceptance Criteria

- [ ] All 10 test cases implemented
- [ ] Tests use helper functions where applicable
- [ ] Tests pass with fixtures loaded
- [ ] Tests handle validation errors correctly
- [ ] Tests generate unique test data to avoid conflicts
- [ ] Tests follow existing code style

---

### Task 5: Password Reset Flow Tests

**Story Points**: 3  
**Priority**: Medium  
**Estimated Time**: 4-5 hours

#### Description

Create comprehensive tests for the password reset flow.

#### Test File

`tests/e2e/auth/password-reset.spec.ts`

#### Test Cases to Implement

1. **Password Reset Request Form**:
   - Navigate to password reset page (`/accounts/password_reset/`)
   - Verify form is present
   - Verify email field is present
   - Verify submit button is present
   - Verify "Back to login" link is present (if exists)

2. **Successful Password Reset Request**:
   - Navigate to password reset page
   - Fill in valid email address (existing user)
   - Submit form
   - Verify redirect to password reset done page (`/accounts/password_reset/done/`)
   - Verify success message displayed (e.g., "We have sent you an e-mail...")
   - **Note**: In development, email is printed to console, so verify console output or mock email

3. **Password Reset Request - Invalid Email**:
   - Navigate to password reset page
   - Fill in email that doesn't exist
   - Submit form
   - Verify error message displayed (or verify redirect with message - behavior depends on Django settings)

4. **Password Reset Request - Empty Email**:
   - Navigate to password reset page
   - Submit form without filling email
   - Verify validation error displayed

5. **Password Reset Link Access**:
   - **Note**: This test requires email token, which is complex in E2E tests
   - Option 1: Mock email service and extract token
   - Option 2: Use Django management command to get reset token
   - Option 3: Skip this test if too complex, document in unit tests
   - If implemented:
     - Get password reset token for test user
     - Navigate to password reset confirm page (`/accounts/reset/<uidb64>/<token>/`)
     - Verify form is present
     - Fill in new password
     - Submit form
     - Verify redirect to password reset complete page
     - Verify password changed successfully

6. **Password Reset Complete**:
   - After successful password reset (if test 5 implemented)
   - Verify redirect to password reset complete page (`/accounts/reset/done/`)
   - Verify success message displayed
   - Verify "Back to login" link is present (if exists)

7. **Password Reset Link - Invalid Token**:
   - Navigate to password reset confirm page with invalid token
   - Verify error message displayed (e.g., "The password reset link was invalid...")

8. **Password Reset Link - Expired Token**:
   - **Note**: Requires token expiration setup, may be complex
   - Create expired reset token
   - Navigate to password reset confirm page
   - Verify error message displayed

9. **Password Reset Link in Login Form**:
   - Navigate to login page
   - Verify "Forgot Password?" link is present
   - Click "Forgot Password?" link
   - Verify navigation to password reset page

#### Implementation Steps

1. Create `tests/e2e/auth/password-reset.spec.ts`
2. Import necessary Playwright functions and auth helpers
3. Write test cases following existing test patterns
4. For token-based tests, decide on approach (mock, management command, or skip)
5. Run tests and fix any issues

#### Acceptance Criteria

- [ ] Test cases 1-4, 7, 9 implemented (basic flow)
- [ ] Test cases 5-6 implemented if feasible (token handling)
- [ ] Test case 8 implemented if feasible (token expiration)
- [ ] Tests use helper functions where applicable
- [ ] Tests pass with fixtures loaded
- [ ] Tests handle email console output appropriately
- [ ] Tests follow existing code style

---

### Task 6: Password Change Flow Tests

**Story Points**: 2  
**Priority**: Medium  
**Estimated Time**: 3-4 hours

#### Description

Create comprehensive tests for the password change flow (for authenticated users).

#### Test File

`tests/e2e/auth/password-change.spec.ts`

#### Test Cases to Implement

1. **Password Change Form Access**:
   - Login as user
   - Navigate to password change page (`/accounts/password_change/`)
   - Verify form is present
   - Verify old password field is present
   - Verify new password field is present
   - Verify new password confirmation field is present
   - Verify submit button is present

2. **Password Change Form via Menu**:
   - Login as user
   - Click user menu dropdown
   - Click "Change password" link
   - Verify navigation to password change page

3. **Successful Password Change**:
   - Login as user
   - Navigate to password change page
   - Fill in old password (correct)
   - Fill in new password (valid)
   - Fill in new password confirmation (matches)
   - Submit form
   - Verify redirect to password change done page (`/accounts/password_change/done/`)
   - Verify success message displayed
   - Logout and login with new password
   - Verify login successful

4. **Password Change Validation - Wrong Old Password**:
   - Login as user
   - Navigate to password change page
   - Fill in wrong old password
   - Fill in new password
   - Submit form
   - Verify error message displayed (e.g., "Your old password was entered incorrectly...")

5. **Password Change Validation - New Password Too Short**:
   - Login as user
   - Navigate to password change page
   - Fill in old password (correct)
   - Fill in new password shorter than minimum length
   - Submit form
   - Verify password validation error displayed

6. **Password Change Validation - Password Mismatch**:
   - Login as user
   - Navigate to password change page
   - Fill in old password (correct)
   - Fill in new password
   - Fill in different password confirmation
   - Submit form
   - Verify password mismatch error displayed

7. **Password Change Validation - Empty Fields**:
   - Login as user
   - Navigate to password change page
   - Submit form without filling fields
   - Verify validation errors displayed

8. **Password Change - Unauthenticated Access**:
   - Navigate to password change page without logging in
   - Verify redirect to login page
   - Verify redirect back to password change page after login

9. **Password Change Done Page**:
   - After successful password change
   - Verify redirect to password change done page
   - Verify success message displayed
   - Verify "Back to profile" or similar link is present (if exists)

#### Implementation Steps

1. Create `tests/e2e/auth/password-change.spec.ts`
2. Import necessary Playwright functions and auth helpers
3. Write test cases following existing test patterns
4. Use `login()` helper function
5. Test password change and verify new password works
6. Run tests and fix any issues

#### Acceptance Criteria

- [ ] All 9 test cases implemented
- [ ] Tests use helper functions
- [ ] Tests pass with fixtures loaded
- [ ] Tests verify new password works after change
- [ ] Tests follow existing code style

---

### Task 7: Navigation Menu Tests - Authenticated Users

**Story Points**: 2  
**Priority**: High  
**Estimated Time**: 3-4 hours

#### Description

Create tests for navigation menu links for authenticated users.

#### Test File

`tests/e2e/navigation/navbar-authenticated.spec.ts`

#### Menu Items to Test

From `base_navbar.html`:
- Home (`/`)
- Characters (`/characters/`)
- Games (`/games/`)
- User Menu Dropdown:
  - Profile (`/accounts/profile/`)
  - My characters (`/account/characters/`)
  - Messages (`/messages/`)
  - Change password (`/accounts/password_change/`)
  - Admin Panel (only for superuser) (`/admin/`)
  - Log out (`/accounts/logout/`)

#### Test Cases to Implement

1. **Navbar Visibility**:
   - Login as user
   - Verify navbar is visible on all pages
   - Verify user menu dropdown is visible
   - Verify user avatar/name is visible

2. **Main Menu Links - Home**:
   - Login as user
   - Click "Home" link
   - Verify navigation to home page (`/`)
   - Verify correct page content loaded

3. **Main Menu Links - Characters**:
   - Login as user
   - Click "Characters" link
   - Verify navigation to characters list page (`/characters/`)
   - Verify correct page content loaded

4. **Main Menu Links - Games**:
   - Login as user
   - Click "Games" link
   - Verify navigation to games list page (`/games/`)
   - Verify correct page content loaded

5. **User Menu - Profile**:
   - Login as user
   - Click user menu dropdown
   - Click "Profile" link
   - Verify navigation to profile page (`/accounts/profile/`)
   - Verify correct page content loaded

6. **User Menu - My Characters**:
   - Login as user
   - Click user menu dropdown
   - Click "My characters" link
   - Verify navigation to user characters page (`/account/characters/`)
   - Verify correct page content loaded

7. **User Menu - Messages**:
   - Login as user
   - Click user menu dropdown
   - Click "Messages" link
   - Verify navigation to messages page (`/messages/`)
   - Verify correct page content loaded

8. **User Menu - Change Password**:
   - Login as user
   - Click user menu dropdown
   - Click "Change password" link
   - Verify navigation to password change page (`/accounts/password_change/`)
   - Verify correct page content loaded

9. **User Menu - Admin Panel (Superuser Only)**:
   - Login as superuser (if available in fixtures)
   - Click user menu dropdown
   - Verify "Admin Panel" link is visible
   - Click "Admin Panel" link
   - Verify navigation to admin page (`/admin/`)
   - Verify admin page is accessible

10. **User Menu - Admin Panel (Regular User)**:
    - Login as regular user (not superuser)
    - Click user menu dropdown
    - Verify "Admin Panel" link is NOT visible

11. **User Menu - Logout**:
    - Login as user
    - Click user menu dropdown
    - Click "Log out" link
    - Verify logout successful (covered in logout tests, but verify link works)

12. **Active Page Highlighting**:
    - Login as user
    - Navigate to different pages
    - Verify active page link is highlighted in navbar (if implemented)

#### Implementation Steps

1. Create `tests/e2e/navigation/navbar-authenticated.spec.ts`
2. Import necessary Playwright functions and auth helpers
3. Write test cases following existing test patterns
4. Use `login()` helper function
5. Test each menu link individually
6. Run tests and fix any issues

#### Acceptance Criteria

- [ ] All 12 test cases implemented
- [ ] Tests use helper functions
- [ ] Tests pass with fixtures loaded
- [ ] Tests verify correct page navigation for each link
- [ ] Tests verify correct page content loaded
- [ ] Tests follow existing code style

---

### Task 8: Navigation Menu Tests - Unauthenticated Users

**Story Points**: 1  
**Priority**: High  
**Estimated Time**: 2-3 hours

#### Description

Create tests for navigation menu links for unauthenticated (guest) users.

#### Test File

`tests/e2e/navigation/navbar-unauthenticated.spec.ts`

#### Menu Items to Test

From `base_navbar.html`:
- Home (`/`)
- Characters (`/characters/`)
- Games (`/games/`)
- Log in (`/accounts/login/`)
- Register (`/accounts/signup/`)

#### Test Cases to Implement

1. **Navbar Visibility**:
   - Navigate to site without logging in
   - Verify navbar is visible
   - Verify "Log in" and "Register" links are visible
   - Verify user menu dropdown is NOT visible

2. **Main Menu Links - Home**:
   - Navigate to site without logging in
   - Click "Home" link
   - Verify navigation to home page (`/`)
   - Verify correct page content loaded

3. **Main Menu Links - Characters**:
   - Navigate to site without logging in
   - Click "Characters" link
   - Verify navigation to characters list page (`/characters/`)
   - Verify correct page content loaded (or appropriate message if login required)

4. **Main Menu Links - Games**:
   - Navigate to site without logging in
   - Click "Games" link
   - Verify navigation to games list page (`/games/`)
   - Verify correct page content loaded

5. **Login Link**:
   - Navigate to site without logging in
   - Click "Log in" link
   - Verify navigation to login page (`/accounts/login/`)
   - Verify login form is present

6. **Register Link**:
   - Navigate to site without logging in
   - Click "Register" link
   - Verify navigation to signup page (`/accounts/signup/`)
   - Verify signup form is present

7. **Protected Route Access**:
   - Navigate to protected page without logging in (e.g., `/accounts/profile/`)
   - Verify redirect to login page
   - Verify redirect back to originally requested page after login

8. **Active Page Highlighting**:
   - Navigate to different pages without logging in
   - Verify active page link is highlighted in navbar (if implemented)

#### Implementation Steps

1. Create `tests/e2e/navigation/navbar-unauthenticated.spec.ts`
2. Import necessary Playwright functions and auth helpers
3. Write test cases following existing test patterns
4. Use `isNotAuthenticated()` helper function where applicable
5. Test each menu link individually
6. Run tests and fix any issues

#### Acceptance Criteria

- [ ] All 8 test cases implemented
- [ ] Tests use helper functions where applicable
- [ ] Tests pass without fixtures (or with fixtures loaded)
- [ ] Tests verify correct page navigation for each link
- [ ] Tests verify protected routes redirect to login
- [ ] Tests follow existing code style

---

## Implementation Guidelines

### Code Style

Follow existing test patterns from `tests/e2e/friends/friend-request-button.spec.ts`:

```typescript
import { test, expect } from '@playwright/test';
import { login, logout, isAuthenticated, TEST_USERS } from '../../helpers/auth-helpers';

test.describe('Feature Name', () => {
  test.beforeEach(async ({ page }) => {
    // Setup if needed
    await login(page, TEST_USERS.main.username, TEST_USERS.main.password);
  });

  test('should do something', async ({ page }) => {
    // Arrange
    await page.goto('/some/page/');
    
    // Act
    await page.click('button:has-text("Click Me")');
    
    // Assert
    await expect(page.locator('text=Success')).toBeVisible();
  });
});
```

### Test Data

- **Use fixtures**: Always load fixtures before running tests (`pnpm load:fixtures`)
- **Test users**: Use predefined test users from `TEST_USERS` constant:
  - `TEST_USERS.main` - Main test user (testuser/testpass123)
  - `TEST_USERS.secondary` - Secondary test user (otheruser/pass)
  - `TEST_USERS.private` - Private profile user (privateuser/testpass123)

### Error Handling

- Use `if (await element.count() > 0)` pattern for conditional elements
- Add appropriate waits (`await page.waitForURL()`, `await page.waitForSelector()`)
- Handle timeouts gracefully
- Verify element exists before interacting with it

### Running Tests

```bash
# Load fixtures first (REQUIRED)
pnpm load:fixtures

# Run all tests
pnpm test:e2e

# Run specific test file
pnpm test:e2e tests/e2e/auth/login.spec.ts

# Run tests in UI mode (interactive)
pnpm test:e2e:ui

# Run tests in headed mode (see browser)
pnpm test:e2e:headed
```

## Testing Checklist

After implementing each task, verify:

- [ ] All tests pass with fixtures loaded
- [ ] Tests run in headless mode
- [ ] Tests are not flaky (run 3 times, all pass)
- [ ] Code follows existing patterns
- [ ] Helper functions are reused (no duplication)
- [ ] Tests are readable and well-commented
- [ ] Error handling is appropriate
- [ ] Tests verify both success and failure cases

## Priority Order

Implement tasks in this order:

1. **Task 1**: Create Authentication Helper Functions (prerequisite for other tasks)
2. **Task 2**: Login Flow Tests (high priority, fundamental feature)
3. **Task 3**: Logout Flow Tests (high priority, fundamental feature)
4. **Task 7**: Navigation Menu Tests - Authenticated Users (high priority, user experience)
5. **Task 8**: Navigation Menu Tests - Unauthenticated Users (high priority, user experience)
6. **Task 4**: Registration Flow Tests (high priority, user acquisition)
7. **Task 6**: Password Change Flow Tests (medium priority)
8. **Task 5**: Password Reset Flow Tests (medium priority, complex token handling)

## Estimated Timeline

- **Task 1**: 2-3 hours
- **Task 2**: 4-5 hours
- **Task 3**: 2-3 hours
- **Task 4**: 4-5 hours
- **Task 5**: 4-5 hours
- **Task 6**: 3-4 hours
- **Task 7**: 3-4 hours
- **Task 8**: 2-3 hours

**Total**: 24-32 hours (3-4 days for one developer)

## Dependencies

- Django server running on `http://localhost:7600`
- Test fixtures loaded (`pnpm load:fixtures`)
- Playwright browsers installed (`pnpx playwright install`)
- All dependencies installed (`pnpm install`, `pipenv install`)

## Notes

- **Email Testing**: Password reset tests may require email mock setup or Django console email backend verification
- **Token Testing**: Password reset token tests may be complex; consider simplifying or documenting limitations
- **Multi-step Registration**: The project has multi-step registration (`register/step1/`, etc.) but uses `account_signup` in navbar - verify which one is actually used
- **Session Testing**: "Remember me" functionality may require session persistence testing
- **Admin Panel**: Admin panel tests require superuser in fixtures - verify if available

## Success Criteria

All authentication and navigation flows are covered by E2E tests:
- ✅ Users can login successfully
- ✅ Users can logout successfully
- ✅ Users can register successfully
- ✅ Users can reset passwords
- ✅ Users can change passwords
- ✅ All navigation menu links work correctly
- ✅ Protected routes redirect appropriately
- ✅ Authentication state is verified correctly

---

**Document Version**: 1.0  
**Last Updated**: 2024-12-19  
**Author**: Software Architect  
**Reviewers**: Tech Lead, QA Lead



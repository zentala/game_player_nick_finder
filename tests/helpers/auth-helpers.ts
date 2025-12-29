import { Page, expect } from '@playwright/test';

/**
 * Login helper function
 * Logs in a user and waits for redirect to home page
 * 
 * Note: This function does not verify user menu visibility as it can be unreliable
 * due to timing issues and different page structures. Tests should use isAuthenticated()
 * if they need to verify authentication status.
 */
export async function login(
  page: Page,
  username: string,
  password: string
): Promise<void> {
  // KROK 1: Sprawdź, czy użytkownik jest już zalogowany
  // CustomLoginView ma redirect_authenticated_user = True
  // Jeśli użytkownik jest już zalogowany, redirect nastąpi natychmiast
  await page.goto('/accounts/login/');
  
  // KROK 2: Czekaj na redirect (jeśli użytkownik jest już zalogowany)
  // Jeśli redirect nastąpi, użytkownik jest już zalogowany - zwróć sukces
  try {
    await page.waitForURL(/\/(?!accounts\/login)/, { timeout: 2000 });
    // Redirect nastąpił - użytkownik jest już zalogowany
    // Weryfikuj, że użytkownik jest faktycznie zalogowany
    await page.waitForLoadState('networkidle');
    const loginLink = page.locator('a:has-text("Log in")');
    const hasLoginLink = await loginLink.count() > 0;
    if (!hasLoginLink) {
      // User is authenticated, login successful - RETURN IMMEDIATELY
      // Don't try to login again, as this will cause "Please enter correct username" error
      return;
    }
    // If login link is visible, user is NOT logged in, continue with login
  } catch (error) {
    // Redirect nie nastąpił w ciągu 2 sekund - użytkownik prawdopodobnie nie jest zalogowany
    // Sprawdź jeszcze raz URL - może redirect nastąpił później
    await page.waitForTimeout(500);
    const currentURL = page.url();
    if (!currentURL.includes('/accounts/login/')) {
      // Redirect nastąpił później - użytkownik jest już zalogowany
      await page.waitForLoadState('networkidle');
      const loginLink = page.locator('a:has-text("Log in")');
      const hasLoginLink = await loginLink.count() > 0;
      if (!hasLoginLink) {
        // User is authenticated, login successful - RETURN IMMEDIATELY
        return;
      }
    }
    // Jeśli nadal jesteśmy na /accounts/login/, kontynuuj logowanie
  }
  
  // KROK 3: Normalne logowanie (użytkownik nie jest zalogowany)
  // WAŻNE: Sprawdź jeszcze raz, czy nie jesteśmy już zalogowani (może redirect nastąpił w międzyczasie)
  const currentURLBeforeLogin = page.url();
  if (!currentURLBeforeLogin.includes('/accounts/login/')) {
    // Nie jesteśmy na stronie logowania - użytkownik jest już zalogowany
    await page.waitForLoadState('networkidle');
    const loginLink = page.locator('a:has-text("Log in")');
    const hasLoginLink = await loginLink.count() > 0;
    if (!hasLoginLink) {
      // User is authenticated, login successful - RETURN IMMEDIATELY
      return;
    }
  }
  
  await page.waitForLoadState('networkidle');
  
  // Wait for form fields to be visible before filling (CRITICAL - fixes timing issues)
  // Use EXACT same selectors and pattern as login.spec.ts that works (100% passing)
  // CustomLoginView uses Django AuthenticationForm (username field), not allauth LoginForm (login field)
  await expect(page.locator('#id_username')).toBeVisible({ timeout: 5000 });
  await expect(page.locator('#id_password')).toBeVisible({ timeout: 5000 });
  
  // Fill in credentials - use EXACT same code as login.spec.ts (100% passing)
  await page.fill('#id_username', username);
  await page.fill('#id_password', password);
  
  // Verify fields are filled (CRITICAL - throw error if not filled, don't just warn)
  // This is EXACT same verification as in login.spec.ts
  const usernameValue = await page.locator('#id_username').inputValue();
  const passwordValue = await page.locator('#id_password').inputValue();
  
  if (usernameValue !== username || passwordValue.length === 0) {
    throw new Error(`Fields not filled correctly. Username: ${usernameValue} (expected: ${username}), Password length: ${passwordValue.length}`);
  }
  
  // Submit form - use EXACT same pattern as login.spec.ts that works (100% passing)
  await page.click('button[type="submit"]');
  
  // Wait for redirect to home page (same pattern as login.spec.ts)
  await page.waitForURL('**/', { timeout: 15000 });
  
  // Wait for page to fully load after navigation
  await page.waitForLoadState('networkidle');
  
  // Final check: Verify we're not still on login page (indicates login failure)
  const finalURL = page.url();
  if (finalURL.includes('/accounts/login/')) {
    const finalErrors = await page.locator('.alert-danger, .errorlist, .invalid-feedback').allTextContents();
    throw new Error(
      `Login failed - still on login page after redirect wait. ` +
      `Errors: ${finalErrors.join(', ')}. ` +
      `Please ensure test user '${username}' exists and fixtures are loaded.`
    );
  }
  
  // Note: We don't verify user menu visibility here because:
  // 1. Redirect is a sufficient indicator of successful login
  // 2. Menu may not be visible due to timing or page structure differences
  // 3. Tests can use isAuthenticated() if they need explicit verification
}

/**
 * Opens user dropdown menu and waits for it to be visible
 * Handles Bootstrap dropdown animation timing
 */
export async function openUserMenu(page: Page): Promise<void> {
  const userMenu = page.locator('a.nav-link.dropdown-toggle').first();
  await expect(userMenu).toBeVisible({ timeout: 10000 });
  await userMenu.click();
  await page.waitForSelector('.dropdown-menu.show', { state: 'visible', timeout: 2000 });
  await page.waitForTimeout(200); // Safety buffer for animation completion
}

/**
 * Logout helper function
 * Logs out current user and waits for redirect
 */
export async function logout(page: Page): Promise<void> {
  // Open user menu dropdown with proper wait
  await openUserMenu(page);
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
  // Metoda 1: Sprawdź, czy login link jest widoczny (jeśli nie, użytkownik jest zalogowany)
  const loginLink = page.locator('a:has-text("Log in")');
  const hasLoginLink = await loginLink.count() > 0;
  
  if (hasLoginLink) {
    // Login link jest widoczny - użytkownik NIE jest zalogowany
    return false;
  }
  
  // Metoda 2: Sprawdź, czy user menu jest widoczny
  const userMenu = page.locator('a.nav-link.dropdown-toggle, a.dropdown-toggle, [data-toggle="dropdown"]').first();
  const hasUserMenu = await userMenu.count() > 0;
  
  if (hasUserMenu) {
    // User menu jest widoczny - użytkownik JEST zalogowany
    return true;
  }
  
  // Metoda 3: Sprawdź URL - jeśli jesteśmy na /accounts/login/, użytkownik NIE jest zalogowany
  const currentURL = page.url();
  if (currentURL.includes('/accounts/login/')) {
    return false;
  }
  
  // Jeśli żadna metoda nie zadziałała, zwróć false (bezpieczniejsze)
  return false;
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



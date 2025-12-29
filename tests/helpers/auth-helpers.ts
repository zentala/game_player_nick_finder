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
  await page.fill('#id_username', username);
  await page.fill('#id_password', password);
  await page.click('button[type="submit"]');
  await page.waitForURL('**/');
}

/**
 * Opens user dropdown menu and waits for it to be visible
 * Handles Bootstrap dropdown animation timing
 */
export async function openUserMenu(page: Page): Promise<void> {
  await page.click('nav .dropdown-toggle');
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



import { test, expect } from '@playwright/test';
import { login, logout, isAuthenticated, isNotAuthenticated, TEST_USERS } from '../../helpers/auth-helpers';

test.describe('Logout Flow', () => {
  test('should successfully logout user', async ({ page }) => {
    // Login first
    await login(page, TEST_USERS.main.username, TEST_USERS.main.password);
    
    // Verify user is authenticated
    let authenticated = await isAuthenticated(page);
    expect(authenticated).toBe(true);
    
    // Click user menu dropdown
    await page.click('nav .dropdown-toggle');
    
    // Click logout link
    await page.click('a:has-text("Log out")');
    
    // Wait for redirect (usually to home page)
    await page.waitForURL('**/');
    
    // Verify user menu no longer visible
    await expect(page.locator('nav .dropdown-toggle')).not.toBeVisible();
    
    // Verify login/register links visible
    const loginLink = page.locator('a:has-text("Log in")');
    await expect(loginLink).toBeVisible();
    
    // Verify user is NOT authenticated
    authenticated = await isAuthenticated(page);
    expect(authenticated).toBe(false);
    
    // Verify user is not authenticated (alternative check)
    const notAuthenticated = await isNotAuthenticated(page);
    expect(notAuthenticated).toBe(true);
  });

  test('should have logout button accessible in user menu', async ({ page }) => {
    // Login first
    await login(page, TEST_USERS.main.username, TEST_USERS.main.password);
    
    // Verify user menu dropdown is visible
    const userMenu = page.locator('nav .dropdown-toggle');
    await expect(userMenu).toBeVisible();
    
    // Click dropdown to open menu
    await userMenu.click();
    
    // Verify "Log out" link is visible
    const logoutLink = page.locator('a:has-text("Log out")');
    await expect(logoutLink).toBeVisible();
    
    // Verify "Log out" link is clickable
    await expect(logoutLink).toBeEnabled();
  });

  test('should logout from different pages', async ({ page }) => {
    // Login first
    await login(page, TEST_USERS.main.username, TEST_USERS.main.password);
    
    // Test logout from profile page
    await page.goto('/accounts/profile/');
    await logout(page);
    
    // Verify logout successful
    let authenticated = await isAuthenticated(page);
    expect(authenticated).toBe(false);
    
    // Login again
    await login(page, TEST_USERS.main.username, TEST_USERS.main.password);
    
    // Test logout from characters page
    await page.goto('/characters/');
    await logout(page);
    
    // Verify logout successful
    authenticated = await isAuthenticated(page);
    expect(authenticated).toBe(false);
    
    // Login again
    await login(page, TEST_USERS.main.username, TEST_USERS.main.password);
    
    // Test logout from games page
    await page.goto('/games/');
    await logout(page);
    
    // Verify logout successful
    authenticated = await isAuthenticated(page);
    expect(authenticated).toBe(false);
  });

  test('should allow re-login after logout', async ({ page }) => {
    // Login first
    await login(page, TEST_USERS.main.username, TEST_USERS.main.password);
    
    // Verify user is logged in
    let authenticated = await isAuthenticated(page);
    expect(authenticated).toBe(true);
    
    // Logout
    await logout(page);
    
    // Verify user is logged out
    authenticated = await isAuthenticated(page);
    expect(authenticated).toBe(false);
    
    // Login again with same credentials
    await login(page, TEST_USERS.main.username, TEST_USERS.main.password);
    
    // Verify login successful
    authenticated = await isAuthenticated(page);
    expect(authenticated).toBe(true);
    
    // Verify user menu is visible
    await expect(page.locator('nav .dropdown-toggle')).toBeVisible();
  });

  test('should not show logout link for unauthenticated users', async ({ page }) => {
    // Navigate to site without logging in
    await page.goto('/');
    
    // Verify logout link is NOT visible
    await expect(page.locator('a:has-text("Log out")')).not.toBeVisible();
    
    // Verify login/register links are visible
    const loginLink = page.locator('a:has-text("Log in")');
    await expect(loginLink).toBeVisible();
    
    // Verify user menu dropdown is NOT visible
    await expect(page.locator('nav .dropdown-toggle')).not.toBeVisible();
    
    // Try to access logout URL directly (if it exists)
    // Note: django-allauth logout typically redirects unauthenticated users
    await page.goto('/accounts/logout/');
    
    // Should redirect to home page or login page
    await page.waitForURL('**/', { timeout: 3000 });
    
    // Verify user is still not authenticated
    const authenticated = await isAuthenticated(page);
    expect(authenticated).toBe(false);
  });
});



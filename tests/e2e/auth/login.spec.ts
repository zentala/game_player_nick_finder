import { test, expect } from '@playwright/test';
import { login, isAuthenticated, isNotAuthenticated, TEST_USERS } from '../../helpers/auth-helpers';

test.describe('Login Flow', () => {
  test('should display login form with all required elements', async ({ page }) => {
    await page.goto('/accounts/login/');
    
    // Verify login form is present
    await expect(page.locator('form.login')).toBeVisible();
    
    // Verify username/email field is present
    await expect(page.locator('#id_username')).toBeVisible();
    
    // Verify password field is present
    await expect(page.locator('#id_password')).toBeVisible();
    
    // Verify submit button is present
    await expect(page.locator('button[type="submit"]')).toBeVisible();
    
    // Verify "Forgot Password?" link is present
    const forgotPasswordLink = page.locator('a:has-text("Forgot Password?")');
    if (await forgotPasswordLink.count() > 0) {
      await expect(forgotPasswordLink).toBeVisible();
    }
  });

  test('should successfully login with valid credentials', async ({ page }) => {
    await page.goto('/accounts/login/');
    
    // Fill in valid credentials
    await page.fill('#id_username', TEST_USERS.main.username);
    await page.fill('#id_password', TEST_USERS.main.password);
    
    // Submit form
    await page.click('button[type="submit"]');
    
    // Verify redirect to home page
    await page.waitForURL('**/');
    await expect(page).toHaveURL(/\/$/);
    
    // Verify user menu appears in navbar
    await expect(page.locator('nav .dropdown-toggle')).toBeVisible();
    
    // Verify user is authenticated
    const authenticated = await isAuthenticated(page);
    expect(authenticated).toBe(true);
  });

  test('should fail login with invalid username', async ({ page }) => {
    await page.goto('/accounts/login/');
    
    // Fill in invalid username with valid password
    await page.fill('#id_username', 'nonexistentuser');
    await page.fill('#id_password', TEST_USERS.main.password);
    
    // Submit form
    await page.click('button[type="submit"]');
    
    // Verify error message displayed
    await expect(page.locator('.alert-danger, .errorlist, .invalid-feedback').filter({ hasText: /correct|invalid/i }).first()).toBeVisible();
    
    // Verify still on login page
    await expect(page).toHaveURL(/\/accounts\/login\/?/);
    
    // Verify user is NOT authenticated
    const authenticated = await isAuthenticated(page);
    expect(authenticated).toBe(false);
  });

  test('should fail login with invalid password', async ({ page }) => {
    await page.goto('/accounts/login/');
    
    // Fill in valid username with invalid password
    await page.fill('#id_username', TEST_USERS.main.username);
    await page.fill('#id_password', 'wrongpassword123');
    
    // Submit form
    await page.click('button[type="submit"]');
    
    // Verify error message displayed
    await expect(page.locator('.alert-danger, .errorlist, .invalid-feedback').filter({ hasText: /correct|invalid|incorrect|wrong/i }).first()).toBeVisible();
    
    // Verify still on login page
    await expect(page).toHaveURL(/\/accounts\/login\/?/);
    
    // Verify user is NOT authenticated
    const authenticated = await isAuthenticated(page);
    expect(authenticated).toBe(false);
  });

  test('should fail login with empty fields', async ({ page }) => {
    await page.goto('/accounts/login/');
    
    // Submit form without filling fields
    await page.click('button[type="submit"]');
    
    // Verify validation errors displayed
    // Django forms usually show validation errors or prevent submission
    const errorElement = page.locator('.alert-danger, .errorlist, .invalid-feedback, [class*="error"]');
    const currentUrl = page.url();
    
    // Either validation errors are shown or form prevents submission (stays on same page)
    if (await errorElement.count() > 0) {
      await expect(errorElement.first()).toBeVisible();
    } else {
      // If no visible errors, verify we're still on login page (form validation prevented submission)
      expect(currentUrl).toContain('/accounts/login');
    }
    
    // Verify user is NOT authenticated
    const authenticated = await isAuthenticated(page);
    expect(authenticated).toBe(false);
  });

  test('should redirect to originally requested page after login', async ({ page }) => {
    // Navigate to protected page (profile) without logging in
    await page.goto('/accounts/profile/');
    
    // Should redirect to login page
    await page.waitForURL(/\/accounts\/login\/?/);
    await expect(page).toHaveURL(/\/accounts\/login\/?/);
    
    // Login with valid credentials
    await page.fill('#id_username', TEST_USERS.main.username);
    await page.fill('#id_password', TEST_USERS.main.password);
    await page.click('button[type="submit"]');
    
    // Should redirect back to originally requested page (profile)
    await page.waitForURL(/\/accounts\/profile\/?/, { timeout: 5000 });
    await expect(page).toHaveURL(/\/accounts\/profile\/?/);
    
    // Verify user is authenticated
    const authenticated = await isAuthenticated(page);
    expect(authenticated).toBe(true);
  });

  test('should login with "Remember me" checkbox if available', async ({ page }) => {
    await page.goto('/accounts/login/');
    
    // Check if "Remember me" checkbox exists
    const rememberMeCheckbox = page.locator('#id_remember, input[name="remember"]');
    
    if (await rememberMeCheckbox.count() > 0) {
      // Fill in credentials
      await page.fill('#id_username', TEST_USERS.main.username);
      await page.fill('#id_password', TEST_USERS.main.password);
      
      // Check "Remember me" checkbox
      await rememberMeCheckbox.check();
      
      // Submit form
      await page.click('button[type="submit"]');
      
      // Verify login successful
      await page.waitForURL('**/');
      const authenticated = await isAuthenticated(page);
      expect(authenticated).toBe(true);
      
      // Note: Testing session persistence (closing and reopening browser)
      // would require more complex setup and is typically tested in integration tests
    } else {
      // If remember me checkbox doesn't exist, just verify normal login works
      await page.fill('#id_username', TEST_USERS.main.username);
      await page.fill('#id_password', TEST_USERS.main.password);
      await page.click('button[type="submit"]');
      
      await page.waitForURL('**/');
      const authenticated = await isAuthenticated(page);
      expect(authenticated).toBe(true);
    }
  });

  test('should redirect logged in user away from login page', async ({ page }) => {
    // Login first
    await login(page, TEST_USERS.main.username, TEST_USERS.main.password);
    
    // Verify user is authenticated
    const authenticated = await isAuthenticated(page);
    expect(authenticated).toBe(true);
    
    // Navigate to login page
    await page.goto('/accounts/login/');
    
    // Should redirect to home page (or appropriate page)
    await page.waitForURL('**/', { timeout: 3000 });
    
    // Verify we're not on login page anymore
    await expect(page).not.toHaveURL(/\/accounts\/login\/?/);
    
    // Verify user is still authenticated
    const stillAuthenticated = await isAuthenticated(page);
    expect(stillAuthenticated).toBe(true);
  });
});


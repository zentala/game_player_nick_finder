import { test, expect } from '@playwright/test';
import { login, isAuthenticated, isNotAuthenticated, TEST_USERS } from '../../helpers/auth-helpers';

test.describe('Login Flow', () => {
  test('should display login form with all required elements', async ({ page }) => {
    await page.goto('/accounts/login/');
    
    // Verify login form is present (use multiple fallback selectors for reliability)
    const loginForm = page.locator('form.login, form[action*="login"]').first();
    const formExists = await loginForm.count() > 0;
    if (formExists) {
      await expect(loginForm).toBeVisible();
    } else {
      // Fallback: if specific form selectors don't work, verify username input exists (form must be present)
      await expect(page.locator('input[name="username"]').first()).toBeVisible();
    }
    
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
    await page.waitForLoadState('networkidle');
    
    // Wait for form fields to be visible before filling
    await expect(page.locator('#id_username')).toBeVisible({ timeout: 5000 });
    await expect(page.locator('#id_password')).toBeVisible({ timeout: 5000 });
    
    // Fill in valid credentials
    await page.fill('#id_username', TEST_USERS.main.username);
    await page.fill('#id_password', TEST_USERS.main.password);
    
    // Verify fields are filled (debug check)
    const usernameValue = await page.locator('#id_username').inputValue();
    const passwordValue = await page.locator('#id_password').inputValue();
    if (usernameValue !== TEST_USERS.main.username || passwordValue.length === 0) {
      throw new Error(`Fields not filled correctly. Username: ${usernameValue}, Password length: ${passwordValue.length}`);
    }
    
    // Submit form
    await page.click('button[type="submit"]');
    
    // Verify redirect to home page
    await page.waitForURL('**/');
    await expect(page).toHaveURL(/\/$/);
    
    // Verify user menu appears in navbar
    await expect(page.locator('a.nav-link.dropdown-toggle').first()).toBeVisible();
    
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
    
    // Wait for page to load before filling
    await page.waitForLoadState('networkidle');
    
    // Wait for form fields to be visible
    await expect(page.locator('#id_username')).toBeVisible({ timeout: 5000 });
    await expect(page.locator('#id_password')).toBeVisible({ timeout: 5000 });
    
    // Login with valid credentials
    await page.fill('#id_username', TEST_USERS.main.username);
    await page.fill('#id_password', TEST_USERS.main.password);
    await page.click('button[type="submit"]');
    
    // Should redirect back to originally requested page (profile)
    await page.waitForURL(/\/accounts\/profile\/?/, { timeout: 15000 });
    await expect(page).toHaveURL(/\/accounts\/profile\/?/);
    
    // Verify user is authenticated
    const authenticated = await isAuthenticated(page);
    expect(authenticated).toBe(true);
  });

  test('should login with "Remember me" checkbox if available', async ({ page }) => {
    await page.goto('/accounts/login/');
    await page.waitForLoadState('networkidle');
    
    // Wait for form fields to be visible
    await expect(page.locator('#id_username')).toBeVisible({ timeout: 5000 });
    await expect(page.locator('#id_password')).toBeVisible({ timeout: 5000 });
    
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
    
    // Explicit wait before verification
    await page.waitForLoadState('networkidle');
    await page.waitForTimeout(500); // Additional wait for UI
    
    // Verify user is authenticated
    const authenticated = await isAuthenticated(page);
    expect(authenticated).toBe(true);
    
    // Wait for redirect after login
    await page.waitForURL('**/', { timeout: 5000 });
    
    // Navigate to login page - should redirect authenticated users
    await page.goto('/accounts/login/', { waitUntil: 'networkidle' });
    
    // Give Django time to process redirect
    await page.waitForTimeout(1000);
    
    // Check if we're still on login page (should not be for authenticated users)
    const currentUrl = page.url();
    if (currentUrl.includes('/accounts/login/')) {
      // If still on login, check if form is visible (should not be if redirect worked)
      const formVisible = await page.locator('form.login').isVisible().catch(() => false);
      if (formVisible) {
        // This is an error - logged in user should be redirected
        throw new Error('Logged in user should be redirected from login page, but form is still visible');
      }
    }
    
    // Verify we're not on login page anymore (should redirect to home)
    await expect(page).not.toHaveURL(/\/accounts\/login\/?/);
    
    // Verify user is still authenticated
    const stillAuthenticated = await isAuthenticated(page);
    expect(stillAuthenticated).toBe(true);
  });
});



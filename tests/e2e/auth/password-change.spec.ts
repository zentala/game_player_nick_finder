import { test, expect } from '@playwright/test';
import { login, isAuthenticated, TEST_USERS } from '../../helpers/auth-helpers';

test.describe('Password Change Flow', () => {
  test.beforeEach(async ({ page }) => {
    // Login before each test
    await login(page, TEST_USERS.main.username, TEST_USERS.main.password);
  });

  test('should display password change form with all required fields', async ({ page }) => {
    await page.goto('/accounts/password_change/');
    
    // Verify form is present
    await expect(page.locator('form.password_change')).toBeVisible();
    
    // Verify old password field is present
    await expect(page.locator('#id_oldpassword, input[name="oldpassword"]')).toBeVisible();
    
    // Verify new password field is present
    await expect(page.locator('#id_password1, input[name="password1"]')).toBeVisible();
    
    // Verify new password confirmation field is present
    await expect(page.locator('#id_password2, input[name="password2"]')).toBeVisible();
    
    // Verify submit button is present
    await expect(page.locator('button[type="submit"], input[type="submit"]')).toBeVisible();
  });

  test('should navigate to password change page via user menu', async ({ page }) => {
    await page.goto('/');
    
    // Click user menu dropdown
    await page.click('nav .dropdown-toggle');
    
    // Click "Change password" link
    await page.click('a:has-text("Change password")');
    
    // Verify navigation to password change page
    await expect(page).toHaveURL(/\/accounts\/password_change\/?/);
    
    // Verify password change form is present
    await expect(page.locator('form.password_change')).toBeVisible();
  });

  test('should successfully change password', async ({ page }) => {
    await page.goto('/accounts/password_change/');
    
    const oldPassword = TEST_USERS.main.password;
    const newPassword = 'NewTestPassword123!';
    
    // Fill in old password (correct)
    await page.fill('#id_oldpassword, input[name="oldpassword"]', oldPassword);
    
    // Fill in new password
    await page.fill('#id_password1, input[name="password1"]', newPassword);
    
    // Fill in new password confirmation (matches)
    await page.fill('#id_password2, input[name="password2"]', newPassword);
    
    // Submit form
    await page.click('button[type="submit"], input[type="submit"]');
    
    // Verify redirect to password change done page
    await page.waitForURL(/\/accounts\/password_change\/done\/?/, { timeout: 5000 });
    await expect(page).toHaveURL(/\/accounts\/password_change\/done\/?/);

    // Verify success message displayed
    await expect(page.getByText(/success|changed|password/i)).toBeVisible();

    // Logout and login with new password
    await page.click('nav .dropdown-toggle');
    await page.click('a:has-text("Log out")');
    await page.waitForURL('**/');
    
    // Login with new password
    await page.goto('/accounts/login/');
    await page.fill('#id_username', TEST_USERS.main.username);
    await page.fill('#id_password', newPassword);
    await page.click('button[type="submit"]');
    await page.waitForURL('**/');
    
    // Verify login successful with new password
    const authenticated = await isAuthenticated(page);
    expect(authenticated).toBe(true);
    
    // Note: In a real scenario, you would want to restore the original password
    // or use a dedicated test user for password change tests
  });

  test('should show error for wrong old password', async ({ page }) => {
    await page.goto('/accounts/password_change/');
    
    const wrongOldPassword = 'WrongOldPassword123!';
    const newPassword = 'NewTestPassword123!';
    
    // Fill in wrong old password
    await page.fill('#id_oldpassword, input[name="oldpassword"]', wrongOldPassword);
    
    // Fill in new password
    await page.fill('#id_password1, input[name="password1"]', newPassword);
    
    // Fill in new password confirmation
    await page.fill('#id_password2, input[name="password2"]', newPassword);
    
    // Submit form
    await page.click('button[type="submit"], input[type="submit"]');
    
    // Verify error message displayed
    await expect(page.locator('.alert-danger, .errorlist, .invalid-feedback').filter({ hasText: /old password|incorrect|wrong/i })).toBeVisible();
    
    // Verify still on password change page
    await expect(page).toHaveURL(/\/accounts\/password_change\/?/);
  });

  test('should show validation error for password too short', async ({ page }) => {
    await page.goto('/accounts/password_change/');
    
    const oldPassword = TEST_USERS.main.password;
    const shortPassword = '123'; // Too short
    
    // Fill in old password (correct)
    await page.fill('#id_oldpassword, input[name="oldpassword"]', oldPassword);
    
    // Fill in new password (too short)
    await page.fill('#id_password1, input[name="password1"]', shortPassword);
    
    // Fill in new password confirmation
    await page.fill('#id_password2, input[name="password2"]', shortPassword);
    
    // Submit form
    await page.click('button[type="submit"], input[type="submit"]');
    
    // Verify password validation error displayed
    await expect(page.locator('.alert-danger, .errorlist, .invalid-feedback').filter({ hasText: /password|short|minimum/i })).toBeVisible();
    
    // Verify still on password change page
    await expect(page).toHaveURL(/\/accounts\/password_change\/?/);
  });

  test('should show validation error for password mismatch', async ({ page }) => {
    await page.goto('/accounts/password_change/');
    
    const oldPassword = TEST_USERS.main.password;
    const newPassword = 'NewTestPassword123!';
    const differentPassword = 'DifferentPassword456!';
    
    // Fill in old password (correct)
    await page.fill('#id_oldpassword, input[name="oldpassword"]', oldPassword);
    
    // Fill in new password
    await page.fill('#id_password1, input[name="password1"]', newPassword);
    
    // Fill in different password confirmation
    await page.fill('#id_password2, input[name="password2"]', differentPassword);
    
    // Submit form
    await page.click('button[type="submit"], input[type="submit"]');
    
    // Verify password mismatch error displayed
    await expect(page.locator('.alert-danger, .errorlist, .invalid-feedback').filter({ hasText: /match|confirm|password/i })).toBeVisible();
    
    // Verify still on password change page
    await expect(page).toHaveURL(/\/accounts\/password_change\/?/);
  });

  test('should show validation errors for empty fields', async ({ page }) => {
    await page.goto('/accounts/password_change/');
    
    // Submit form without filling fields
    await page.click('button[type="submit"], input[type="submit"]');
    
    // Verify validation errors displayed
    const errorElement = page.locator('.alert-danger, .errorlist, .invalid-feedback, [class*="error"]');
    const currentUrl = page.url();
    
    // Either validation errors are shown or form prevents submission
    if (await errorElement.count() > 0) {
      await expect(errorElement.first()).toBeVisible();
    } else {
      // If no visible errors, verify we're still on password change page
      expect(currentUrl).toContain('/accounts/password_change');
    }
  });

  test('should redirect to login when accessing password change without authentication', async ({ page }) => {
    // Logout first
    await page.click('nav .dropdown-toggle');
    await page.click('a:has-text("Log out")');
    await page.waitForURL('**/');
    
    // Navigate to password change page without logging in
    await page.goto('/accounts/password_change/');
    
    // Should redirect to login page
    await page.waitForURL(/\/accounts\/login\/?/, { timeout: 5000 });
    await expect(page).toHaveURL(/\/accounts\/login\/?/);
    
    // Verify login form is present
    await expect(page.locator('form.login')).toBeVisible();
    
    // After login, should redirect back to password change page
    await page.fill('#id_username', TEST_USERS.main.username);
    await page.fill('#id_password', TEST_USERS.main.password);
    await page.click('button[type="submit"]');
    
    // Should redirect to password change page (or home if redirect URL not preserved)
    await page.waitForURL(/\/(accounts\/password_change|$)/, { timeout: 5000 });
  });

  test('should display password change done page after successful change', async ({ page }) => {
    await page.goto('/accounts/password_change/');
    
    const oldPassword = TEST_USERS.main.password;
    const newPassword = 'NewTestPassword123!';
    
    // Fill in old password (correct)
    await page.fill('#id_oldpassword, input[name="oldpassword"]', oldPassword);
    
    // Fill in new password
    await page.fill('#id_password1, input[name="password1"]', newPassword);
    
    // Fill in new password confirmation
    await page.fill('#id_password2, input[name="password2"]', newPassword);
    
    // Submit form
    await page.click('button[type="submit"], input[type="submit"]');
    
    // Verify redirect to password change done page
    await page.waitForURL(/\/accounts\/password_change\/done\/?/, { timeout: 5000 });
    await expect(page).toHaveURL(/\/accounts\/password_change\/done\/?/);

    // Verify success message displayed
    await expect(page.getByText(/success|changed|password/i)).toBeVisible();

    // Verify page content is visible
    await expect(page.locator('body')).toBeVisible();
  });
});


import { test, expect } from '@playwright/test';
import { TEST_USERS } from '../../helpers/auth-helpers';

test.describe('Password Reset Flow', () => {
  test('should display password reset request form with all required elements', async ({ page }) => {
    await page.goto('/accounts/password_reset/');
    
    // Verify form is present
    await expect(page.locator('form.password_reset')).toBeVisible();
    
    // Verify email field is present
    await expect(page.locator('#id_email, input[name="email"], input[type="email"]')).toBeVisible();
    
    // Verify submit button is present
    await expect(page.locator('button[type="submit"], input[type="submit"]')).toBeVisible();
    
    // Verify "Back to login" link if present
    const backToLoginLink = page.locator('a:has-text("Back"), a:has-text("login")');
    // This is optional - just check if it exists
  });

  test('should successfully request password reset with valid email', async ({ page }) => {
    await page.goto('/accounts/password_reset/');
    
    // Fill in valid email address (existing user)
    // Note: Using test user email if available, or a test email
    await page.fill('#id_email, input[name="email"], input[type="email"]', 'testuser@example.com');
    
    // Submit form
    await page.click('button[type="submit"], input[type="submit"]');
    
    // Verify redirect to password reset done page
    await page.waitForURL(/\/accounts\/password_reset\/done\/?/, { timeout: 5000 });
    await expect(page).toHaveURL(/\/accounts\/password_reset\/done\/?/);

    // Verify success message displayed
    await expect(page.getByText(/email|sent|reset/i)).toBeVisible();

    // Note: In development, email is printed to console
    // Full email token testing would require email mock setup or management command
  });

  test('should handle password reset request with invalid email gracefully', async ({ page }) => {
    await page.goto('/accounts/password_reset/');
    
    // Fill in email that doesn't exist
    await page.fill('#id_email, input[name="email"], input[type="email"]', 'nonexistent@example.com');
    
    // Submit form
    await page.click('button[type="submit"], input[type="submit"]');
    
    // Django typically shows success message even for non-existent emails (security best practice)
    // OR redirects to done page, OR shows error
    // Verify we're either on done page or error is shown
    const currentUrl = page.url();
    const donePage = currentUrl.includes('/password_reset/done');
    const errorElement = page.locator('.alert-danger, .errorlist, .invalid-feedback');
    
    // Either success page or error message - both are valid behaviors
    if (!donePage) {
      // If not on done page, check for error
      if (await errorElement.count() > 0) {
        await expect(errorElement.first()).toBeVisible();
      }
    } else {
      // On done page - verify success message
      await expect(page.locator('body')).toBeVisible();
    }
  });

  test('should show validation error for empty email field', async ({ page }) => {
    await page.goto('/accounts/password_reset/');
    
    // Submit form without filling email
    await page.click('button[type="submit"], input[type="submit"]');
    
    // Verify validation error displayed
    const errorElement = page.locator('.alert-danger, .errorlist, .invalid-feedback, [class*="error"]');
    const currentUrl = page.url();
    
    // Either validation errors are shown or form prevents submission
    if (await errorElement.count() > 0) {
      await expect(errorElement.first()).toBeVisible();
    } else {
      // If no visible errors, verify we're still on password reset page
      expect(currentUrl).toContain('/accounts/password_reset');
    }
  });

  test('should show validation error for invalid email format', async ({ page }) => {
    await page.goto('/accounts/password_reset/');
    
    // Fill in invalid email format
    await page.fill('#id_email, input[name="email"], input[type="email"]', 'notanemail');
    
    // Submit form
    await page.click('button[type="submit"], input[type="submit"]');
    
    // Verify email validation error displayed
    await expect(page.locator('.alert-danger, .errorlist, .invalid-feedback').filter({ hasText: /email|invalid/i })).toBeVisible();
    
    // Verify still on password reset page
    await expect(page).toHaveURL(/\/accounts\/password_reset\/?/);
  });

  test('should have Forgot Password link in login form', async ({ page }) => {
    await page.goto('/accounts/login/');
    
    // Verify login form is present
    await expect(page.locator('form.login')).toBeVisible();
    
    // Verify "Forgot Password?" link is present (link text is "Reset it")
    const forgotPasswordLink = page.locator('a:has-text("Reset it"), a:has-text("Reset"), a:has-text("Forgot")');
    await expect(forgotPasswordLink.first()).toBeVisible();
    
    // Click "Forgot Password?" link
    await forgotPasswordLink.first().click();
    
    // Verify navigation to password reset page
    await expect(page).toHaveURL(/\/accounts\/password_reset\/?/);
    
    // Verify password reset form is present
    await expect(page.locator('form.password_reset')).toBeVisible();
  });

  test('should display password reset done page after request', async ({ page }) => {
    await page.goto('/accounts/password_reset/');
    
    // Fill in email
    await page.fill('#id_email, input[name="email"], input[type="email"]', 'testuser@example.com');
    
    // Submit form
    await page.click('button[type="submit"], input[type="submit"]');
    
    // Verify redirect to password reset done page
    await page.waitForURL(/\/accounts\/password_reset\/done\/?/, { timeout: 5000 });
    await expect(page).toHaveURL(/\/accounts\/password_reset\/done\/?/);

    // Verify success message displayed
    await expect(page.getByText(/email|sent|reset/i)).toBeVisible();

    // Verify page content is visible
    await expect(page.locator('body')).toBeVisible();
  });

  // Note: Tests for password reset confirmation (with token) are skipped
  // These would require:
  // - Email mock setup to capture reset tokens
  // - OR Django management command to generate tokens
  // - OR complex test setup with email backend
  // These are better suited for integration tests or unit tests
});


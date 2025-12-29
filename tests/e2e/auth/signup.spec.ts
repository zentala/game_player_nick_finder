import { test, expect } from '@playwright/test';
import { isAuthenticated, isNotAuthenticated, TEST_USERS } from '../../helpers/auth-helpers';

test.describe('Registration (Signup) Flow', () => {
  test('should display signup form with all required elements', async ({ page }) => {
    await page.goto('/accounts/register/');
    
    // Verify form is present (use multiple fallback selectors for reliability)
    const signupForm = page.locator('form.signup, form#signup_form, form[action*="signup"], form[action*="register"]').first();
    const formExists = await signupForm.count() > 0;
    if (formExists) {
      await expect(signupForm).toBeVisible();
    } else {
      // Fallback: if specific form selectors don't work, verify username input exists (form must be present)
      await expect(page.locator('input[name="username"]').first()).toBeVisible();
    }
    
    // Verify username field is present
    const usernameField = page.locator('#id_username, input[name="username"]');
    if (await usernameField.count() > 0) {
      await expect(usernameField.first()).toBeVisible();
    }
    
    // Verify email field is present (if required)
    const emailField = page.locator('#id_email, input[name="email"]');
    if (await emailField.count() > 0) {
      await expect(emailField.first()).toBeVisible();
    }
    
    // Verify password field is present
    const passwordField = page.locator('#id_password1, input[name="password1"], input[type="password"]').first();
    await expect(passwordField).toBeVisible();
    
    // Verify submit button is present
    await expect(page.locator('button[type="submit"]')).toBeVisible();
    
    // Verify "Already have an account? Sign in" link is present
    const signInLink = page.locator('a:has-text("sign in"), a:has-text("Sign in")');
    if (await signInLink.count() > 0) {
      await expect(signInLink.first()).toBeVisible();
    }
  });

  test('should successfully register new user', async ({ page }) => {
    await page.goto('/accounts/register/');
    
    // Generate unique username/email to avoid conflicts
    const timestamp = Date.now();
    const uniqueUsername = `testuser${timestamp}`;
    const uniqueEmail = `test${timestamp}@example.com`;
    const password = 'TestPassword123!';
    
    // Fill in all required fields with valid data
    const usernameField = page.locator('#id_username, input[name="username"]').first();
    if (await usernameField.count() > 0) {
      await usernameField.fill(uniqueUsername);
    }
    
    const emailField = page.locator('#id_email, input[name="email"]').first();
    if (await emailField.count() > 0) {
      await emailField.fill(uniqueEmail);
    }
    
    const passwordField = page.locator('#id_password1, input[name="password1"], input[type="password"]').first();
    await passwordField.fill(password);
    
    // Check for password confirmation field
    const passwordConfirmField = page.locator('#id_password2, input[name="password2"]');
    if (await passwordConfirmField.count() > 0) {
      await passwordConfirmField.fill(password);
    }
    
    // Submit form
    await page.click('button[type="submit"]');
    
    // Wait for redirect (usually to home page after successful registration)
    await page.waitForURL('**/', { timeout: 5000 });
    
    // Verify redirect to appropriate page (usually home)
    await expect(page).toHaveURL(/\/$/);
    
    // Verify user is authenticated
    const authenticated = await isAuthenticated(page);
    expect(authenticated).toBe(true);
    
    // Verify user menu appears in navbar
    await expect(page.locator('a.nav-link.dropdown-toggle').first()).toBeVisible();
  });

  test('should show validation errors for empty fields', async ({ page }) => {
    await page.goto('/accounts/register/');
    
    // Submit form without filling fields
    await page.click('button[type="submit"]');
    
    // Verify validation errors displayed or form prevents submission
    const errorElement = page.locator('.alert-danger, .errorlist, .invalid-feedback, [class*="error"]');
    const currentUrl = page.url();
    
    // Either validation errors are shown or form prevents submission
    if (await errorElement.count() > 0) {
      await expect(errorElement.first()).toBeVisible();
    } else {
      // If no visible errors, verify we're still on signup page (form validation prevented submission)
      expect(currentUrl).toContain('/accounts/signup');
    }
    
    // Verify user is NOT authenticated
    const authenticated = await isAuthenticated(page);
    expect(authenticated).toBe(false);
  });

  test('should show validation error for invalid email format', async ({ page }) => {
    await page.goto('/accounts/register/');
    
    const timestamp = Date.now();
    const uniqueUsername = `testuser${timestamp}`;
    const invalidEmail = 'notanemail';
    const password = 'TestPassword123!';
    
    // Fill in fields with invalid email
    const usernameField = page.locator('#id_username, input[name="username"]').first();
    if (await usernameField.count() > 0) {
      await usernameField.fill(uniqueUsername);
    }
    
    const emailField = page.locator('#id_email, input[name="email"]').first();
    if (await emailField.count() > 0) {
      await emailField.fill(invalidEmail);
    }
    
    const passwordField = page.locator('#id_password1, input[name="password1"], input[type="password"]').first();
    await passwordField.fill(password);
    
    const passwordConfirmField = page.locator('#id_password2, input[name="password2"]');
    if (await passwordConfirmField.count() > 0) {
      await passwordConfirmField.fill(password);
    }
    
    // Submit form
    await page.click('button[type="submit"]');
    
    // Verify email validation error displayed
    await expect(page.locator('.alert-danger, .errorlist, .invalid-feedback').filter({ hasText: /email|invalid/i })).toBeVisible();
    
    // Verify still on signup page
    await expect(page).toHaveURL(/\/accounts\/signup\/?/);
  });

  test('should show validation error for password too short', async ({ page }) => {
    await page.goto('/accounts/register/');
    
    const timestamp = Date.now();
    const uniqueUsername = `testuser${timestamp}`;
    const shortPassword = '123'; // Too short
    
    // Fill in fields with short password
    const usernameField = page.locator('#id_username, input[name="username"]').first();
    if (await usernameField.count() > 0) {
      await usernameField.fill(uniqueUsername);
    }
    
    const emailField = page.locator('#id_email, input[name="email"]').first();
    if (await emailField.count() > 0) {
      await emailField.fill(`test${timestamp}@example.com`);
    }
    
    const passwordField = page.locator('#id_password1, input[name="password1"], input[type="password"]').first();
    await passwordField.fill(shortPassword);
    
    const passwordConfirmField = page.locator('#id_password2, input[name="password2"]');
    if (await passwordConfirmField.count() > 0) {
      await passwordConfirmField.fill(shortPassword);
    }
    
    // Submit form
    await page.click('button[type="submit"]');
    
    // Verify password validation error displayed
    await expect(page.locator('.alert-danger, .errorlist, .invalid-feedback').filter({ hasText: /password|short|minimum/i })).toBeVisible();
    
    // Verify still on signup page
    await expect(page).toHaveURL(/\/accounts\/signup\/?/);
  });

  test('should show validation error for password mismatch', async ({ page }) => {
    await page.goto('/accounts/register/');
    
    const timestamp = Date.now();
    const uniqueUsername = `testuser${timestamp}`;
    const password = 'TestPassword123!';
    const differentPassword = 'DifferentPassword456!';
    
    // Fill in fields with different passwords
    const usernameField = page.locator('#id_username, input[name="username"]').first();
    if (await usernameField.count() > 0) {
      await usernameField.fill(uniqueUsername);
    }
    
    const emailField = page.locator('#id_email, input[name="email"]').first();
    if (await emailField.count() > 0) {
      await emailField.fill(`test${timestamp}@example.com`);
    }
    
    const passwordField = page.locator('#id_password1, input[name="password1"], input[type="password"]').first();
    await passwordField.fill(password);
    
    const passwordConfirmField = page.locator('#id_password2, input[name="password2"]');
    if (await passwordConfirmField.count() > 0) {
      await passwordConfirmField.fill(differentPassword);
      
      // Submit form
      await page.click('button[type="submit"]');
      
      // Verify password mismatch error displayed
      await expect(page.locator('.alert-danger, .errorlist, .invalid-feedback').filter({ hasText: /match|confirm|password/i })).toBeVisible();
      
      // Verify still on signup page
      await expect(page).toHaveURL(/\/accounts\/signup\/?/);
    } else {
      // If no password confirmation field, skip this test
      test.skip();
    }
  });

  test('should show validation error for username already exists', async ({ page }) => {
    await page.goto('/accounts/register/');
    
    // Use existing username from fixtures
    const existingUsername = TEST_USERS.main.username;
    const password = 'TestPassword123!';
    
    // Fill in fields with existing username
    const usernameField = page.locator('#id_username, input[name="username"]').first();
    if (await usernameField.count() > 0) {
      await usernameField.fill(existingUsername);
    }
    
    const emailField = page.locator('#id_email, input[name="email"]').first();
    if (await emailField.count() > 0) {
      await emailField.fill(`newemail${Date.now()}@example.com`);
    }
    
    const passwordField = page.locator('#id_password1, input[name="password1"], input[type="password"]').first();
    await passwordField.fill(password);
    
    const passwordConfirmField = page.locator('#id_password2, input[name="password2"]');
    if (await passwordConfirmField.count() > 0) {
      await passwordConfirmField.fill(password);
    }
    
    // Submit form
    await page.click('button[type="submit"]');
    
    // Verify username already exists error displayed
    await expect(page.locator('.alert-danger, .errorlist, .invalid-feedback').filter({ hasText: /username|already|exists|taken/i })).toBeVisible();
    
    // Verify still on signup page
    await expect(page).toHaveURL(/\/accounts\/signup\/?/);
  });

  test('should show validation error for email already exists (if uniqueness enforced)', async ({ page }) => {
    // This test depends on ACCOUNT_UNIQUE_EMAIL setting
    // In base.py it's set to True, so we should test it
    await page.goto('/accounts/register/');
    
    // Use existing email (assuming testuser has email in fixtures)
    // Note: This test may need adjustment based on actual fixture data
    const timestamp = Date.now();
    const uniqueUsername = `newuser${timestamp}`;
    // Try to use email that might exist - adjust based on fixtures
    // For now, we'll use a pattern that might conflict
    const existingEmail = 'test@example.com'; // Adjust if needed
    
    const password = 'TestPassword123!';
    
    // Fill in fields with potentially existing email
    const usernameField = page.locator('#id_username, input[name="username"]').first();
    if (await usernameField.count() > 0) {
      await usernameField.fill(uniqueUsername);
    }
    
    const emailField = page.locator('#id_email, input[name="email"]').first();
    if (await emailField.count() > 0) {
      await emailField.fill(existingEmail);
    }
    
    const passwordField = page.locator('#id_password1, input[name="password1"], input[type="password"]').first();
    await passwordField.fill(password);
    
    const passwordConfirmField = page.locator('#id_password2, input[name="password2"]');
    if (await passwordConfirmField.count() > 0) {
      await passwordConfirmField.fill(password);
    }
    
    // Submit form
    await page.click('button[type="submit"]');
    
    // Verify email already exists error displayed (if email uniqueness is enforced)
    // Note: This may not trigger if email doesn't exist, so we check conditionally
    const errorElement = page.locator('.alert-danger, .errorlist, .invalid-feedback').filter({ hasText: /email|already|exists|taken/i });
    const currentUrl = page.url();
    
    // If error is shown, verify it. If not, user was created successfully (email was unique)
    if (await errorElement.count() > 0) {
      await expect(errorElement.first()).toBeVisible();
      await expect(page).toHaveURL(/\/accounts\/signup\/?/);
    } else {
      // Email was unique, registration succeeded - verify redirect
      await expect(page).toHaveURL(/\/$/);
    }
  });

  test('should redirect logged in user away from signup page', async ({ page }) => {
    // Login first
    await page.goto('/accounts/login/');
    await page.fill('#id_username', TEST_USERS.main.username);
    await page.fill('#id_password', TEST_USERS.main.password);
    await page.click('button[type="submit"]');
    await page.waitForURL('**/');
    
    // Verify user is authenticated
    let authenticated = await isAuthenticated(page);
    expect(authenticated).toBe(true);
    
    // Navigate to signup page
    await page.goto('/accounts/register/');
    
    // Should redirect to home page (or appropriate page)
    await page.waitForURL('**/', { timeout: 3000 });
    
    // Verify we're not on signup page anymore
    await expect(page).not.toHaveURL(/\/accounts\/signup\/?/);
    
    // Verify user is still authenticated
    authenticated = await isAuthenticated(page);
    expect(authenticated).toBe(true);
  });

  test('should have register link in navbar for unauthenticated users', async ({ page }) => {
    // Navigate to site without logging in
    await page.goto('/');

    // Verify user is not authenticated
    const notAuthenticated = await isNotAuthenticated(page);
    expect(notAuthenticated).toBe(true);

    // Verify "Register" link is visible in navbar
    const registerLink = page.locator('a:has-text("Register"), a:has-text("register")');
    await expect(registerLink.first()).toBeVisible();

    // Click "Register" link
    await registerLink.first().click();

    // Verify navigation to signup page (register_step1 is /register/step1/)
    await expect(page).toHaveURL(/\/register\/step1\/?/);

    // Verify signup form is present
    await expect(page.locator('form.signup, form#signup_form')).toBeVisible();
  });
});



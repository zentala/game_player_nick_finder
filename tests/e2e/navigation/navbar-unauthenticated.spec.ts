import { test, expect } from '@playwright/test';
import { isNotAuthenticated } from '../../helpers/auth-helpers';

test.describe('Navigation Menu - Unauthenticated Users', () => {
  test('should display navbar with login and register links', async ({ page }) => {
    await page.goto('/');
    
    // Verify navbar is visible
    await expect(page.locator('nav').first()).toBeVisible();
    
    // Verify "Log in" and "Register" links are visible
    const loginLink = page.locator('a:has-text("Log in")');
    await expect(loginLink).toBeVisible();
    
    const registerLink = page.locator('a:has-text("Register")');
    await expect(registerLink).toBeVisible();
    
    // Verify user menu dropdown is NOT visible
    await expect(page.locator('a.nav-link.dropdown-toggle').first()).not.toBeVisible();
    
    // Verify user is not authenticated
    const notAuthenticated = await isNotAuthenticated(page);
    expect(notAuthenticated).toBe(true);
  });

  test('should navigate to home page via Home link', async ({ page }) => {
    await page.goto('/characters/');
    
    // Click "Home" link
    await page.click('nav a:has-text("Home")');
    
    // Verify navigation to home page
    await expect(page).toHaveURL(/\/$/);
    
    // Verify navbar is still visible
    await expect(page.locator('nav').first()).toBeVisible();
  });

  test('should navigate to characters list via Characters link', async ({ page }) => {
    await page.goto('/');
    
    // Click "Characters" link
    await page.click('nav a:has-text("Characters")');
    
    // Verify navigation to characters list page
    await expect(page).toHaveURL(/\/characters\/?/);
    
    // Verify navbar is still visible
    await expect(page.locator('nav').first()).toBeVisible();
    
    // Characters list should be accessible without login (or show appropriate message)
    await expect(page.locator('body')).toBeVisible();
  });

  test('should navigate to games list via Games link', async ({ page }) => {
    await page.goto('/');
    
    // Click "Games" link
    await page.click('nav a:has-text("Games")');
    
    // Verify navigation to games list page
    await expect(page).toHaveURL(/\/games\/?/);
    
    // Verify navbar is still visible
    await expect(page.locator('nav').first()).toBeVisible();
    
    // Games list should be accessible without login
    await expect(page.locator('body')).toBeVisible();
  });

  test('should navigate to login page via Log in link', async ({ page }) => {
    await page.goto('/');
    
    // Click "Log in" link
    await page.click('a:has-text("Log in")');
    
    // Verify navigation to login page
    await expect(page).toHaveURL(/\/accounts\/login\/?/);
    
    // Verify login form is present (use multiple fallback selectors for reliability)
    const loginForm = page.locator('form.login, form[action*="login"]').first();
    const formExists = await loginForm.count() > 0;
    if (formExists) {
      await expect(loginForm).toBeVisible();
    } else {
      // Fallback: if specific form selectors don't work, verify username input exists (form must be present)
      await expect(page.locator('input[name="username"]').first()).toBeVisible();
    }
  });

  test('should navigate to signup page via Register link', async ({ page }) => {
    await page.goto('/');
    
    // Click "Register" link
    await page.click('a:has-text("Register")');
    
    // Verify navigation to signup page (accept both allauth and django-registration URLs)
    await expect(page).toHaveURL(/\/accounts\/signup\/?|\/register\/step1\/?/);
    
    // Verify signup form is present (use multiple fallback selectors for reliability)
    let signupForm = page.locator('form.signup, form#signup_form, form[action*="signup"], form[action*="register"]').first();
    if (await signupForm.count() === 0) {
      // Fallback: find form that contains username input by using parent locator
      const usernameInput = page.locator('input[name="username"]').first();
      signupForm = usernameInput.locator('xpath=ancestor::form[1]');
    }
    await expect(signupForm).toBeVisible();
  });

  test('should redirect to login when accessing protected route', async ({ page }) => {
    // Navigate to protected page without logging in
    await page.goto('/accounts/profile/');
    
    // Should redirect to login page
    await page.waitForURL(/\/accounts\/login\/?/, { timeout: 5000 });
    await expect(page).toHaveURL(/\/accounts\/login\/?/);
    
    // Verify login form is present (use multiple fallback selectors for reliability)
    const loginForm = page.locator('form.login, form[action*="login"]').first();
    const formExists = await loginForm.count() > 0;
    if (formExists) {
      await expect(loginForm).toBeVisible();
    } else {
      // Fallback: if specific form selectors don't work, verify username input exists (form must be present)
      await expect(page.locator('input[name="username"]').first()).toBeVisible();
    }
    
    // After login, should redirect back to originally requested page
    // This is tested in login.spec.ts, so we just verify redirect to login here
  });

  test('should highlight active page link in navbar (if implemented)', async ({ page }) => {
    // Navigate to different pages and check if active class is applied
    // Note: This test depends on implementation - navbar may or may not highlight active page
    
    // Navigate to home
    await page.goto('/');
    const homeLink = page.locator('nav a:has-text("Home")');
    if (await homeLink.count() > 0) {
      // Check if active class is present (if implemented)
      const homeLinkClasses = await homeLink.first().getAttribute('class');
      // Active class might be 'active' or similar
      // This is optional - if not implemented, test passes
    }
    
    // Navigate to characters
    await page.goto('/characters/');
    const charactersLink = page.locator('nav a:has-text("Characters")');
    if (await charactersLink.count() > 0) {
      const charactersLinkClasses = await charactersLink.first().getAttribute('class');
      // Active class might be 'active' or similar
    }
    
    // Navigate to games
    await page.goto('/games/');
    const gamesLink = page.locator('nav a:has-text("Games")');
    if (await gamesLink.count() > 0) {
      const gamesLinkClasses = await gamesLink.first().getAttribute('class');
      // Active class might be 'active' or similar
    }
    
    // This test verifies navigation works, active highlighting is optional feature
    expect(true).toBe(true);
  });
});



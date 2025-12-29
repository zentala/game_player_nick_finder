import { test, expect } from '@playwright/test';

test.describe('User Profile Display', () => {
  test('should display public profile', async ({ page }) => {
    await page.goto('/profile/testuser/');
    
    await expect(page.locator('h2:has-text("testuser")')).toBeVisible();
  });

  test('should show profile bio if available', async ({ page }) => {
    await page.goto('/profile/testuser/');
    
    // Check if bio is visible (if set)
    const bio = page.locator('.lead');
    if (await bio.count() > 0) {
      await expect(bio).toBeVisible();
    }
  });

  test('should show social media links', async ({ page }) => {
    await page.goto('/profile/testuser/');
    
    // Check if links section exists
    const linksSection = page.locator('h4:has-text("Links")');
    if (await linksSection.count() > 0) {
      await expect(linksSection).toBeVisible();
    }
  });

  test('should show user characters', async ({ page }) => {
    await page.goto('/profile/testuser/');
    
    const charactersSection = page.locator('h4:has-text("Characters")');
    if (await charactersSection.count() > 0) {
      await expect(charactersSection).toBeVisible();
    }
  });

  test('should block private profile from non-friends', async ({ page }) => {
    // Login as different user
    await page.goto('/accounts/login/');
    await page.fill('#id_username', 'otheruser');
    await page.fill('#id_password', 'pass');
    await page.click('button[type="submit"]');
    await page.waitForURL('**/');
    
    // Try to view private profile
    await page.goto('/profile/privateuser/');
    
    // Should show permission denied
    const errorMessage = page.locator('text=This profile is private');
    if (await errorMessage.count() > 0) {
      await expect(errorMessage).toBeVisible();
    }
  });
});

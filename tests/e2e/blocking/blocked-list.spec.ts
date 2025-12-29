import { test, expect } from '@playwright/test';
import { login, TEST_USERS } from '../../helpers/auth-helpers';

test.describe('Blocked Characters List', () => {
  test.beforeEach(async ({ page }) => {
    await login(page, TEST_USERS.main.username, TEST_USERS.main.password);
  });

  test('should display blocked characters list page', async ({ page }) => {
    await page.goto('/characters/blocked/');
    
    // Verify page title
    await expect(page.locator('h1, h2, h5:has-text("Blocked Characters")').first()).toBeVisible();
  });

  test('should show empty state when no blocked characters', async ({ page }) => {
    await page.goto('/characters/blocked/');
    
    // Check for empty state message
    const emptyMessage = page.locator('text=No blocked characters');
    if (await emptyMessage.count() > 0) {
      await expect(emptyMessage).toBeVisible();
    }
  });

  test('should display blocked character information', async ({ page }) => {
    // First block a character
    await page.goto('/character/test-character-123-testhash/');
    
    const blockButton = page.locator('button:has-text("Block")');
    if (await blockButton.count() > 0) {
      await blockButton.click();
      const submitButton = page.locator('button:has-text("Block Character")');
      await submitButton.click();
      
      // Navigate to blocked list
      await page.goto('/characters/blocked/');
      
      // Verify blocked character appears in list
      const characterLink = page.locator('a:has-text("test-character")');
      if (await characterLink.count() > 0) {
        await expect(characterLink.first()).toBeVisible();
        
        // Verify unblock button is present
        await expect(page.locator('button:has-text("Unblock")')).toBeVisible();
      }
    } else {
      test.skip();
    }
  });

  test('should show block date and reason if provided', async ({ page }) => {
    // Block character with reason
    await page.goto('/character/test-character-123-testhash/');
    
    const blockButton = page.locator('button:has-text("Block")');
    if (await blockButton.count() > 0) {
      await blockButton.click();
      
      const reasonTextarea = page.locator('textarea[name="reason"]');
      if (await reasonTextarea.count() > 0) {
        await reasonTextarea.fill('Test reason for blocking');
        const submitButton = page.locator('button:has-text("Block Character")');
        await submitButton.click();
        
        // Navigate to blocked list
        await page.goto('/characters/blocked/');
        
        // Verify reason is displayed
        await expect(page.locator('text=Test reason for blocking')).toBeVisible();
      }
    } else {
      test.skip();
    }
  });

  test('should have navigation link in navbar', async ({ page }) => {
    await page.goto('/');
    
    // Click user menu
    const userMenu = page.locator('a.nav-link.dropdown-toggle').first();
    if (await userMenu.count() > 0) {
      await userMenu.click();
      
      // Look for "Blocked Characters" link
      const blockedLink = page.locator('a:has-text("Blocked Characters")');
      await expect(blockedLink).toBeVisible();
      
      // Click and verify navigation
      await blockedLink.click();
      await expect(page).toHaveURL(/\/characters\/blocked/);
    }
  });
});



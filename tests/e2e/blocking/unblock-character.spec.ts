import { test, expect } from '@playwright/test';
import { login, TEST_USERS } from '../../helpers/auth-helpers';

test.describe('Unblock Character', () => {
  test.beforeEach(async ({ page }) => {
    await login(page, TEST_USERS.main.username, TEST_USERS.main.password);
  });

  test('should show unblock button when character is blocked', async ({ page }) => {
    // First, block a character (if not already blocked)
    await page.goto('/character/test-character-123-testhash/');
    
    // Check if already blocked (unblock button visible)
    const unblockButton = page.locator('button:has-text("Unblock")');
    
    if (await unblockButton.count() > 0) {
      // Already blocked, test unblock
      await unblockButton.click();
      
      // Verify success message
      await expect(page.locator('text=unblocked successfully')).toBeVisible();
      
      // Verify button changed back to "Block"
      await expect(page.locator('button:has-text("Block")')).toBeVisible();
    } else {
      // Not blocked yet, block first then unblock
      const blockButton = page.locator('button:has-text("Block")');
      if (await blockButton.count() > 0) {
        await blockButton.click();
        const submitButton = page.locator('button:has-text("Block Character")');
        await submitButton.click();
        
        // Wait for block to complete
        await expect(page.locator('text=blocked successfully')).toBeVisible();
        
        // Now unblock
        const newUnblockButton = page.locator('button:has-text("Unblock")');
        await newUnblockButton.click();
        
        // Verify success
        await expect(page.locator('text=unblocked successfully')).toBeVisible();
      } else {
        test.skip();
      }
    }
  });

  test('should unblock from blocked list page', async ({ page }) => {
    // Navigate to blocked characters list
    await page.goto('/characters/blocked/');
    
    // Look for unblock button
    const unblockButton = page.locator('button:has-text("Unblock")');
    
    if (await unblockButton.count() > 0) {
      // Click first unblock button
      await unblockButton.first().click();
      
      // Verify success message
      await expect(page.locator('text=unblocked successfully')).toBeVisible();
      
      // Character should be removed from list (or list should be empty)
      // Wait a moment for page to update
      await page.waitForTimeout(500);
    } else {
      // No blocked characters - skip
      test.skip();
    }
  });
});



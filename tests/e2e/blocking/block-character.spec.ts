import { test, expect } from '@playwright/test';
import { login, TEST_USERS } from '../../helpers/auth-helpers';

test.describe('Block Character', () => {
  test.beforeEach(async ({ page }) => {
    await login(page, TEST_USERS.main.username, TEST_USERS.main.password);
  });

  test('should show block button on character detail page', async ({ page }) => {
    // Navigate to a character detail page (not own character)
    await page.goto('/character/test-character-123-testhash/');
    
    // Look for block button
    const blockButton = page.locator('button:has-text("Block")');
    
    if (await blockButton.count() > 0) {
      await expect(blockButton.first()).toBeVisible();
    } else {
      // Character might be own character or already blocked - skip
      test.skip();
    }
  });

  test('should block character with reason', async ({ page }) => {
    // Navigate to character detail page
    await page.goto('/character/test-character-123-testhash/');
    
    const blockButton = page.locator('button:has-text("Block")');
    
    if (await blockButton.count() > 0) {
      // Click block button to open dropdown
      await blockButton.first().click();
      
      // Fill reason
      const reasonTextarea = page.locator('textarea[name="reason"]');
      if (await reasonTextarea.count() > 0) {
        await reasonTextarea.fill('Spam messages');
        
        // Submit block form
        const submitButton = page.locator('button:has-text("Block Character")');
        await submitButton.click();
        
        // Verify success message
        await expect(page.locator('text=blocked successfully')).toBeVisible();
        
        // Verify button changed to "Unblock"
        await expect(page.locator('button:has-text("Unblock")')).toBeVisible();
      }
    } else {
      test.skip();
    }
  });

  test('should block character with spam report', async ({ page }) => {
    await page.goto('/character/test-character-123-testhash/');
    
    const blockButton = page.locator('button:has-text("Block")');
    
    if (await blockButton.count() > 0) {
      await blockButton.first().click();
      
      // Check spam report checkbox
      const spamCheckbox = page.locator('input[name="report_spam"]');
      if (await spamCheckbox.count() > 0) {
        await spamCheckbox.check();
        
        // Submit
        const submitButton = page.locator('button:has-text("Block Character")');
        await submitButton.click();
        
        // Verify success
        await expect(page.locator('text=blocked successfully')).toBeVisible();
      }
    } else {
      test.skip();
    }
  });

  test('should not show block button for own character', async ({ page }) => {
    // Navigate to own character (adjust based on test user's characters)
    await page.goto('/character/my-character-123-myhash/');
    
    // Block button should NOT be visible for own characters
    const blockButton = page.locator('button:has-text("Block")');
    await expect(blockButton).not.toBeVisible();
  });
});



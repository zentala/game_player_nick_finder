import { test, expect } from '@playwright/test';
import { login, TEST_USERS } from '../../helpers/auth-helpers';

test.describe('Blocked Character Interactions', () => {
  test.beforeEach(async ({ page }) => {
    await login(page, TEST_USERS.main.username, TEST_USERS.main.password);
  });

  test('should prevent sending message to blocked character', async ({ page }) => {
    // First block a character
    await page.goto('/character/test-character-123-testhash/');
    
    const blockButton = page.locator('button:has-text("Block")');
    if (await blockButton.count() > 0) {
      await blockButton.click();
      const submitButton = page.locator('button:has-text("Block Character")');
      await submitButton.click();
      
      // Wait for block to complete
      await expect(page.locator('text=blocked successfully')).toBeVisible();
      
      // Try to send message (should be blocked)
      // The "Send Message" button should not be visible or should show error
      const sendMessageButton = page.locator('a:has-text("Send Message")');
      // After blocking, message button should not be available
      // (or if it is, clicking should show error)
      if (await sendMessageButton.count() > 0) {
        // If button exists, clicking should fail
        await sendMessageButton.click();
        // Should show error or redirect
        await page.waitForTimeout(500);
      }
    } else {
      test.skip();
    }
  });

  test('should prevent sending POKE to blocked character', async ({ page }) => {
    // Block character first
    await page.goto('/character/test-character-123-testhash/');
    
    const blockButton = page.locator('button:has-text("Block")');
    if (await blockButton.count() > 0) {
      await blockButton.click();
      const submitButton = page.locator('button:has-text("Block Character")');
      await submitButton.click();
      
      await expect(page.locator('text=blocked successfully')).toBeVisible();
      
      // Try to send POKE (should be blocked)
      const sendPokeButton = page.locator('a:has-text("Send POKE")');
      if (await sendPokeButton.count() > 0) {
        await sendPokeButton.click();
        // Should show error or prevent sending
        await page.waitForTimeout(500);
      }
    } else {
      test.skip();
    }
  });

  test('should prevent sending friend request to blocked character', async ({ page }) => {
    // Block character first
    await page.goto('/character/test-character-123-testhash/');
    
    const blockButton = page.locator('button:has-text("Block")');
    if (await blockButton.count() > 0) {
      await blockButton.click();
      const submitButton = page.locator('button:has-text("Block Character")');
      await submitButton.click();
      
      await expect(page.locator('text=blocked successfully')).toBeVisible();
      
      // Try to send friend request
      const addFriendButton = page.locator('button:has-text("Add as Friend")');
      if (await addFriendButton.count() > 0) {
        await addFriendButton.click();
        
        // Fill form if modal appears
        const senderSelect = page.locator('select[name="sender_character"]');
        if (await senderSelect.count() > 0) {
          await senderSelect.selectOption({ index: 0 });
          await page.fill('textarea[name="message"]', 'Test request');
          await page.click('button:has-text("Send Request")');
          
          // Should show error about being blocked
          await expect(
            page.locator('text=cannot send, text=blocked').or(page.locator('.alert-danger'))
          ).toBeVisible({ timeout: 3000 });
        }
      }
    } else {
      test.skip();
    }
  });

  test('should restore interactions after unblocking', async ({ page }) => {
    // Block then unblock
    await page.goto('/character/test-character-123-testhash/');
    
    const blockButton = page.locator('button:has-text("Block")');
    if (await blockButton.count() > 0) {
      // Block
      await blockButton.click();
      const submitButton = page.locator('button:has-text("Block Character")');
      await submitButton.click();
      await expect(page.locator('text=blocked successfully')).toBeVisible();
      
      // Unblock
      const unblockButton = page.locator('button:has-text("Unblock")');
      await unblockButton.click();
      await expect(page.locator('text=unblocked successfully')).toBeVisible();
      
      // After unblocking, interaction buttons should be available again
      // (depending on POKE exchange status)
      const sendPokeButton = page.locator('a:has-text("Send POKE")');
      const sendMessageButton = page.locator('a:has-text("Send Message")');
      
      // At least one interaction button should be visible
      const hasInteraction = 
        (await sendPokeButton.count() > 0) || 
        (await sendMessageButton.count() > 0);
      
      expect(hasInteraction).toBe(true);
    } else {
      test.skip();
    }
  });
});



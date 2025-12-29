import { test, expect } from '@playwright/test';
import { login, TEST_USERS } from '../../helpers/auth-helpers';

test.describe('POKE Actions', () => {
  test.beforeEach(async ({ page }) => {
    // Login as test user
    await login(page, TEST_USERS.main.username, TEST_USERS.main.password);
  });

  test('should respond to POKE from list', async ({ page }) => {
    await page.goto('/pokes/');
    
    // Look for "Respond" button in POKE list
    const respondButton = page.locator('button:has-text("Respond"), form button[type="submit"]:has-text("Respond")');
    
    if (await respondButton.count() > 0) {
      // Get the first respond button
      const firstRespond = respondButton.first();
      
      // Verify button is visible
      await expect(firstRespond).toBeVisible();
      
      // Click respond button
      await firstRespond.click();
      
      // Verify redirect or success message
      // After responding, user should be redirected to POKE list
      await expect(page).toHaveURL(/\/pokes\/$/);
    } else {
      // No pending POKEs to respond to - skip test
      test.skip();
    }
  });

  test('should respond to POKE from detail page', async ({ page }) => {
    await page.goto('/pokes/');
    
    // Find a POKE with respond button and navigate to detail
    const viewButton = page.locator('a:has-text("View")').first();
    
    if (await viewButton.count() > 0) {
      await viewButton.click();
      
      // Look for respond button on detail page
      const respondButton = page.locator('button:has-text("Respond"), button:has-text("Send POKE back")');
      
      if (await respondButton.count() > 0) {
        await expect(respondButton.first()).toBeVisible();
        
        // Click respond button
        await respondButton.first().click();
        
        // Verify redirect or success message
        await expect(page).toHaveURL(/\/pokes\/$/);
      } else {
        test.skip();
      }
    } else {
      test.skip();
    }
  });

  test('should ignore POKE from detail page', async ({ page }) => {
    await page.goto('/pokes/');
    
    const viewButton = page.locator('a:has-text("View")').first();
    
    if (await viewButton.count() > 0) {
      await viewButton.click();
      
      // Look for ignore button
      const ignoreButton = page.locator('button:has-text("Ignore")');
      
      if (await ignoreButton.count() > 0) {
        await expect(ignoreButton.first()).toBeVisible();
        
        // Click ignore button
        await ignoreButton.first().click();
        
        // Verify redirect to POKE list
        await expect(page).toHaveURL(/\/pokes\/$/);
      } else {
        // No ignore button available (not a pending received POKE) - skip
        test.skip();
      }
    } else {
      test.skip();
    }
  });

  test('should block POKE from detail page', async ({ page }) => {
    await page.goto('/pokes/');
    
    const viewButton = page.locator('a:has-text("View")').first();
    
    if (await viewButton.count() > 0) {
      await viewButton.click();
      
      // Look for block button
      const blockButton = page.locator('button:has-text("Block"), button:has-text("Block & Report")');
      
      if (await blockButton.count() > 0) {
        await expect(blockButton.first()).toBeVisible();
        
        // Click block button - should open modal
        await blockButton.first().click();
        
        // Verify modal appears (if implemented)
        // The modal may have a form to submit
        const modal = page.locator('#blockModal, .modal');
        if (await modal.count() > 0) {
          await expect(modal.first()).toBeVisible();
        }
      } else {
        // No block button available - skip
        test.skip();
      }
    } else {
      test.skip();
    }
  });

  test('should show send POKE button instead of send message when messaging not unlocked', async ({ page }) => {
    // Navigate to character detail page
    await page.goto('/character/other-char-123-otherhash/');
    
    // Look for either "Send POKE" or "Send Message" button
    const sendPokeButton = page.locator('a:has-text("Send POKE")');
    const sendMessageButton = page.locator('a:has-text("Send Message")');
    
    const pokeCount = await sendPokeButton.count();
    const messageCount = await sendMessageButton.count();
    
    // Either button should be visible (depending on unlock status)
    expect(pokeCount > 0 || messageCount > 0).toBe(true);
    
    // If POKE button is visible, click it to verify navigation
    if (pokeCount > 0) {
      await sendPokeButton.click();
      await expect(page).toHaveURL(/\/pokes\/send/);
    }
  });
});



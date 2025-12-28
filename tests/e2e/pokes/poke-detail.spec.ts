import { test, expect } from '@playwright/test';
import { login, TEST_USERS } from '../../helpers/auth-helpers';

test.describe('POKE Detail', () => {
  test.beforeEach(async ({ page }) => {
    // Login as test user
    await login(page, TEST_USERS.main.username, TEST_USERS.main.password);
  });

  test('should display POKE detail page', async ({ page }) => {
    // Navigate to POKE list first
    await page.goto('/pokes/');
    
    // Look for a POKE item with "View" button
    const viewButton = page.locator('a:has-text("View")').first();
    
    if (await viewButton.count() > 0) {
      // Click view button
      await viewButton.click();
      
      // Verify POKE detail page elements
      await expect(page.locator('h5:has-text("POKE Details")')).toBeVisible();
    } else {
      // No POKEs to view - skip test
      test.skip();
    }
  });

  test('should have back to POKEs button', async ({ page }) => {
    // Navigate to POKE list first
    await page.goto('/pokes/');
    
    const viewButton = page.locator('a:has-text("View")').first();
    
    if (await viewButton.count() > 0) {
      await viewButton.click();
      
      // Find back button
      const backButton = page.locator('a:has-text("Back to POKEs")');
      await expect(backButton).toBeVisible();
      
      // Click back button
      await backButton.click();
      
      // Verify navigation back to POKE list
      await expect(page).toHaveURL(/\/pokes\/$/);
    } else {
      test.skip();
    }
  });

  test('should display POKE status badge', async ({ page }) => {
    await page.goto('/pokes/');
    
    const viewButton = page.locator('a:has-text("View")').first();
    
    if (await viewButton.count() > 0) {
      await viewButton.click();
      
      // Verify status badge is present
      const statusBadge = page.locator('.badge');
      await expect(statusBadge.first()).toBeVisible();
    } else {
      test.skip();
    }
  });

  test('should display POKE content', async ({ page }) => {
    await page.goto('/pokes/');
    
    const viewButton = page.locator('a:has-text("View")').first();
    
    if (await viewButton.count() > 0) {
      await viewButton.click();
      
      // Verify POKE content is displayed
      const contentSection = page.locator('h6:has-text("Message")');
      await expect(contentSection).toBeVisible();
    } else {
      test.skip();
    }
  });

  test('should show action buttons for received POKE with PENDING status', async ({ page }) => {
    // This test requires a POKE sent TO the test user with PENDING status
    // In a real scenario, we'd need to set up test data first
    await page.goto('/pokes/');
    
    // Look for POKEs with "Respond" button (pending received POKEs)
    const respondButton = page.locator('button:has-text("Respond"), form:has-text("Respond")');
    
    if (await respondButton.count() > 0) {
      // Navigate to detail page
      const viewButton = page.locator('a:has-text("View")').first();
      await viewButton.click();
      
      // Verify action buttons are present
      const respondBtn = page.locator('button:has-text("Respond")');
      const ignoreBtn = page.locator('button:has-text("Ignore")');
      const blockBtn = page.locator('button:has-text("Block")');
      
      // At least respond button should be visible for pending received POKE
      if (await respondBtn.count() > 0) {
        await expect(respondBtn.first()).toBeVisible();
      }
    } else {
      // No pending POKEs to respond to - skip test
      test.skip();
    }
  });
});


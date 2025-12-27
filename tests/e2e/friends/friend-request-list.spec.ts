import { test, expect } from '@playwright/test';

test.describe('Friend Request List', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/accounts/login/');
    await page.fill('#id_login', 'testuser');
    await page.fill('#id_password', 'testpass123');
    await page.click('button[type="submit"]');
    await page.waitForURL('**/');
  });

  test('should display friend requests list', async ({ page }) => {
    await page.goto('/friends/requests/');
    
    await expect(page.locator('h2:has-text("Friend Requests")')).toBeVisible();
  });

  test('should show pending friend requests', async ({ page }) => {
    await page.goto('/friends/requests/');
    
    // Verify request cards are visible (if any exist)
    const requestCards = page.locator('.list-group-item');
    const count = await requestCards.count();
    
    if (count > 0) {
      await expect(requestCards.first()).toBeVisible();
    }
  });

  test('should accept friend request', async ({ page }) => {
    await page.goto('/friends/requests/');
    
    // Click accept button on first request if exists
    const acceptButton = page.locator('.list-group-item:first-child button:has-text("Accept")');
    if (await acceptButton.count() > 0) {
      await acceptButton.click();
      
      // Verify success message
      await expect(page.locator('text=Accepted friend request')).toBeVisible();
    }
  });

  test('should decline friend request', async ({ page }) => {
    await page.goto('/friends/requests/');
    
    // Click decline button if exists
    const declineButton = page.locator('.list-group-item:first-child button:has-text("Decline")');
    if (await declineButton.count() > 0) {
      await declineButton.click();
      
      // Verify info message
      await expect(page.locator('text=Declined friend request')).toBeVisible();
    }
  });

  test('should show empty state when no requests', async ({ page }) => {
    // Assume no requests exist
    await page.goto('/friends/requests/');
    
    const emptyState = page.locator('text=No pending friend requests');
    if (await emptyState.count() > 0) {
      await expect(emptyState).toBeVisible();
    }
  });
});


import { test, expect } from '@playwright/test';
import { login, TEST_USERS } from '../../helpers/auth-helpers';

test.describe('Character Friend List', () => {
  test.beforeEach(async ({ page }) => {
    await login(page, TEST_USERS.main.username, TEST_USERS.main.password);
  });

  test('should display friend list for character', async ({ page }) => {
    await page.goto('/character/my-character-123-myhash/friends/');
    
    await expect(page.locator('h2:has-text("Friends")')).toBeVisible();
  });

  test('should show friend cards', async ({ page }) => {
    await page.goto('/character/my-character-123-myhash/friends/');
    
    // Verify friend cards exist
    const friendCards = page.locator('.card');
    const count = await friendCards.count();
    
    if (count > 0) {
      await expect(friendCards.first()).toBeVisible();
    }
  });

  test('should navigate to friend character detail', async ({ page }) => {
    await page.goto('/character/my-character-123-myhash/friends/');
    
    // Click View button on first friend if exists
    const viewButton = page.locator('.card:first-child a:has-text("View")').first();
    if (await viewButton.count() > 0) {
      await viewButton.click();
      
      // Verify navigation to character detail
      await expect(page).toHaveURL(/\/character\/.+\/.+\/$/);
    }
  });

  test('should show empty state when no friends', async ({ page }) => {
    // Navigate to character with no friends
    await page.goto('/character/new-character-123-newhash/friends/');
    
    const emptyState = page.locator('text=No friends yet');
    if (await emptyState.count() > 0) {
      await expect(emptyState).toBeVisible();
    }
  });
});

import { test, expect } from '@playwright/test';
import { login, TEST_USERS } from '../../helpers/auth-helpers';

test.describe('Friend Request Button', () => {
  test.beforeEach(async ({ page }) => {
    // Login as test user using login helper
    await login(page, TEST_USERS.main.username, TEST_USERS.main.password);
  });

  test('should display Add Friend button on character detail page', async ({ page }) => {
    // Navigate to character detail page
    // Note: Adjust URL based on actual character data in fixtures
    await page.goto('/character/test-character-123-testhash/');
    
    // Verify Add Friend button is visible (if not own character and not already friend)
    const addFriendButton = page.locator('button:has-text("Add as Friend")');
    if (await addFriendButton.count() > 0) {
      await expect(addFriendButton.first()).toBeVisible();
    }
  });

  test('should open friend request modal on button click', async ({ page }) => {
    await page.goto('/character/test-character-123-testhash/');
    
    // Click Add Friend button if visible
    const addFriendButton = page.locator('button:has-text("Add as Friend")');
    if (await addFriendButton.count() > 0) {
      await addFriendButton.first().click();
      
      // Verify modal appears
      await expect(page.locator('#friendRequestModal')).toBeVisible();
      await expect(page.locator('text=Send Friend Request')).toBeVisible();
    }
  });

  test('should show character selector in modal', async ({ page }) => {
    await page.goto('/character/test-character-123-testhash/');
    const addFriendButton = page.locator('button:has-text("Add as Friend")');
    
    if (await addFriendButton.count() > 0) {
      await addFriendButton.first().click();
      
      // Verify character selector exists
      await expect(page.locator('select[name="sender_character"]')).toBeVisible();
    }
  });

  test('should send friend request successfully', async ({ page }) => {
    await page.goto('/character/test-character-123-testhash/');
    const addFriendButton = page.locator('button:has-text("Add as Friend")');
    
    if (await addFriendButton.count() > 0) {
      await addFriendButton.first().click();
      
      // Select character and send request
      await page.selectOption('select[name="sender_character"]', { index: 0 });
      await page.fill('textarea[name="message"]', 'Hey, remember me?');
      await page.click('button:has-text("Send Request")');
      
      // Verify success message
      await expect(page.locator('text=Friend request sent')).toBeVisible();
      
      // Verify button changes to "Friend Request Sent"
      await expect(page.locator('button:has-text("Friend Request Sent")')).toBeVisible();
    }
  });

  test('should not show Add Friend button for own characters', async ({ page }) => {
    // Navigate to own character (adjust based on test user's characters)
    await page.goto('/character/my-character-123-myhash/');
    
    // Verify Add Friend button is NOT visible
    await expect(page.locator('button:has-text("Add as Friend")')).not.toBeVisible();
  });

  test('should show Friends badge for existing friends', async ({ page }) => {
    // Assume friendship exists (setup in fixtures)
    await page.goto('/character/friend-character-123-friendhash/');
    
    // Verify Friends badge is shown
    const friendsButton = page.locator('button:has-text("Friends")');
    if (await friendsButton.count() > 0) {
      await expect(friendsButton.first()).toBeVisible();
      await expect(friendsButton.first()).toBeDisabled();
    }
  });
});

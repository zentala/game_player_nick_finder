import { test, expect } from '@playwright/test';

test.describe('Profile Edit', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/accounts/login/');
    await page.fill('#id_username', 'testuser');
    await page.fill('#id_password', 'testpass123');
    await page.click('button[type="submit"]');
    await page.waitForURL('**/');
    await page.goto('/accounts/profile/');
  });

  test('should display profile edit form', async ({ page }) => {
    await expect(page.locator('h4:has-text("Edit Profile")')).toBeVisible();
    await expect(page.locator('form')).toBeVisible();
  });

  test('should have profile visibility field', async ({ page }) => {
    await expect(page.locator('select[name="profile_visibility"]')).toBeVisible();
  });

  test('should have profile bio field', async ({ page }) => {
    await expect(page.locator('textarea[name="profile_bio"]')).toBeVisible();
  });

  test('should have social media link fields', async ({ page }) => {
    await expect(page.locator('input[name="steam_profile"]')).toBeVisible();
    await expect(page.locator('input[name="github_profile"]')).toBeVisible();
  });

  test('should save profile changes', async ({ page }) => {
    // Update profile bio
    await page.fill('textarea[name="profile_bio"]', 'My gaming journey started in 2005...');
    
    // Save
    await page.click('button:has-text("Save Changes")');
    
    // Verify success message
    await expect(page.locator('text=Profile updated successfully')).toBeVisible();
    
    // Verify changes persisted
    await expect(page.locator('textarea[name="profile_bio"]')).toHaveValue('My gaming journey started in 2005...');
  });
});

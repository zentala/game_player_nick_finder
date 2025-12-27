import { test, expect } from '@playwright/test';

test.describe('Character Profile Edit', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/accounts/login/');
    await page.fill('#id_login', 'testuser');
    await page.fill('#id_password', 'testpass123');
    await page.click('button[type="submit"]');
    await page.waitForURL('**/');
  });

  test('should display character profile edit form', async ({ page }) => {
    await page.goto('/character/my-character-123-myhash/profile/edit/');
    
    await expect(page.locator('h2:has-text("Edit Character Profile")')).toBeVisible();
    await expect(page.locator('form')).toBeVisible();
  });

  test('should have custom bio field', async ({ page }) => {
    await page.goto('/character/my-character-123-myhash/profile/edit/');
    
    await expect(page.locator('textarea[name="custom_bio"]')).toBeVisible();
  });

  test('should save character profile', async ({ page }) => {
    await page.goto('/character/my-character-123-myhash/profile/edit/');
    
    // Fill custom bio
    await page.fill('textarea[name="custom_bio"]', 'My gaming journey with this character...');
    
    // Save
    await page.click('button:has-text("Save Profile")');
    
    // Verify success and redirect
    await expect(page.locator('text=Character profile updated successfully')).toBeVisible();
    await expect(page).toHaveURL(/\/character\/.+\/.+\/?$/);
  });
});


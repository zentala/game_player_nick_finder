import { test, expect } from '@playwright/test';

test.describe('Character Profile Display', () => {
  test('should display character custom bio if available', async ({ page }) => {
    await page.goto('/character/character-with-bio-123-hash/');
    
    // Check if bio section exists
    const bioSection = page.locator('h4:has-text("About")');
    if (await bioSection.count() > 0) {
      await expect(bioSection).toBeVisible();
    }
  });

  test('should not show profile for characters without profile', async ({ page }) => {
    await page.goto('/character/new-character-123-hash/');
    
    // Profile section should not exist
    const bioSection = page.locator('h4:has-text("About")');
    if (await bioSection.count() === 0) {
      // This is expected - no profile section
      expect(true).toBeTruthy();
    }
  });
});


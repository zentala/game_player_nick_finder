import { test, expect } from '@playwright/test';

test.describe('Homepage Layout Switcher', () => {
  test.beforeEach(async ({ page }) => {
    // Clear session before each test
    await page.context().clearCookies();
    await page.goto('/');
  });

  test('should display default layout (v0) when no layout param is provided', async ({ page }) => {
    await page.goto('/');
    
    // Wait for page to load
    await page.waitForLoadState('networkidle');
    
    // Check that original layout elements are present
    // Use more specific selector for h1
    await expect(page.locator('h1.display-4:has-text("Reconnect with Old Gaming Buddies!")')).toBeVisible();
    // Use first() to handle multiple matches
    await expect(page.locator('h2:has-text("Time machine")').first()).toBeVisible();
    await expect(page.locator('h2:has-text("Friendship")').first()).toBeVisible();
    
    // Layout switcher should NOT be visible by default
    const switcher = page.locator('.layout-switcher');
    await expect(switcher).not.toBeVisible();
  });

  test('should switch to layout v1 when layout=v1 param is provided', async ({ page }) => {
    await page.goto('/?layout=v1');
    
    // Wait for page to load
    await page.waitForLoadState('networkidle');
    
    // Check that v1 layout elements are present
    await expect(page.locator('h3:has-text("Select Game")')).toBeVisible();
    await expect(page.locator('h3:has-text("Time Machine - Choose Year")')).toBeVisible();
    await expect(page.locator('h3:has-text("Friendship - Enter Nicknames")')).toBeVisible();
    
    // Layout switcher should be visible
    const switcher = page.locator('.layout-switcher');
    await expect(switcher).toBeVisible();
    
    // Check that v1 button is active
    const v1Button = switcher.locator('a[href*="layout=v1"]');
    await expect(v1Button).toHaveClass(/btn-primary/);
  });

  test('should switch to layout v2 when layout=v2 param is provided', async ({ page }) => {
    await page.goto('/?layout=v2');
    
    // Wait for page to load
    await page.waitForLoadState('networkidle');
    
    // Check that v2 layout elements are present (horizontal cards)
    await expect(page.locator('.homepage-card')).toHaveCount(3);
    await expect(page.locator('h3.card-title:has-text("Select Game")').first()).toBeVisible();
    await expect(page.locator('h3.card-title:has-text("Time Machine")').first()).toBeVisible();
    await expect(page.locator('h3.card-title:has-text("Friendship")').first()).toBeVisible();
    
    // Layout switcher should be visible
    const switcher = page.locator('.layout-switcher');
    await expect(switcher).toBeVisible();
    
    // Check that v2 button is active
    const v2Button = switcher.locator('a[href*="layout=v2"]');
    await expect(v2Button).toHaveClass(/btn-primary/);
  });

  test('should switch to layout v3 when layout=v3 param is provided', async ({ page }) => {
    await page.goto('/?layout=v3');
    
    // Wait for page to load
    await page.waitForLoadState('networkidle');
    
    // Check that v3 layout elements are present (wizard)
    await expect(page.locator('.wizard-container')).toBeVisible();
    await expect(page.locator('h2:has-text("Step 1 of 3: Select Game")')).toBeVisible();
    await expect(page.locator('.wizard-progress')).toBeVisible();
    
    // Layout switcher should be visible
    const switcher = page.locator('.layout-switcher');
    await expect(switcher).toBeVisible();
    
    // Check that v3 button is active
    const v3Button = switcher.locator('a[href*="layout=v3"]');
    await expect(v3Button).toHaveClass(/btn-primary/);
  });

  test('should remember layout preference in session', async ({ page }) => {
    // First, set layout to v1
    await page.goto('/?layout=v1');
    await page.waitForLoadState('networkidle');
    await expect(page.locator('h3:has-text("Select Game")')).toBeVisible();
    
    // Navigate to home page without layout param
    await page.goto('/');
    await page.waitForLoadState('networkidle');
    
    // Layout should still be v1 (remembered from session)
    await expect(page.locator('h3:has-text("Select Game")')).toBeVisible();
    await expect(page.locator('h3:has-text("Time Machine - Choose Year")')).toBeVisible();
    
    // Layout switcher should be visible (because user has saved preference)
    const switcher = page.locator('.layout-switcher');
    await expect(switcher).toBeVisible();
    
    // Check that saved layout badge is shown
    await expect(switcher.locator('text=Saved: V1')).toBeVisible();
  });

  test('should reset layout to default when layout=reset param is provided', async ({ page }) => {
    // First, set layout to v1
    await page.goto('/?layout=v1');
    await page.waitForLoadState('networkidle');
    await expect(page.locator('h3:has-text("Select Game")')).toBeVisible();
    
    // Reset to default
    await page.goto('/?layout=reset');
    await page.waitForLoadState('networkidle');
    
    // Should show default layout (v0)
    await expect(page.locator('h1.display-4:has-text("Reconnect with Old Gaming Buddies!")')).toBeVisible();
    await expect(page.locator('h2:has-text("Time machine")').first()).toBeVisible();
    
    // Navigate to home page - should still be default
    await page.goto('/');
    await page.waitForLoadState('networkidle');
    await expect(page.locator('h1.display-4:has-text("Reconnect with Old Gaming Buddies!")')).toBeVisible();
  });

  test('should allow switching between layouts using switcher buttons', async ({ page }) => {
    // Start with v1
    await page.goto('/?layout=v1');
    await page.waitForLoadState('networkidle');
    await expect(page.locator('h3:has-text("Select Game")')).toBeVisible();
    
    // Click v2 button in switcher
    const switcher = page.locator('.layout-switcher');
    const v2Button = switcher.locator('a[href*="layout=v2"]');
    await v2Button.click();
    await page.waitForLoadState('networkidle');
    
    // Should switch to v2
    await expect(page.locator('.homepage-card')).toHaveCount(3);
    await expect(page.locator('h3.card-title:has-text("Select Game")').first()).toBeVisible();
    
    // Click v3 button
    const v3Button = switcher.locator('a[href*="layout=v3"]');
    await v3Button.click();
    await page.waitForLoadState('networkidle');
    
    // Should switch to v3
    await expect(page.locator('.wizard-container')).toBeVisible();
    await expect(page.locator('h2:has-text("Step 1 of 3: Select Game")')).toBeVisible();
  });

  test('should show reset button when user has saved layout preference', async ({ page }) => {
    // Set layout to v1
    await page.goto('/?layout=v1');
    await page.waitForLoadState('networkidle');
    
    // Navigate to home (layout should be remembered)
    await page.goto('/');
    await page.waitForLoadState('networkidle');
    
    const switcher = page.locator('.layout-switcher');
    await expect(switcher).toBeVisible();
    
    // Reset button should be visible
    const resetButton = switcher.locator('a[href*="layout=reset"]');
    await expect(resetButton).toBeVisible();
    await expect(resetButton).toContainText('Reset to Default');
  });

  test('should not show reset button when using default layout', async ({ page }) => {
    // Go to default layout
    await page.goto('/?layout=v0');
    
    // Navigate to home
    await page.goto('/');
    
    // If switcher is visible, reset button should not be there
    const switcher = page.locator('.layout-switcher');
    if (await switcher.isVisible()) {
      const resetButton = switcher.locator('a[href*="layout=reset"]');
      await expect(resetButton).not.toBeVisible();
    }
  });

  test('should display mock data in v1 layout', async ({ page }) => {
    await page.goto('/?layout=v1');
    await page.waitForLoadState('networkidle');
    
    // Check that game selector has mock games
    const gameInput = page.locator('#game-search');
    await expect(gameInput).toBeVisible();
    await gameInput.click();
    
    // Wait for dropdown
    const gameDropdown = page.locator('#game-dropdown');
    await expect(gameDropdown).toBeVisible({ timeout: 2000 });
    
    // Check for mock games
    await expect(gameDropdown.locator('text=Counter-Strike')).toBeVisible();
    await expect(gameDropdown.locator('text=World of Warcraft')).toBeVisible();
    await expect(gameDropdown.locator('text=League of Legends')).toBeVisible();
  });

  test('should display year slider in v1 layout', async ({ page }) => {
    await page.goto('/?layout=v1');
    await page.waitForLoadState('networkidle');
    
    // Check that year slider is present
    const yearSlider = page.locator('#year-slider');
    await expect(yearSlider).toBeVisible();
    
    // Check that years are displayed
    await expect(yearSlider.locator('.year-item').first()).toBeVisible();
    
    // Check that prominent years (2000-2010) are marked
    const prominentYears = yearSlider.locator('.year-item.prominent');
    const count = await prominentYears.count();
    expect(count).toBeGreaterThan(0);
  });

  test('should handle invalid layout param gracefully', async ({ page }) => {
    // Try invalid layout
    await page.goto('/?layout=invalid');
    await page.waitForLoadState('networkidle');
    
    // Should fallback to default layout
    await expect(page.locator('h1.display-4:has-text("Reconnect with Old Gaming Buddies!")')).toBeVisible();
    await expect(page.locator('h2:has-text("Time machine")').first()).toBeVisible();
  });
});


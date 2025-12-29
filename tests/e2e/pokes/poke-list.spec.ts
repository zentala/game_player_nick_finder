import { test, expect } from '@playwright/test';
import { login, TEST_USERS } from '../../helpers/auth-helpers';

test.describe('POKE List', () => {
  test.beforeEach(async ({ page }) => {
    // Login as test user
    await login(page, TEST_USERS.main.username, TEST_USERS.main.password);
  });

  test('should display POKE list page', async ({ page }) => {
    await page.goto('/pokes/');
    
    // Verify page title/heading
    await expect(page.locator('h2:has-text("POKEs")')).toBeVisible();
    
    // Verify "Send POKE" button is present
    await expect(page.locator('a:has-text("Send POKE")')).toBeVisible();
  });

  test('should display filter tabs', async ({ page }) => {
    await page.goto('/pokes/');
    
    // Verify filter tabs are present
    await expect(page.locator('a:has-text("All")')).toBeVisible();
    await expect(page.locator('a:has-text("Received")')).toBeVisible();
    await expect(page.locator('a:has-text("Sent")')).toBeVisible();
    await expect(page.locator('a:has-text("Pending")')).toBeVisible();
  });

  test('should navigate to send POKE page from list', async ({ page }) => {
    await page.goto('/pokes/');
    
    // Click "Send POKE" button
    await page.click('a:has-text("Send POKE")');
    
    // Verify navigation to send POKE page
    await expect(page).toHaveURL(/\/pokes\/send/);
    await expect(page.locator('h5:has-text("Send POKE")')).toBeVisible();
  });

  test('should filter by received POKEs', async ({ page }) => {
    await page.goto('/pokes/');
    
    // Click "Received" filter tab
    await page.click('a:has-text("Received")');
    
    // Verify URL includes status filter
    await expect(page).toHaveURL(/status=received/);
  });

  test('should filter by sent POKEs', async ({ page }) => {
    await page.goto('/pokes/');
    
    // Click "Sent" filter tab
    await page.click('a:has-text("Sent")');
    
    // Verify URL includes status filter
    await expect(page).toHaveURL(/status=sent/);
  });

  test('should filter by pending POKEs', async ({ page }) => {
    await page.goto('/pokes/');
    
    // Click "Pending" filter tab
    await page.click('a:has-text("Pending")');
    
    // Verify URL includes status filter
    await expect(page).toHaveURL(/status=pending/);
  });

  test('should show empty state when no POKEs', async ({ page }) => {
    await page.goto('/pokes/');
    
    // If no POKEs exist, should show empty message
    const emptyMessage = page.locator('text=No POKEs found');
    const pokeList = page.locator('.list-group-item');
    
    // Either empty message or list items should be visible
    const emptyCount = await emptyMessage.count();
    const listCount = await pokeList.count();
    
    expect(emptyCount > 0 || listCount > 0).toBe(true);
  });

  test('should display POKE link in navbar', async ({ page }) => {
    await page.goto('/');
    
    // Click user menu dropdown
    await page.click('a.nav-link.dropdown-toggle');
    
    // Verify POKEs link is present in menu
    const pokeLink = page.locator('a:has-text("POKEs")');
    await expect(pokeLink).toBeVisible();
    
    // Click POKEs link
    await pokeLink.click();
    
    // Verify navigation to POKE list
    await expect(page).toHaveURL(/\/pokes\/$/);
  });
});



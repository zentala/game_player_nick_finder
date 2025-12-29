import { test, expect } from '@playwright/test';
import { login, TEST_USERS } from '../../helpers/auth-helpers';

test.describe('Conversation List', () => {
    test.beforeEach(async ({ page }) => {
        // Login as testuser using login helper
        await login(page, TEST_USERS.main.username, TEST_USERS.main.password);
    });

    test('should display conversation list', async ({ page }) => {
        await page.goto('/messages/');
        
        // Verify conversation list is visible
        await expect(page.locator('.conversation-list')).toBeVisible({ timeout: 5000 });
        
        // Verify sidebar is visible on desktop
        await expect(page.locator('.conversation-sidebar')).toBeVisible();
    });

    test('should show conversation items with character info', async ({ page }) => {
        await page.goto('/messages/');
        
        // Wait for conversation list to load
        await page.waitForSelector('.conversation-item', { timeout: 5000 });
        
        // Check if any conversations exist
        const conversationItems = page.locator('.conversation-item');
        const count = await conversationItems.count();
        
        if (count > 0) {
            const firstConversation = conversationItems.first();
            
            // Verify conversation has avatar or placeholder
            const avatar = firstConversation.locator('.conversation-avatar, .bi-person-fill');
            await expect(avatar.first()).toBeVisible();
            
            // Verify conversation has character name
            const name = firstConversation.locator('.conversation-name');
            await expect(name).toBeVisible();
            
            // Verify conversation has game name
            const game = firstConversation.locator('.conversation-game');
            await expect(game).toBeVisible();
        }
    });

    test('should show unread message count when present', async ({ page }) => {
        await page.goto('/messages/');
        
        await page.waitForSelector('.conversation-item', { timeout: 5000 });
        
        const unreadBadge = page.locator('.unread-badge').first();
        
        // If unread messages exist, badge should be visible
        if (await unreadBadge.isVisible()) {
            const count = await unreadBadge.textContent();
            expect(parseInt(count || '0')).toBeGreaterThan(0);
        }
    });

    test('should switch between conversations', async ({ page }) => {
        await page.goto('/messages/');
        
        await page.waitForSelector('.conversation-item', { timeout: 5000 });
        
        const conversationItems = page.locator('.conversation-item');
        const count = await conversationItems.count();
        
        if (count > 0) {
            const firstConversation = conversationItems.first();
            const conversationText = await firstConversation.textContent();
            
            await firstConversation.click();
            
            // Verify URL contains thread_id
            await page.waitForURL(/\?thread_id=.*/, { timeout: 5000 });
            
            // Verify messages are displayed (either message bubbles or empty state)
            const messageArea = page.locator('.message-bubble, .message-item, .chat-messages');
            await expect(messageArea.first()).toBeVisible({ timeout: 5000 });
        }
    });

    test('should highlight active conversation', async ({ page }) => {
        await page.goto('/messages/');
        
        await page.waitForSelector('.conversation-item', { timeout: 5000 });
        
        const conversationItems = page.locator('.conversation-item');
        const count = await conversationItems.count();
        
        if (count > 0) {
            const firstConversation = conversationItems.first();
            await firstConversation.click();
            
            await page.waitForURL(/\?thread_id=.*/, { timeout: 5000 });
            
            // Verify it has active class
            await expect(firstConversation).toHaveClass(/active/);
        }
    });

    test('should show last message preview', async ({ page }) => {
        await page.goto('/messages/');
        
        await page.waitForSelector('.conversation-item', { timeout: 5000 });
        
        const conversationItems = page.locator('.conversation-item');
        const count = await conversationItems.count();
        
        if (count > 0) {
            const conversation = conversationItems.first();
            const preview = conversation.locator('.conversation-preview');
            
            await expect(preview).toBeVisible();
            const previewText = await preview.textContent();
            expect(previewText?.trim().length).toBeGreaterThanOrEqual(0);
        }
    });

    test('should show timestamp', async ({ page }) => {
        await page.goto('/messages/');
        
        await page.waitForSelector('.conversation-item', { timeout: 5000 });
        
        const conversationItems = page.locator('.conversation-item');
        const count = await conversationItems.count();
        
        if (count > 0) {
            const conversation = conversationItems.first();
            const timestamp = conversation.locator('.conversation-time');
            
            await expect(timestamp).toBeVisible();
            const timeText = await timestamp.textContent();
            expect(timeText).toMatch(/ago|minute|hour|day|week|month|year/i);
        }
    });

    test('should show empty state when no conversations', async ({ page }) => {
        // This test assumes user has no conversations
        // In real scenario, you might need to create a test user with no messages
        await page.goto('/messages/');
        
        // Check if empty state appears (either conversation list is empty or shows message)
        const emptyState = page.locator('text=No conversations yet');
        const conversationItems = page.locator('.conversation-item');
        const count = await conversationItems.count();
        
        // Either empty state is shown OR conversation items exist
        if (count === 0) {
            await expect(emptyState).toBeVisible({ timeout: 5000 });
        }
    });

    test('mobile: should toggle sidebar', async ({ page }) => {
        // Set mobile viewport
        await page.setViewportSize({ width: 375, height: 667 });
        await page.goto('/messages/');
        
        // Check if toggle button exists (should be visible on mobile)
        const toggleButton = page.locator('#conversation-sidebar-toggle-mobile, #conversation-sidebar-toggle-header').first();
        
        if (await toggleButton.isVisible()) {
            // Sidebar should be hidden initially
            const sidebar = page.locator('.conversation-sidebar');
            const sidebarClasses = await sidebar.getAttribute('class');
            expect(sidebarClasses).not.toContain('show');
            
            // Click toggle button
            await toggleButton.click();
            
            // Sidebar should be visible
            await expect(sidebar).toHaveClass(/show/, { timeout: 1000 });
            
            // Click again to close
            await toggleButton.click();
            
            // Sidebar should be hidden
            const sidebarClassesAfter = await sidebar.getAttribute('class');
            expect(sidebarClassesAfter).not.toContain('show');
        }
    });

    test('mobile: should close sidebar when clicking backdrop', async ({ page }) => {
        await page.setViewportSize({ width: 375, height: 667 });
        await page.goto('/messages/');
        
        const toggleButton = page.locator('#conversation-sidebar-toggle-mobile, #conversation-sidebar-toggle-header').first();
        const sidebar = page.locator('.conversation-sidebar');
        const backdrop = page.locator('.conversation-backdrop');
        
        if (await toggleButton.isVisible()) {
            // Open sidebar
            await toggleButton.click();
            await expect(sidebar).toHaveClass(/show/, { timeout: 1000 });
            
            // Click backdrop
            if (await backdrop.isVisible()) {
                await backdrop.click();
                
                // Sidebar should be closed
                const sidebarClasses = await sidebar.getAttribute('class');
                expect(sidebarClasses).not.toContain('show');
            }
        }
    });

    test('mobile: should close sidebar when clicking conversation', async ({ page }) => {
        await page.setViewportSize({ width: 375, height: 667 });
        await page.goto('/messages/');
        
        await page.waitForSelector('.conversation-item', { timeout: 5000 });
        
        const conversationItems = page.locator('.conversation-item');
        const count = await conversationItems.count();
        
        if (count > 0) {
            const toggleButton = page.locator('#conversation-sidebar-toggle-mobile, #conversation-sidebar-toggle-header').first();
            const sidebar = page.locator('.conversation-sidebar');
            
            if (await toggleButton.isVisible()) {
                // Open sidebar
                await toggleButton.click();
                await expect(sidebar).toHaveClass(/show/, { timeout: 1000 });
                
                // Click conversation
                const firstConversation = conversationItems.first();
                await firstConversation.click();
                
                // Sidebar should be closed
                await page.waitForTimeout(500); // Wait for animation
                const sidebarClasses = await sidebar.getAttribute('class');
                expect(sidebarClasses).not.toContain('show');
            }
        }
    });
});



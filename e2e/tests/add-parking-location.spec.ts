import { test, expect } from '@playwright/test';

test.describe('Add parking location to Balaclava', () => {
  test('Navigate to Balaclava, add parking location, and verify in feed', async ({ page }) => {
    await page.goto('/');

    // Search for and select Balaclava
    const searchInput = page.getByPlaceholder('Enter suburb or postcode');
    await searchInput.fill('Balaclava');
    await searchInput.press('Enter');
    await page.locator('text=/Balaclava/i').first().click();
    await page.waitForLoadState('networkidle');

    // Fill address field
    const addressInput = page.locator('input[placeholder="Search for an address..."]');
    await addressInput.fill('123 Carlisle Street');
    await page.waitForTimeout(1000);

    // Select from autocomplete if available, otherwise use entered text
    const addressSuggestion = page.locator('.v-list-item:has-text("123 Carlisle Street")').first();
    if (await addressSuggestion.isVisible({ timeout: 2000 }).catch(() => false)) {
      await addressSuggestion.click();
    } else {
      await page.keyboard.press('Enter');
    }

    // parking type dropdown
    await page.locator('.v-select').nth(0).click();
    await page.locator('.v-list-item-title:has-text("On-Street")').click();

    // lighting dropdown
    await page.locator('.v-select').nth(1).click();
    await page.locator('.v-list-item-title:has-text("Good")').click();

    // CCTV dropdown
    await page.locator('.v-select').nth(2).click();
    await page.locator('.v-list-item-title:has-text("Yes")').first().click();

    await page.locator('button:has-text("Submit")').click();

    // Handle success dialog
    const successDialog = page.locator('.v-dialog .v-card:has-text("Thank you!")');
    await expect(successDialog).toBeVisible({ timeout: 10000 });
    await page.locator('.v-dialog button:has-text("Got it")').click();
    await expect(successDialog).not.toBeVisible();

    // Verify parking location appears in feed
    await expect(page.locator('.parking-feed .v-card-title:has-text("123 CARLISLE STREET")').first()).toBeVisible({ timeout: 10000 });

    // Verify feed counter shows at least 1
    const feedCounter = page.locator('.parking-feed .v-card-title .v-chip');
    const counterText = await feedCounter.textContent();
    expect(parseInt(counterText || '0')).toBeGreaterThan(0);
  });
});

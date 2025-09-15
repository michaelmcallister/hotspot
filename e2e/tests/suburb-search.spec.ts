import { test, expect } from '@playwright/test';

test.describe('As a rider, I want to search for parking by suburb or postcode so I can easily find options near my destination', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/');
  });

  test('The rider can enter either a suburb name or postcode into a search field', async ({ page }) => {
    const searchInput = page.getByPlaceholder('Enter suburb or postcode');

    // Test searching by suburb name
    await searchInput.fill('Balaclava');
    await searchInput.press('Enter');
    await page.waitForTimeout(1000);

    // Clear and test searching by postcode
    await searchInput.clear();
    await searchInput.fill('3183');
    await searchInput.press('Enter');
    await page.waitForTimeout(1000);
  });

  test('Search results return accurate data from the database (suburb name and postcode match correctly)', async ({ page }) => {
    const searchInput = page.getByPlaceholder('Enter suburb or postcode');

    // Test with suburb name
    await searchInput.fill('Balaclava');
    await searchInput.press('Enter');
    await page.waitForTimeout(1500);

    // Verify that Balaclava appears in results
    const balaclavaResult = page.locator('text=/Balaclava/i');
    await expect(balaclavaResult.first()).toBeVisible();

    // Clear and test with postcode
    await searchInput.clear();
    await searchInput.fill('3183');
    await searchInput.press('Enter');
    await page.waitForTimeout(1500);

    // Verify that results for postcode 3183 are visible
    const postcodeResult = page.locator('text=/3183/');
    await expect(postcodeResult.first()).toBeVisible();
  });
});
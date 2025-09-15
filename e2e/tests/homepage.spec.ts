import { test, expect } from '@playwright/test';

test('homepage loads successfully', async ({ page }) => {
  await page.goto('/');

  // Check if the page title contains "Hotspot"
  await expect(page).toHaveTitle(/Hotspot/i);

  // Verify the main content is visible
  await expect(page.locator('body')).toBeVisible();
});

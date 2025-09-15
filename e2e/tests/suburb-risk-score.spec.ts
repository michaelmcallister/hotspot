import { test, expect } from '@playwright/test';

test.describe('As a rider, I want to see an aggregate theft risk score for each suburb so I can quickly identify the least risky suburbs to park in for my specific circumstance', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/top-suburbs');
  });

  test('Riders must be able to sort suburbs risk score', async ({ page }) => {
    // Verify risk scores are visible
    const scores = await page.locator('td:last-child').allTextContents();
    expect(scores.length).toBeGreaterThan(0);

    // Click the Order dropdown
    await page.getByText('Descending').click();
    await page.getByText('Ascending').click();
    await page.waitForTimeout(500);

    // Change back to Descending
    await page.getByText('Ascending').click();
    await page.getByText('Descending').click();
    await page.waitForTimeout(500);
  });
});

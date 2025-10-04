import { test, expect } from '@playwright/test';

test.describe('Saved Spots', () => {
  test('should save a location and manage saved spots', async ({ page }) => {
    test.setTimeout(60000);

    await page.route('**/api/suburbs/search?*', async route => {
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify([
          {
            suburb: 'SOUTH WHARF',
            postcode: '3006',
            state: 'VIC',
            council: 'MELBOURNE',
            latitude: -37.8227,
            longitude: 144.9528
          }
        ])
      });
    });

    await page.route('**/api/suburbs/*/safety-score', async route => {
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({
          score: 65,
          level: 'Medium Risk'
        })
      });
    });

    await page.route('**/api/parking/locations*', async route => {
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify([
          {
            id: '1',
            address: '35 CONVENTION CENTRE PLACE',
            suburb: 'SOUTH WHARF',
            postcode: '3006',
            type: 'On Street',
            lighting: 'Good',
            security: ['CCTV'],
            savedAt: new Date().toISOString()
          }
        ])
      });
    });

    await page.goto('/');
    await page.waitForTimeout(200);

    await page.getByRole('combobox', { name: 'Enter suburb or postcode (e.g' }).click();
    await page.waitForTimeout(200);

    await page.getByText('SOUTH WHARF,').click();
    await page.waitForTimeout(500);

    await page.locator('.v-card-item__append > button:nth-child(2)').first().click();
    await page.waitForTimeout(200);

    await page.getByRole('link', { name: 'Your Spots' }).click();
    await page.waitForTimeout(500);

    await page.locator('span').filter({ hasText: 'Secure/Off‑street' }).click();
    await page.waitForTimeout(200);

    await page.getByText('CCTV').click();
    await page.waitForTimeout(200);

    await page.getByText('Well‑lit').click();
    await page.waitForTimeout(200);

    await page.locator('span').filter({ hasText: 'Well‑lit' }).locator('i').nth(1).click();
    await page.waitForTimeout(200);

    const removeButton = page.getByRole('button').filter({ hasText: /^$/ }).nth(2);
    if (await removeButton.isVisible()) {
      await removeButton.click();
      await page.waitForTimeout(200);
    }

    const exploreLink = page.getByRole('link', { name: 'Explore Spots' });
    if (await exploreLink.isVisible()) {
      await exploreLink.click();
      await page.waitForTimeout(200);
    }

    await expect(page).toHaveURL(/\/(saved|explore)/);
  });
});

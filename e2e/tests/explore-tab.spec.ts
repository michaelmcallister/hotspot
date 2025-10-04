import { test, expect } from '@playwright/test';

test.describe('Explore Tab', () => {
  test('should navigate explore page and interact with councils data', async ({ page }) => {
    test.setTimeout(60000);
    await page.route('**/api/suburbs', async route => {
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify([
          { suburb: 'MELBOURNE', postcode: '3000', council: 'MELBOURNE', state: 'VIC', safetyScore: 45 },
          { suburb: 'RICHMOND', postcode: '3121', council: 'YARRA', state: 'VIC', safetyScore: 32 },
          { suburb: 'SOUTH YARRA', postcode: '3141', council: 'MELBOURNE', state: 'VIC', safetyScore: 67 },
          { suburb: 'CARLTON', postcode: '3053', council: 'MELBOURNE', state: 'VIC', safetyScore: 55 },
          { suburb: 'FITZROY', postcode: '3065', council: 'YARRA', state: 'VIC', safetyScore: 28 },
          { suburb: 'COLLINGWOOD', postcode: '3066', council: 'YARRA', state: 'VIC', safetyScore: 31 },
          { suburb: 'ST KILDA', postcode: '3182', council: 'PORT PHILLIP', state: 'VIC', safetyScore: 42 },
          { suburb: 'BRIGHTON', postcode: '3186', council: 'BAYSIDE', state: 'VIC', safetyScore: 85 },
          { suburb: 'PRAHRAN', postcode: '3181', council: 'STONNINGTON', state: 'VIC', safetyScore: 58 },
          { suburb: 'HAWTHORN', postcode: '3122', council: 'BOROONDARA', state: 'VIC', safetyScore: 72 },
          { suburb: 'BRUNSWICK', postcode: '3056', council: 'MORELAND', state: 'VIC', safetyScore: 48 },
          { suburb: 'FOOTSCRAY', postcode: '3011', council: 'MARIBYRNONG', state: 'VIC', safetyScore: 35 }
        ])
      });
    });

    
    await page.route('**/api/councils', async route => {
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify([
          { council: 'YARRA', averageScore: 32, incidentCount: 14, suburbCount: 3 },
          { council: 'MELBOURNE', averageScore: 56, incidentCount: 8, suburbCount: 4 },
          { council: 'PORT PHILLIP', averageScore: 42, incidentCount: 11, suburbCount: 2 },
          { council: 'BAYSIDE', averageScore: 85, incidentCount: 2, suburbCount: 3 },
          { council: 'STONNINGTON', averageScore: 58, incidentCount: 7, suburbCount: 2 },
          { council: 'BOROONDARA', averageScore: 72, incidentCount: 4, suburbCount: 5 },
          { council: 'MORELAND', averageScore: 48, incidentCount: 9, suburbCount: 3 },
          { council: 'MARIBYRNONG', averageScore: 35, incidentCount: 12, suburbCount: 2 }
        ])
      });
    });

    
    await page.route('**/api/councils/*/postcodes', async route => {
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify([
          { postcode: '3121', suburbs: ['RICHMOND', 'BURNLEY', 'CREMORNE'] },
          { postcode: '3065', suburbs: ['FITZROY'] },
          { postcode: '3066', suburbs: ['COLLINGWOOD', 'CLIFTON HILL'] }
        ])
      });
    });

    await page.goto('/');
    await page.waitForTimeout(200);

    await page.getByRole('link', { name: 'Explore' }).click();
    await page.waitForTimeout(500);

    await page.getByRole('cell', { name: 'Safety Score' }).click();
    await page.waitForTimeout(200);

    const itemsPerPageSelector = page.getByRole('combobox').filter({ hasText: '20' });
    await itemsPerPageSelector.locator('i').click();
    await page.waitForTimeout(200);

    await page.getByText('10', { exact: true }).click();
    await page.waitForTimeout(200);

    await page.locator('div').filter({ hasText: /^Suburbs$/ }).first().click();
    await page.waitForTimeout(200);

    await page.getByText('Councils', { exact: true }).click();
    await page.waitForTimeout(500);

    await page.getByRole('row', { name: /Yarra.*View Postcodes/ }).getByRole('button').click();
    await page.waitForTimeout(500);

    await page.getByRole('button', { name: 'Close' }).click();
    await page.waitForTimeout(200);

    await page.getByRole('button', { name: 'Next page' }).click();
    await page.waitForTimeout(200);

    await page.getByRole('button', { name: 'Next page' }).click();
    await page.waitForTimeout(200);

    await expect(page).toHaveURL(/\/explore/);
  });
});

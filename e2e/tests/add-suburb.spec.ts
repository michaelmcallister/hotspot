import { test, expect } from '@playwright/test';

test.describe('Add Suburb', () => {
  test('should add a parking location in Elwood', async ({ page }) => {
    test.setTimeout(60000);
    await page.route('**/api/suburbs/search?*', async route => {
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify([
          {
            suburb: 'ELWOOD',
            postcode: '3184',
            state: 'VIC',
            council: 'PORT PHILLIP',
            latitude: -37.8827,
            longitude: 144.9827
          }
        ])
      });
    });

    await page.route('**/api/addresses/search?*', async route => {
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify([
          {
            address: '123 GLEN HUNTLY ROAD, ELWOOD VIC 3184',
            latitude: -37.8827,
            longitude: 144.9827
          },
          {
            address: '123A GLEN HUNTLY ROAD, ELWOOD VIC 3184',
            latitude: -37.8828,
            longitude: 144.9828
          }
        ])
      });
    });

    await page.route('**/api/parking/add', async route => {
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({
          success: true,
          message: 'Parking location added successfully'
        })
      });
    });

    await page.route('**/api/suburbs/*/safety-score', async route => {
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({
          score: 75,
          level: 'Medium Risk'
        })
      });
    });

    await page.route('**/api/parking/locations*', async route => {
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify([])
      });
    });

    await page.goto('/');
    await page.waitForTimeout(200);

    await page.getByRole('combobox', { name: 'Enter suburb or postcode (e.g' }).click();
    await page.waitForTimeout(200);

    await page.getByText('ELWOOD,').click();
    await page.waitForTimeout(500);

    const addButton = page.getByRole('button', { name: /Add.*Location/i });
    await addButton.click();
    await page.waitForTimeout(200);

    await page.getByRole('combobox', { name: 'Address Address' }).click();
    await page.waitForTimeout(200);
    await page.getByRole('combobox', { name: 'Address Address' }).fill('123');
    await page.waitForTimeout(500);

    await page.getByText('GLEN HUNTLY ROAD, ELWOOD').first().click();
    await page.waitForTimeout(200);

    await page.getByRole('button', { name: 'Submit' }).click();
    await page.waitForTimeout(500);

    await page.getByRole('button', { name: 'Got it' }).click();
    await page.waitForTimeout(200);

    await expect(page).toHaveURL(/\/elwood/i);
  });
});

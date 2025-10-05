import { test, expect } from '@playwright/test';

test.describe('FAQ Page', () => {
  test('should interact with FAQ accordion and search', async ({ page }) => {
    test.setTimeout(30000);

    await page.goto('/');
    await page.waitForTimeout(200);

    await page.getByRole('banner').getByRole('button').click();
    await page.waitForTimeout(200);

    await page.getByRole('button', { name: 'FAQ' }).click();
    await page.waitForTimeout(500);

    await page.getByRole('button', { name: 'What is the Safety Score and' }).click();
    await page.waitForTimeout(200);

    await page.getByRole('button', { name: 'Can I contribute parking' }).click();
    await page.waitForTimeout(200);

    await page.getByRole('button', { name: 'How accurate is the parking' }).click();
    await page.waitForTimeout(200);

    const searchBox = page.getByRole('textbox', { name: /Search FAQs/i });
    await searchBox.click();
    await page.waitForTimeout(200);

    await searchBox.fill('safety');
    await page.waitForTimeout(500);

    await searchBox.clear();
    await searchBox.fill('hi zed!');
    await page.waitForTimeout(200);

    await expect(page.getByRole('textbox', { name: /Search FAQs/i })).toBeVisible();
  });
});

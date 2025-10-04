import { test, expect } from '@playwright/test';

test.describe('Contact Page', () => {
  test('should navigate to contact page through menu', async ({ page }) => {
    test.setTimeout(30000);

    await page.goto('/');
    await page.waitForTimeout(200);

    const menuButton = page.getByRole('banner').getByRole('button');
    await menuButton.click();
    await page.waitForTimeout(200);

    await page.getByRole('listitem').filter({ hasText: 'Contact' }).click();
    await page.waitForTimeout(500);

    await expect(page).toHaveURL(/\/contact/);
  });
});

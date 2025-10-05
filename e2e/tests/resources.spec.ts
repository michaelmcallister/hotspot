import { test, expect } from '@playwright/test';

test.describe('Resources Modal', () => {
  test('should open and close resources modal', async ({ page }) => {
    test.setTimeout(30000);

    await page.goto('/');
    await page.waitForTimeout(200);

    await page.getByRole('button', { name: 'Resources' }).click();
    await page.waitForTimeout(500);

    await expect(page.locator('role=dialog')).toBeVisible();

    await page.getByRole('button', { name: 'Close resources' }).click();
    await page.waitForTimeout(200);

    await expect(page.locator('role=dialog')).not.toBeVisible();
  });
});

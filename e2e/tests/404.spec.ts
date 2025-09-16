import { test, expect } from '@playwright/test';

test('404 page displays and navigates home', async ({ page }) => {
  await page.goto('/hi_zed');

  await expect(page.locator('h1')).toHaveText('404');
  await expect(page.locator('text=Page Not Found')).toBeVisible();

  await page.click('text=Go to Homepage');
  await expect(page).toHaveURL('/');
});

test('navigates to /hi_zed and shows 404', async ({ page }) => {
  await page.goto('/hi_zed');

  await expect(page.locator('h1')).toHaveText('404');
  await expect(page.locator('text=Page Not Found')).toBeVisible();
});
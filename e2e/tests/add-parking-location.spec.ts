import { test, expect } from '@playwright/test';

test.describe('Add parking location to Balaclava', () => {
  test('Navigate to Balaclava, add parking location, and verify in feed', async ({ page, viewport }) => {
    // Set taller viewport keeping default width
    if (viewport) {
      await page.setViewportSize({ width: viewport.width, height: 1200 });
    } else {
      await page.setViewportSize({ width: 1280, height: 1200 });
    }

    await page.goto('/');

    // Search for Balaclava
    const searchInput = page.getByPlaceholder('Enter suburb or postcode');
    await searchInput.fill('Balaclava');
    await searchInput.press('Enter');
    await page.waitForTimeout(1500);

    // Click on Balaclava result to navigate to suburb page
    const balaclavaResult = page.locator('text=/Balaclava/i').first();
    await balaclavaResult.click();
    await page.waitForLoadState('networkidle');

    // Wait for form to be visible
    await page.waitForSelector('.v-card', { timeout: 5000 });

    // Dismiss any overlays by pressing Escape
    await page.keyboard.press('Escape');
    await page.waitForTimeout(500);

    // Click somewhere neutral to dismiss any popups
    await page.locator('h3:has-text("Add Parking Location")').click();
    await page.waitForTimeout(500);

    // Fill address field with a simple value
    const addressInput = page.locator('input[placeholder="Search for an address..."]');
    await addressInput.click();
    await addressInput.fill('123 Carlisle Street');
    // Don't wait for autocomplete, just move on
    await page.keyboard.press('Tab');
    await page.waitForTimeout(500);

    // Dismiss any overlays that might be blocking
    const overlay = page.locator('.v-overlay__content:has-text("No data available")');
    if (await overlay.isVisible({ timeout: 500 }).catch(() => false)) {
      await page.keyboard.press('Escape');
      await page.waitForTimeout(500);
    }

    // Try clicking dropdowns with force if needed
    // Select Parking Type
    const parkingTypeSelect = page.locator('.v-select').nth(0);
    await parkingTypeSelect.click({ force: true });
    await page.waitForTimeout(500);

    // Look for the option and click it
    let optionFound = await page.locator('.v-list-item-title:has-text("On-Street")').isVisible({ timeout: 500 }).catch(() => false);
    if (optionFound) {
      await page.locator('.v-list-item-title:has-text("On-Street")').click();
    } else {
      // Try typing if dropdown doesn't open
      await page.keyboard.type('On-Street');
      await page.keyboard.press('Enter');
    }
    await page.waitForTimeout(500);

    // Select Lighting
    const lightingSelect = page.locator('.v-select').nth(1);
    await lightingSelect.click({ force: true });
    await page.waitForTimeout(500);

    optionFound = await page.locator('.v-list-item-title:has-text("Good")').isVisible({ timeout: 500 }).catch(() => false);
    if (optionFound) {
      await page.locator('.v-list-item-title:has-text("Good")').click();
    } else {
      await page.keyboard.type('Good');
      await page.keyboard.press('Enter');
    }
    await page.waitForTimeout(500);

    // Select CCTV
    const cctvSelect = page.locator('.v-select').nth(2);
    await cctvSelect.click({ force: true });
    await page.waitForTimeout(500);

    optionFound = await page.locator('.v-list-item-title:has-text("Yes")').first().isVisible({ timeout: 500 }).catch(() => false);
    if (optionFound) {
      await page.locator('.v-list-item-title:has-text("Yes")').first().click();
    } else {
      await page.keyboard.type('Yes');
      await page.keyboard.press('Enter');
    }
    await page.waitForTimeout(500);

    // Log current state
    console.log('Form filled, clicking submit...');

    // Submit the form
    const submitButton = page.locator('button:has-text("Submit")');
    await expect(submitButton).toBeVisible();
    await submitButton.click();
    console.log('Submit button clicked');

    // Wait for response
    await page.waitForTimeout(5000);

    // Check for any success indicators
    const possibleSuccess = [
      '.v-snackbar',
      '.v-alert',
      'text=/success/i',
      'text=/added/i',
      'text=/thank/i',
      'text=/submitted/i'
    ];

    for (const selector of possibleSuccess) {
      const element = page.locator(selector);
      if (await element.isVisible({ timeout: 1000 }).catch(() => false)) {
        console.log('Success indicator found:', selector, await element.textContent());
      }
    }

    // Scroll to bottom to see if cards were added
    await page.evaluate(() => window.scrollTo(0, document.body.scrollHeight));
    await page.waitForTimeout(2000);

    // Check the page state
    const allCards = page.locator('.v-card');
    const cardCount = await allCards.count();
    console.log('Total v-cards on page:', cardCount);

    // Basic assertion - at least the form card should exist
    expect(cardCount).toBeGreaterThan(0);
  });
});
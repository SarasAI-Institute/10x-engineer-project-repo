import { expect, test } from '@playwright/test';

test.describe('PromptLab integrated UI', () => {
  test('shows API status and allows prompt creation', async ({ page }) => {
    await page.goto('/');
    await expect(page.getByText('Connected', { exact: false })).toBeVisible({ timeout: 20_000 });

    const promptTitle = `E2E prompt ${Date.now()}`;
    await page.getByLabel('Title').fill(promptTitle);
    await page.getByLabel('Content').fill('Test automation: ensure prompt cards appear.');
    await page.getByPlaceholder('Add context and expected format').fill('Playwright smoke test content.');

    await page.getByRole('button', { name: 'Save prompt' }).click();
    await expect(page.getByText(promptTitle).first()).toBeVisible({ timeout: 15_000 });
    await expect(page.getByText('Prompt detail')).toBeVisible();
  });

  test('allows creating a collection via the form', async ({ page }) => {
    await page.goto('/');
    const collectionName = `E2E collection ${Date.now()}`;

    await page.getByLabel('Collection name').fill(collectionName);
    await page.getByPlaceholder('Guides for the leadership team').fill('Auto-generated collection for verification.');
    await page.getByRole('button', { name: /Create collection/ }).click();

    await expect(page.locator('p.font-semibold', { hasText: collectionName })).toBeVisible({ timeout: 15_000 });
  });
});

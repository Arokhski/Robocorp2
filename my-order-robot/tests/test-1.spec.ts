import { test, expect } from '@playwright/test';

test('test', async ({ page }) => {
  await page.goto('https://robotsparebinindustries.com/#/robot-order');
  await page.getByRole('button', { name: 'OK' }).click();
  await page.getByLabel('Head:').selectOption('1');
  await page.getByLabel('Roll-a-thor body').check();
  await page.getByPlaceholder('Enter the part number for the').click();
  await page.getByPlaceholder('Enter the part number for the').fill('1');
});
// SPDX-License-Identifier: Apache-2.0
import { expect, test } from '@playwright/test';

test('Auth page has expected home link', async ({ page }) => {
	await page.goto('/');
	await expect(page.getByRole('link', { name: 'Open Model Initiative' })).toBeVisible();
});

test('Auth page has expected sign in options', async ({ page }) => {
	await page.goto('/');
	await expect(page.getByTestId('app-bar').getByRole('button', { name: 'GitHub' })).toBeVisible();
	await expect(page.getByTestId('app-bar').getByRole('button', { name: 'Discord' })).toBeVisible();

	await expect(page.getByRole('button', { name: 'Sign In with GitHub' })).toBeVisible();
	await expect(page.getByRole('button', { name: 'Sign In with Discord' })).toBeVisible();
});

test('Auth page has expected footer links', async ({ page }) => {
	await page.goto('/');

	// TODO: Update footer icons to have better user accessible locators.
	// Get all links
	const links = page.getByRole('link');

	// Check the first link (index 1)
	const firstLink = links.nth(1);
	await expect(firstLink).toBeVisible();
	expect(await firstLink.getAttribute('href')).toBe('https://discord.gg/swYY5RVHft');

	// Check the second link (index 2)
	const secondLink = links.nth(2);
	await expect(secondLink).toBeVisible();
	expect(await secondLink.getAttribute('href')).toBe('https://github.com/Open-Model-Initiative/OMI-Data-Pipeline');
});

test('Unauthenticated user is redirect to auth page', async ({ page }) => {
	await page.goto('/admin');
	await expect(page).toHaveURL('/auth');

	await page.goto('/datasets');
	await expect(page).toHaveURL('/auth');

	await page.goto('/dco');
	await expect(page).toHaveURL('/auth');

	await page.goto('/dump');
	await expect(page).toHaveURL('/auth');

	// await page.goto('/inactive');
	// await expect(page).toHaveURL('/auth');

	await page.goto('/queue');
	await expect(page).toHaveURL('/auth');

	await page.goto('/reports');
	await expect(page).toHaveURL('/auth');
});

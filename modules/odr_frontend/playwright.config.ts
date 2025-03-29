// SPDX-License-Identifier: Apache-2.0
import type { PlaywrightTestConfig } from '@playwright/test';

const config: PlaywrightTestConfig = {
	testDir: 'tests',
	forbidOnly: !!process.env.CI,
	retries: process.env.CI ? 1 : 0,
	testMatch: /(.+\.)?(test|spec)\.[jt]s/,
	use: {
		baseURL: 'http://localhost:5173',
		headless: true
	},
	reporter: [
        ['html', { outputFolder: 'playwright-report' }],
        ['list']
    ]
};

export default config;

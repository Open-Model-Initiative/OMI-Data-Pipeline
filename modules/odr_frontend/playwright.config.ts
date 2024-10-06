import type { PlaywrightTestConfig } from '@playwright/test';

const config: PlaywrightTestConfig = {
	testDir: 'tests',
	forbidOnly: !!process.env.CI,
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

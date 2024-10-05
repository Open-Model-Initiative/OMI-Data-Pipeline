import type { PlaywrightTestConfig } from '@playwright/test';

const config: PlaywrightTestConfig = {
	testDir: 'tests',
	testMatch: /(.+\.)?(test|spec)\.[jt]s/,
	use: {
		baseURL: 'http://localhost:5173',
		headless: true
	}
};

export default config;

// SPDX-License-Identifier: Apache-2.0
import adapter from '@sveltejs/adapter-node';
import { vitePreprocess } from '@sveltejs/vite-plugin-svelte';

/** @type {import('@sveltejs/kit').Config} */
const config = {
	extensions: ['.svelte'],
	// Consult https://kit.svelte.dev/docs/integrations#preprocessors
	// for more information about preprocessors
	preprocess: [vitePreprocess()],

	vitePlugin: {
		inspector: true
	},

	kit: {
		// Use adapter-node for Docker containers
		adapter: adapter({
			out: 'build'
		})
	},
};
export default config;

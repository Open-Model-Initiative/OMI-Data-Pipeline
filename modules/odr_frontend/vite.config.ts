// SPDX-License-Identifier: Apache-2.0
import { purgeCss } from 'vite-plugin-tailwind-purgecss';
import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';


export default defineConfig({
	plugins: [sveltekit(), purgeCss()],
	server: {
		fs: {
			allow: ['/app/uploads']
		},
		allowedHosts: [process.env.AWS_HOSTNAME || 'localhost']
	}
});

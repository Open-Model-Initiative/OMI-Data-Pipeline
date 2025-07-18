// SPDX-License-Identifier: Apache-2.0
import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';
import tailwindcss from "@tailwindcss/vite";


export default defineConfig({
	plugins: [
		sveltekit(),
		tailwindcss()
	],
	server: {
		fs: {
			allow: ['/app/uploads']
		},
		allowedHosts: (() => {
			const hosts = [
				'localhost',
				'app.openmodel.foundation'
			];

			if (process.env.AWS_HOSTNAME) {
				hosts.push(process.env.AWS_HOSTNAME.toLowerCase());
			}

			return hosts;
		})()
	}
});

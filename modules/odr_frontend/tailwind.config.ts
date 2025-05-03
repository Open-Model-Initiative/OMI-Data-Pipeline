// SPDX-License-Identifier: Apache-2.0
import type { Config } from 'tailwindcss';
import forms from '@tailwindcss/forms';
import typography from '@tailwindcss/typography';

export default {
	darkMode: 'class',
	content: [
		'./src/**/*.{html,js,svelte,ts}',
		'./node_modules/@skeletonlabs/skeleton/**/*.{html,js,svelte,ts}'
	  ],
	theme: {
		extend: {}
	},
	plugins: [
		forms,
		typography
	]
} satisfies Config;

import type { CustomThemeConfig } from '@skeletonlabs/tw-plugin';

export const OMICustomTheme: CustomThemeConfig = {
	name: 'omi-custom-theme',
	properties: {
		// =~= Theme Properties =~=
		'--theme-font-family-base': `ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, 'Liberation Mono', 'Courier New', monospace`,
		'--theme-font-family-heading': `ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, 'Liberation Mono', 'Courier New', monospace`,
		'--theme-font-color-base': '0 0 0',
		'--theme-font-color-dark': '255 255 255',
		'--theme-rounded-base': '2px',
		'--theme-rounded-container': '2px',
		'--theme-border-base': '2px',
		// =~= Theme On-X Colors =~=
		'--on-primary': '255 255 255',
		'--on-secondary': '0 0 0',
		'--on-tertiary': '255 255 255',
		'--on-success': '0 0 0',
		'--on-warning': '0 0 0',
		'--on-error': '255 255 255',
		'--on-surface': '255 255 255',
		// =~= Theme Colors  =~=
		// primary | #306a82
		'--color-primary-50': '224 233 236', // #e0e9ec
		'--color-primary-100': '214 225 230', // #d6e1e6
		'--color-primary-200': '203 218 224', // #cbdae0
		'--color-primary-300': '172 195 205', // #acc3cd
		'--color-primary-400': '110 151 168', // #6e97a8
		'--color-primary-500': '48 106 130', // #306a82
		'--color-primary-600': '43 95 117', // #2b5f75
		'--color-primary-700': '36 80 98', // #245062
		'--color-primary-800': '29 64 78', // #1d404e
		'--color-primary-900': '24 52 64', // #183440
		// secondary | #28c3a4
		'--color-secondary-50': '223 246 241', // #dff6f1
		'--color-secondary-100': '212 243 237', // #d4f3ed
		'--color-secondary-200': '201 240 232', // #c9f0e8
		'--color-secondary-300': '169 231 219', // #a9e7db
		'--color-secondary-400': '105 213 191', // #69d5bf
		'--color-secondary-500': '40 195 164', // #28c3a4
		'--color-secondary-600': '36 176 148', // #24b094
		'--color-secondary-700': '30 146 123', // #1e927b
		'--color-secondary-800': '24 117 98', // #187562
		'--color-secondary-900': '20 96 80', // #146050
		// tertiary | #981f6c
		'--color-tertiary-50': '240 221 233', // #f0dde9
		'--color-tertiary-100': '234 210 226', // #ead2e2
		'--color-tertiary-200': '229 199 218', // #e5c7da
		'--color-tertiary-300': '214 165 196', // #d6a5c4
		'--color-tertiary-400': '183 98 152', // #b76298
		'--color-tertiary-500': '152 31 108', // #981f6c
		'--color-tertiary-600': '137 28 97', // #891c61
		'--color-tertiary-700': '114 23 81', // #721751
		'--color-tertiary-800': '91 19 65', // #5b1341
		'--color-tertiary-900': '74 15 53', // #4a0f35
		// success | #1dd33b
		'--color-success-50': '221 248 226', // #ddf8e2
		'--color-success-100': '210 246 216', // #d2f6d8
		'--color-success-200': '199 244 206', // #c7f4ce
		'--color-success-300': '165 237 177', // #a5edb1
		'--color-success-400': '97 224 118', // #61e076
		'--color-success-500': '29 211 59', // #1dd33b
		'--color-success-600': '26 190 53', // #1abe35
		'--color-success-700': '22 158 44', // #169e2c
		'--color-success-800': '17 127 35', // #117f23
		'--color-success-900': '14 103 29', // #0e671d
		// warning | #d3ab1d
		'--color-warning-50': '248 242 221', // #f8f2dd
		'--color-warning-100': '246 238 210', // #f6eed2
		'--color-warning-200': '244 234 199', // #f4eac7
		'--color-warning-300': '237 221 165', // #eddda5
		'--color-warning-400': '224 196 97', // #e0c461
		'--color-warning-500': '211 171 29', // #d3ab1d
		'--color-warning-600': '190 154 26', // #be9a1a
		'--color-warning-700': '158 128 22', // #9e8016
		'--color-warning-800': '127 103 17', // #7f6711
		'--color-warning-900': '103 84 14', // #67540e
		// error | #d3411d
		'--color-error-50': '248 227 221', // #f8e3dd
		'--color-error-100': '246 217 210', // #f6d9d2
		'--color-error-200': '244 208 199', // #f4d0c7
		'--color-error-300': '237 179 165', // #edb3a5
		'--color-error-400': '224 122 97', // #e07a61
		'--color-error-500': '211 65 29', // #d3411d
		'--color-error-600': '190 59 26', // #be3b1a
		'--color-error-700': '158 49 22', // #9e3116
		'--color-error-800': '127 39 17', // #7f2711
		'--color-error-900': '103 32 14', // #67200e
		// surface | #1e2d33
		'--color-surface-50': '221 224 224', // #dde0e0
		'--color-surface-100': '210 213 214', // #d2d5d6
		'--color-surface-200': '199 203 204', // #c7cbcc
		'--color-surface-300': '165 171 173', // #a5abad
		'--color-surface-400': '98 108 112', // #626c70
		'--color-surface-500': '30 45 51', // #1e2d33
		'--color-surface-600': '27 41 46', // #1b292e
		'--color-surface-700': '23 34 38', // #172226
		'--color-surface-800': '18 27 31', // #121b1f
		'--color-surface-900': '15 22 25' // #0f1619
	}
};

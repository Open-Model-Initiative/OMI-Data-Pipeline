// SPDX-License-Identifier: Apache-2.0
import * as dotenv from 'dotenv';

dotenv.config();

function getEnvironmentVariable(environmentVariable: string, required: boolean = true): string {
	const validEnvironmentVariable = process.env[environmentVariable];
	if (!validEnvironmentVariable && required) {
		// During build time, some variables might not be available
		// Check if we're in build mode
		if (process.env.NODE_ENV === 'build') {
			console.warn(`Warning: Environment variable ${environmentVariable} not available during build`);
			return '';
		}
		throw new Error(`Couldn't find environment variable: ${environmentVariable}`);
	}
	return validEnvironmentVariable || '';
}

// All these variables are required at runtime but not at build time
export const ENV = {
	PUBLIC_API_BASE_URL: getEnvironmentVariable('PUBLIC_API_BASE_URL', process.env.NODE_ENV !== 'build'),
	API_SERVICE_URL: getEnvironmentVariable('API_SERVICE_URL', process.env.NODE_ENV !== 'build')
};

export const API_URL = ENV.API_SERVICE_URL || ENV.PUBLIC_API_BASE_URL;

// All these variables are required at runtime but not at build time
export const AUTH_SECRET = getEnvironmentVariable('AUTH_SECRET', process.env.NODE_ENV !== 'build');
export const GITHUB_CLIENT_ID = getEnvironmentVariable('GITHUB_CLIENT_ID', process.env.NODE_ENV !== 'build');
export const GITHUB_CLIENT_SECRET = getEnvironmentVariable('GITHUB_CLIENT_SECRET', process.env.NODE_ENV !== 'build');
export const DISCORD_CLIENT_ID = getEnvironmentVariable('DISCORD_CLIENT_ID', process.env.NODE_ENV !== 'build');
export const DISCORD_CLIENT_SECRET = getEnvironmentVariable('DISCORD_CLIENT_SECRET', process.env.NODE_ENV !== 'build');
export const POSTGRES_HOST = getEnvironmentVariable('POSTGRES_HOST', process.env.NODE_ENV !== 'build');
export const POSTGRES_PORT = getEnvironmentVariable('POSTGRES_PORT', process.env.NODE_ENV !== 'build');
export const POSTGRES_USER = getEnvironmentVariable('POSTGRES_USER', process.env.NODE_ENV !== 'build');
export const POSTGRES_PASSWORD = getEnvironmentVariable('POSTGRES_PASSWORD', process.env.NODE_ENV !== 'build');
export const POSTGRES_DB = getEnvironmentVariable('POSTGRES_DB', process.env.NODE_ENV !== 'build');

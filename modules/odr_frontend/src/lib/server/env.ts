// SPDX-License-Identifier: Apache-2.0
import * as dotenv from 'dotenv';

dotenv.config();

function getEnvironmentVariable(environmentVariable: string): string {
	const validEnvironmentVariable = process.env[environmentVariable];
	if (!validEnvironmentVariable) {
		throw new Error(`Couldn't find environment variable: ${environmentVariable}`);
	}
	return validEnvironmentVariable;
}

export const ENV = {
	PUBLIC_API_BASE_URL: getEnvironmentVariable('PUBLIC_API_BASE_URL'),
	API_SERVICE_URL: getEnvironmentVariable('API_SERVICE_URL')
};

export const API_URL = ENV.API_SERVICE_URL || ENV.PUBLIC_API_BASE_URL;
export const AUTH_SECRET = getEnvironmentVariable('AUTH_SECRET');
export const GITHUB_CLIENT_ID = getEnvironmentVariable('GITHUB_CLIENT_ID');
export const GITHUB_CLIENT_SECRET = getEnvironmentVariable('GITHUB_CLIENT_SECRET');
export const DISCORD_CLIENT_ID = getEnvironmentVariable('DISCORD_CLIENT_ID');
export const DISCORD_CLIENT_SECRET = getEnvironmentVariable('DISCORD_CLIENT_SECRET');
export const POSTGRES_HOST = getEnvironmentVariable('POSTGRES_HOST');
export const POSTGRES_PORT = getEnvironmentVariable('POSTGRES_PORT');
export const POSTGRES_USER = getEnvironmentVariable('POSTGRES_USER');
export const POSTGRES_PASSWORD = getEnvironmentVariable('POSTGRES_PASSWORD');
export const POSTGRES_DB = getEnvironmentVariable('POSTGRES_DB');

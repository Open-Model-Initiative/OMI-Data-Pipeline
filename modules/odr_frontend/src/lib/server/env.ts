import * as dotenv from "dotenv";
dotenv.config();

function getEnvironmentVariable(environmentVariable: string): string {
  const validEnvironmentVariable = process.env[environmentVariable];
  if (!validEnvironmentVariable) {
    throw new Error(`Couldn't find environment variable: ${environmentVariable}`);
  }
  return validEnvironmentVariable;
}

export const ENV = {
  PUBLIC_API_BASE_URL: getEnvironmentVariable("PUBLIC_API_BASE_URL"),
  API_SERVICE_URL: getEnvironmentVariable("API_SERVICE_URL"),
};

export const API_URL = ENV.API_SERVICE_URL || ENV.PUBLIC_API_BASE_URL;

console.log("Environment variables:", ENV);
console.log("Using API URL:", API_URL);

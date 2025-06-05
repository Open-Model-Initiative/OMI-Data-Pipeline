// SPDX-License-Identifier: Apache-2.0
/**
 * Constants related to JSONL file uploads
 */

export const ACCEPTED_FILE_TYPES = {
  JSONL: '.jsonl'
};

export const UPLOAD_STATUSES = {
  IDLE: '',
  UPLOADING: 'uploading',
  SUCCESS: 'success',
  ERROR: 'error'
};

export const UPLOAD_MESSAGES = {
  UPLOADING: (filename: string) => `Uploading ${filename}...`,
  SUCCESS_ALL: 'All files uploaded successfully',
  SUCCESS_WITH_ERRORS: (errorCount: number) =>
    `Uploaded with ${errorCount} error${errorCount > 1 ? 's' : ''}`,
  SUCCESS_FILE: (filename: string, contentCount: number) =>
    `${filename} uploaded successfully. Created ${contentCount} content record(s) with annotations.`,
  INVALID_TYPE: (filename: string) => `Invalid file type: ${filename}`,
  ERROR_UNKNOWN: (filename: string) => `Error uploading ${filename}: Unknown error`,
  ERROR_RESPONSE: (filename: string, message: string) =>
    `Failed to upload ${filename}: ${message || 'Unknown error'}`,
  ERROR_UNEXPECTED: (filename: string) =>
    `Failed to upload ${filename}: Unexpected response type`
};

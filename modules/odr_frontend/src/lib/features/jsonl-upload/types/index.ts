// SPDX-License-Identifier: Apache-2.0
/**
 * Types related to JSONL file uploads
 */

export interface User {
  id: string;
  [key: string]: any;
}

export interface UploadResponse {
  type: string;
  data: string;
}

export interface ParsedUploadResult {
  isSuccess: boolean;
  message: string;
  contentCount?: number;
}

export type UploadStatus = 'idle' | 'uploading' | 'success' | 'error';

export interface UploadError {
  message: string;
  file?: string;
}

export interface UploadState {
  status: UploadStatus;
  progress: number;
  message: string;
  errors: UploadError[];
  selectedFiles: File[];
}

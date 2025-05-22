// SPDX-License-Identifier: Apache-2.0
/**
 * Types related to file uploads
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

// Supporting Types
type AnyString = string & {};
type FileError = "TOO_MANY_FILES" | "FILE_INVALID_TYPE" | "FILE_TOO_LARGE" | "FILE_TOO_SMALL" | "FILE_INVALID" | "FILE_EXISTS" | AnyString;

export interface FileRejection {
  file: File;
  errors: FileError[];
}

export interface FileChangeDetails {
  acceptedFiles: File[];
  rejectedFiles: FileRejection[];
}

export interface FileRejectDetails {
  files: FileRejection[];
}

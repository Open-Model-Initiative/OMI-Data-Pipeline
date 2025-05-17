// SPDX-License-Identifier: Apache-2.0
/**
 * Store for managing JSONL file upload state
 */
import { writable } from 'svelte/store';
import type { UploadState, UploadError, User, ParsedUploadResult } from '../types';
import { ACCEPTED_FILE_TYPES, UPLOAD_MESSAGES, UPLOAD_STATUSES } from '../constants';

// Initial state
const initialState: UploadState = {
  status: 'idle',
  progress: 0,
  message: '',
  errors: [],
  selectedFiles: []
};

function createUploadStore() {
  const { subscribe, set, update } = writable<UploadState>(initialState);

  return {
    subscribe,
    reset: () => set(initialState),

    setFiles: (files: FileList | null) => {
      if (!files) {
        update(state => ({ ...state, selectedFiles: [] }));
        return;
      }

      update(state => ({
        ...state,
        selectedFiles: Array.from(files),
        errors: []
      }));
    },

    uploadFiles: async (user: User) => {
      update(state => ({
        ...state,
        status: 'uploading',
        progress: 0,
        errors: [],
        message: ''
      }));

      const { selectedFiles } = get({ subscribe });
      const totalFiles = selectedFiles.length;
      let completedUploads = 0;
      const errors: UploadError[] = [];

      for (const file of selectedFiles) {
        if (!ACCEPTED_FILE_TYPES.JSONL.endsWith(file.name.slice(file.name.lastIndexOf('.')))) {
          errors.push({
            file: file.name,
            message: UPLOAD_MESSAGES.INVALID_TYPE(file.name)
          });
          continue;
        }

        update(state => ({
          ...state,
          message: UPLOAD_MESSAGES.UPLOADING(file.name)
        }));

        try {
          const result = await uploadFile(file, user);

          if (result.isSuccess) {
            update(state => ({
              ...state,
              message: UPLOAD_MESSAGES.SUCCESS_FILE(file.name, result.contentCount || 0)
            }));
          } else {
            errors.push({
              file: file.name,
              message: UPLOAD_MESSAGES.ERROR_RESPONSE(file.name, result.message)
            });
          }
        } catch (error) {
          console.error('Error uploading file:', error);
          const errorMessage = error instanceof Error
            ? error.message
            : UPLOAD_MESSAGES.ERROR_UNKNOWN(file.name);

          errors.push({ file: file.name, message: errorMessage });
        }

        completedUploads++;
        const progress = Math.round((completedUploads / totalFiles) * 100);

        update(state => ({ ...state, progress }));
      }

      // Update final status
      update(state => {
        const status = errors.length === totalFiles ? 'error' : 'success';
        const message = errors.length === 0
          ? UPLOAD_MESSAGES.SUCCESS_ALL
          : UPLOAD_MESSAGES.SUCCESS_WITH_ERRORS(errors.length);

        return {
          ...state,
          status,
          message,
          errors,
          selectedFiles: [] // Clear selected files after upload
        };
      });
    }
  };
}

// Helper function to get store value
function get(store: { subscribe: any }) {
  let value: any;
  store.subscribe(($value: any) => { value = $value; })();
  return value;
}

// Helper function to upload a single file
async function uploadFile(file: File, user: User): Promise<ParsedUploadResult> {
  const formData = new FormData();
  formData.append('file', file);
  formData.append('userId', user?.id ?? '');

  const response = await fetch('?/uploadJSONL', {
    method: 'POST',
    body: formData
  });

  if (!response.ok) {
    return {
      isSuccess: false,
      message: response.statusText || 'Unknown error'
    };
  }

  const result = await response.json();

  if (result.type !== 'success') {
    return {
      isSuccess: false,
      message: UPLOAD_MESSAGES.ERROR_UNEXPECTED(file.name)
    };
  }

  const data = JSON.parse(result.data);
  return {
    isSuccess: data[1],
    message: data[2],
    contentCount: data[3]?.contentCount || 0
  };
}

export const uploadStore = createUploadStore();

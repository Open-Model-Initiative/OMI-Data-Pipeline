// SPDX-License-Identifier: Apache-2.0
import { readdir, readFile, rename } from 'fs/promises';
import { join } from 'path';
import type { PageServerLoad } from './$types';
import { error } from '@sveltejs/kit';

import { PG_API } from '$lib/server/pg';

const UPLOAD_DIR = process.env.UPLOAD_DIR || './uploads';
const PENDING_DIR = join(UPLOAD_DIR, 'pending');
const ACCEPTED_DIR = join(UPLOAD_DIR, 'accepted');
const REJECTED_DIR = join(UPLOAD_DIR, 'rejected');
const ITEMS_PER_PAGE = 10;


interface ImageData {
  filename: string;
  previewUrl: string;
  metadata: {
    uploadedByUser: string;
    hdrStats: any;
    metadata: any;
  };
}

export const load: PageServerLoad = async ({ url }) => {
  const page = Number(url.searchParams.get('page')) || 1;
  const files = await readdir(PENDING_DIR);

  const imageFiles = files.filter(file => file.endsWith('.jpg'));
  const totalPages = Math.ceil(imageFiles.length / ITEMS_PER_PAGE);

  const startIndex = (page - 1) * ITEMS_PER_PAGE;
  const endIndex = startIndex + ITEMS_PER_PAGE;
  const pageImageFiles = imageFiles.slice(startIndex, endIndex);

  const users = await PG_API.users.getAll();

  const imagesData: ImageData[] = await Promise.all(
    pageImageFiles.map(async (filename) => {
      const jsonFilename = filename.replace('.jpg', '.json');
      const jsonPath = join(PENDING_DIR, jsonFilename);
      const metadata = JSON.parse(await readFile(jsonPath, 'utf-8'));

      const user = users.find(u => u.id === parseInt(metadata.uploadedByUser));

      return {
        filename,
        previewUrl: `/uploads/pending/${filename}`,
        metadata: {
          ...metadata,
          uploadedByUser: user ? user.email : metadata.uploadedByUser
        },
      };
    })
  );

  return {
    images: imagesData,
    currentPage: page,
    totalPages,
  };
};

export const actions = {
    accept: async ({ request }) => {
      const formData = await request.formData();
      const filename = formData.get('filename');
      if (typeof filename !== 'string') {
        throw error(400, 'Invalid filename');
      }
      await moveFile(filename, ACCEPTED_DIR);
      return { success: true };
    },

    reject: async ({ request }) => {
      const formData = await request.formData();
      const filename = formData.get('filename');
      if (typeof filename !== 'string') {
        throw error(400, 'Invalid filename');
      }
      await moveFile(filename, REJECTED_DIR);
      return { success: true };
    }
  };

  async function moveFile(filename: string, destDir: string) {
    const sourcePath = join(PENDING_DIR, filename);
    const destPath = join(destDir, filename);
    await rename(sourcePath, destPath);

    // Move the associated JSON file
    const jsonFilename = filename.replace('.jpg', '.json');
    const jsonSourcePath = join(PENDING_DIR, jsonFilename);
    const jsonDestPath = join(destDir, jsonFilename);
    await rename(jsonSourcePath, jsonDestPath);

    // Move the associated DNG file
    const dngFilename = filename.replace('.jpg', '.dng');
    const dngSourcePath = join(PENDING_DIR, dngFilename);
    const dngDestPath = join(destDir, dngFilename);
    await rename(dngSourcePath, dngDestPath);
  }

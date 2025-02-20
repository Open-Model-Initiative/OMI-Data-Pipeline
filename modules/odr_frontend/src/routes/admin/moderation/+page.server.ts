// SPDX-License-Identifier: Apache-2.0
import { readdir, readFile, rename } from 'fs/promises';
import { join } from 'path';
import type { PageServerLoad } from './$types';
import { error } from '@sveltejs/kit';

import { S3Client, ListObjectsV2Command, GetObjectCommand, CopyObjectCommand, DeleteObjectCommand } from "@aws-sdk/client-s3";

import { PG_API } from '$lib/server/pg';

const UPLOAD_DIR = process.env.UPLOAD_DIR || './uploads';
const PENDING_DIR = join(UPLOAD_DIR, 'pending');
const ACCEPTED_DIR = join(UPLOAD_DIR, 'accepted');
const REJECTED_DIR = join(UPLOAD_DIR, 'rejected');
const ITEMS_PER_PAGE = 10;

let s3Client: S3Client | null = null;

if (process.env.AWS_S3_ENABLED === 'true') {
  s3Client = new S3Client();
} else {
  console.warn('AWS S3 is not enabled');
}

const S3_BUCKET_NAME = process.env.S3_BUCKET_NAME;

async function getS3Objects(prefix: string) {
  if (!s3Client) {
    throw new Error('S3 client is not initialized');
  }

  const command = new ListObjectsV2Command({
    Bucket: S3_BUCKET_NAME,
    Prefix: prefix,
  });
  const response = await s3Client.send(command);
  return response.Contents || [];
}

async function getS3ObjectContent(key: string) {
  if (!s3Client) {
    throw new Error('S3 client is not initialized');
  }

  const command = new GetObjectCommand({
    Bucket: S3_BUCKET_NAME,
    Key: key,
  });
  const response = await s3Client.send(command);
  return response.Body?.transformToString();
}


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
  const users = await PG_API.users.getAll();

  let imageFiles: string[];
  let totalPages: number;
  let imagesData: ImageData[];

  if (process.env.NODE_ENV === 'production') {
    // S3 logic
    const s3Objects = await getS3Objects('pending/');
    imageFiles = s3Objects
    .map(obj => obj.Key)
    .filter((key): key is string => key !== undefined && key.endsWith('.jpg'));
    totalPages = Math.ceil(imageFiles.length / ITEMS_PER_PAGE);

    const startIndex = (page - 1) * ITEMS_PER_PAGE;
    const endIndex = startIndex + ITEMS_PER_PAGE;
    const pageImageFiles = imageFiles.slice(startIndex, endIndex);

    imagesData = await Promise.all(
      pageImageFiles.map(async (filename) => {
        const jsonFilename = filename.replace('.jpg', '.json');
        const content = await getS3ObjectContent(jsonFilename);

        if (content === undefined) {
          throw new Error(`Failed to retrieve content for ${jsonFilename}`);
        }

        const metadata = JSON.parse(content);

        const user = users.find(u => u.id === parseInt(metadata.uploadedByUser));

        return {
          filename,
          previewUrl: `https://${S3_BUCKET_NAME}.s3.amazonaws.com/${filename}`,
          metadata: {
            ...metadata,
            uploadedByUser: user ? user.email : metadata.uploadedByUser
          },
        };
      })
    );

    console.log(`Grabbed image data from S3`);
  } else {
    // Local file system logic
    const files = await readdir(PENDING_DIR);
    imageFiles = files.filter(file => file.endsWith('.jpg'));
    totalPages = Math.ceil(imageFiles.length / ITEMS_PER_PAGE);

    const startIndex = (page - 1) * ITEMS_PER_PAGE;
    const endIndex = startIndex + ITEMS_PER_PAGE;
    const pageImageFiles = imageFiles.slice(startIndex, endIndex);

    imagesData = await Promise.all(
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
  }

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
      await moveFile(filename, 'accepted');
      return { success: true };
    },

    reject: async ({ request }) => {
      const formData = await request.formData();
      const filename = formData.get('filename');
      if (typeof filename !== 'string') {
        throw error(400, 'Invalid filename');
      }
      await moveFile(filename, 'rejected');
      return { success: true };
    }
  };

  async function moveFile(filename: string, destFolder: string) {
    if (process.env.NODE_ENV === 'production') {
      // S3 move logic
      if (!s3Client) {
        throw new Error('S3 client is not initialized');
      }

      const sourceKey = `pending/${filename}`;
      const destKey = `${destFolder}/${filename}`;

      const fileExtensions = ['jpg', 'json', 'dng'];

      await Promise.all(fileExtensions.map(async (ext) => {
        const sourceKeyExt = sourceKey.replace(/\.[^.]+$/, `.${ext}`);
        const destKeyExt = destKey.replace(/\.[^.]+$/, `.${ext}`);

        await s3Client.send(new CopyObjectCommand({
          Bucket: S3_BUCKET_NAME,
          CopySource: `${S3_BUCKET_NAME}/${sourceKeyExt}`,
          Key: destKeyExt,
        }));

        await s3Client.send(new DeleteObjectCommand({
          Bucket: S3_BUCKET_NAME,
          Key: sourceKeyExt,
        }));
      }));
    } else {
      // Local file system move logic
      const sourcePath = join(PENDING_DIR, filename);
      const destPath = join(destFolder === 'accepted' ? ACCEPTED_DIR : REJECTED_DIR, filename);
      await rename(sourcePath, destPath);

      // Move associated JSON and DNG files
      ['json', 'dng'].forEach(async (ext) => {
        const sourcePathExt = sourcePath.replace('.jpg', `.${ext}`);
        const destPathExt = destPath.replace('.jpg', `.${ext}`);
        await rename(sourcePathExt, destPathExt);
      });
    }
  }

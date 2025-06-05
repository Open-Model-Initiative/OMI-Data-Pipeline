// SPDX-License-Identifier: Apache-2.0
import { redirect } from '@sveltejs/kit';
import type { RequestEvent } from '@sveltejs/kit';
import { PG_API } from '$lib/server/pg';

import fs from 'fs';
import { join } from 'path';
import { S3Client, PutObjectCommand } from "@aws-sdk/client-s3";
import { writeFile, mkdir } from 'fs/promises';

const UPLOAD_DIR = join(process.cwd(), 'uploads');
export const PENDING_DIR = join(UPLOAD_DIR, 'pending');
const REJECTED_DIR = join(UPLOAD_DIR, 'rejected');
const FLAGGED_DIR = join(UPLOAD_DIR, 'flagged');
export const JSONL_DIR = join(UPLOAD_DIR, 'jsonl');

export async function handlePageLoad(event: RequestEvent) {
  const session = await event.locals.auth();
  if (!session?.user) throw redirect(303, '/auth');

  const featureToggles = await PG_API.featureToggles.getAll();
  const featureToggleMap = Object.fromEntries(
    featureToggles.map(toggle => [toggle.feature_name, toggle.is_enabled])
  );

  return {
    featureToggles: featureToggleMap
  };
}

export function setupS3Client() {
  if (process.env.AWS_S3_ENABLED === 'true') {
    return new S3Client();
  } else {
    console.warn('AWS S3 is not enabled');
    return null
  }
}

export function setupLocalDirectories() {
  if (process.env.NODE_ENV !== 'production' || !process.env.AWS_S3_BUCKET) {
    if (!fs.existsSync(UPLOAD_DIR)) {
        fs.mkdirSync(UPLOAD_DIR, { recursive: true });
    }
    if (!fs.existsSync(PENDING_DIR)) {
        fs.mkdirSync(PENDING_DIR, { recursive: true });
    }
    if (!fs.existsSync(REJECTED_DIR)) {
        fs.mkdirSync(REJECTED_DIR, { recursive: true });
    }
    if (!fs.existsSync(FLAGGED_DIR)) {
        fs.mkdirSync(FLAGGED_DIR, { recursive: true });
    }
    if (!fs.existsSync(JSONL_DIR)) {
        fs.mkdirSync(JSONL_DIR, { recursive: true });
    }
  }
}

export function handleFileUpload(file: File, timestamp: string, userId: string): { uniqueFileName: string, fileExtension: string } {
  if (!(file instanceof File)) {
    throw new Error('No file uploaded')
  }

  if (!userId || typeof userId !== 'string') {
    throw new Error('No user ID provided')
  }

  const originalFilename = file.name;
  const fileExtension = originalFilename.split('.').pop() ?? '';
  const uniqueFileName = `${userId}_${timestamp}.${fileExtension}`;

  return { uniqueFileName, fileExtension };
}

export async function uploadToS3(s3Client: S3Client | null, key: string, body: Buffer | string) {
  if (!s3Client) {
    throw new Error('S3 client is not initialized');
  }

  await s3Client.send(new PutObjectCommand({
    Bucket: process.env.S3_BUCKET_NAME,
    Key: key,
    Body: body,
  }));

  console.log(`File uploaded to S3: ${key}`);
}

export async function saveFileLocally(directory: string, fileName: string, content: Buffer | ArrayBuffer | string) {
  await mkdir(directory, { recursive: true });
  const filePath = join(directory, fileName);
  if (Buffer.isBuffer(content) || content instanceof ArrayBuffer) {
    await writeFile(filePath, new Uint8Array(content));
  } else {
    await writeFile(filePath, content);
  }

  console.log(`File saved locally: ${filePath}`);
}

export async function getFormData(request: Request) {
  const formData = await request.formData();
  const file = formData.get('file') as File;
  const userId = formData.get('userId') as string;

  return { file, userId }
}

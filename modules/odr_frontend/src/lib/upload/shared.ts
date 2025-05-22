// SPDX-License-Identifier: Apache-2.0
import { join } from 'path';
import { S3Client, PutObjectCommand } from "@aws-sdk/client-s3";
import { writeFile, mkdir } from 'fs/promises';

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

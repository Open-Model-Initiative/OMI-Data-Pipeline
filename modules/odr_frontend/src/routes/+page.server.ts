// SPDX-License-Identifier: Apache-2.0
import { redirect, type RequestEvent } from '@sveltejs/kit';
import type { PageServerLoad } from './$types';
import { PG_API } from '$lib/server/pg';
import { writeFile, mkdir } from 'fs/promises';
import { join } from 'path';

import { S3Client, PutObjectCommand } from "@aws-sdk/client-s3";

export const load: PageServerLoad = async (event) => {
	const session = await event.locals.auth();
	if (!session?.user) throw redirect(303, '/auth');

	const featureToggles = await PG_API.featureToggles.getAll();

	const featureToggleMap = Object.fromEntries(
		featureToggles.map(toggle => [toggle.feature_name, toggle.is_enabled])
	);

	return {
		featureToggles: featureToggleMap
	};
};

const UPLOAD_DIR = process.env.UPLOAD_DIR ?? './uploads';
const PENDING_DIR = join(UPLOAD_DIR, 'pending');
const ACCEPTED_DIR = join(UPLOAD_DIR, 'accepted');
const REJECTED_DIR = join(UPLOAD_DIR, 'rejected');
const FLAGGED_DIR = join(UPLOAD_DIR, 'flagged');
const JSONL_DIR = join(UPLOAD_DIR, 'jsonl');
const API_BASE_URL = process.env.API_SERVICE_URL ?? 'http://odr-api:31100/api/v1';

let s3Client: S3Client | null = null;

if (process.env.AWS_S3_ENABLED === 'true') {
  s3Client = new S3Client();
} else {
  console.warn('AWS S3 is not enabled');
}

async function makeImageApiCall(endpoint: string, file: Blob, filename: string) {
	const formData = new FormData();
    formData.append('file', file, filename);

	try {
        const response = await fetch(`${API_BASE_URL}${endpoint}`, {
            method: 'POST',
            body: formData,
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        return await response.json();
    } catch (error) {
        console.error(`Error calling ${endpoint}:`, error);
        throw new Error(`API error (${endpoint}): ${error instanceof Error ? error.message : String(error)}`);
    }
}

async function makeJsonApiCall(endpoint: string, data: any) {
    console.log(`Sending data to ${endpoint}:`, JSON.stringify(data, null, 2));

	try {
        const response = await fetch(`${API_BASE_URL}${endpoint}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        return await response.json();
    } catch (error) {
        console.error(`Error calling ${endpoint}:`, error);
        throw new Error(`API error (${endpoint}): ${error instanceof Error ? error.message : String(error)}`);
    }
}

export const actions = {
	uploadHDR: async ({ request }: RequestEvent) => {
		const formData = await request.formData();
		const file = formData.get('file');
		const userId = formData.get('userId');

		if (!(file instanceof Blob)) {
			return { success: false, error: 'No file uploaded' };
		}

		if (!userId || typeof userId !== 'string') {
			return { success: false, error: 'No user ID provided' };
		}

		try {
			const originalFilename = file.name;
			const fileExtension = originalFilename.split('.').pop();
			const timestamp = new Date().toISOString().replace(/[-:.]/g, '');
			const uniqueFileName = `${userId}_${timestamp}.${fileExtension}`;

			// Clean metadata
			const cleanedData = await makeImageApiCall('/image/clean-metadata', file, uniqueFileName);
			const cleaned_image_base64 = cleanedData.cleaned_image

			// Convert base64 to Blob
			const byteCharacters = atob(cleaned_image_base64);
			const byteNumbers = new Array(byteCharacters.length);
			for (let i = 0; i < byteCharacters.length; i++) {
			  byteNumbers[i] = byteCharacters.charCodeAt(i);
			}
			const byteArray = new Uint8Array(byteNumbers);
			const cleanedBlob = new Blob([byteArray], { type: 'application/octet-stream' });

			const cleanedBuffer = Buffer.from(byteArray);

			// Calculate HDR stats and metadata
			const statsData = await makeImageApiCall('/image/hdr-stats', cleanedBlob, uniqueFileName);
			const metadataData = await makeImageApiCall('/image/metadata', cleanedBlob, uniqueFileName);

			// Create JPG preview
			const jpgData = await makeImageApiCall('/image/jpg-preview', cleanedBlob, uniqueFileName);
			const jpgBuffer = Buffer.from(jpgData.jpg_preview, 'base64');
			const jpgFileName = `${userId}_${timestamp}.jpg`

			// Combine metadata for temporary file storage
			const metadataContent = JSON.stringify({
				uploadedByUser: userId,
				hdrStats: statsData,
				metadata: metadataData
			}, null, 2);
			const metadataFileName = `${userId}_${timestamp}.json`

			if (process.env.NODE_ENV === 'production') {
			  	// S3 upload for production
				if (!s3Client) {
					throw new Error('S3 client is not initialized');
				}

				await s3Client.send(new PutObjectCommand({
					Bucket: process.env.S3_BUCKET_NAME,
					Key: uniqueFileName,
					Body: cleanedBuffer,
				}));

				await s3Client.send(new PutObjectCommand({
					Bucket: process.env.S3_BUCKET_NAME,
					Key: jpgFileName,
					Body: jpgBuffer,
				}));

				await s3Client.send(new PutObjectCommand({
					Bucket: process.env.S3_BUCKET_NAME,
					Key: metadataFileName,
					Body: metadataContent,
				}));

				console.log(`HDR Image uploaded to S3: ${uniqueFileName}`);
			} else {
				// Local file system for development
				await mkdir(PENDING_DIR, { recursive: true });
				await mkdir(ACCEPTED_DIR, { recursive: true });
				await mkdir(REJECTED_DIR, { recursive: true });
				await mkdir(FLAGGED_DIR, { recursive: true });

				const cleanedFilePath = join(PENDING_DIR, uniqueFileName);
				await writeFile(cleanedFilePath, new Uint8Array(cleanedBuffer));

				const jpgFilePath = join(PENDING_DIR, jpgFileName);
				await writeFile(jpgFilePath, new Uint8Array(jpgBuffer));

				const metadataFilePath = join(PENDING_DIR, metadataFileName);
				await writeFile(metadataFilePath, metadataContent);
			}

			const contentData = {
                name: uniqueFileName,
                type: "image",
                hash: "", // Needs calculated elsewhere
                phash: "", // Needs calculated elsewhere
                width: metadataData.width || 0,
                height: metadataData.height || 0,
                url: [], // S3 URL?
                format: fileExtension,
                size: file.size,
                status: "pending",
                license: "CDLA-Permissive-2.0",
                license_url: "https://cdla.dev/permissive-2-0/",
                flags: 0,
                meta: metadataData,
                content_authors: [],
                sources: []
            };

			const from_user_id = Number(userId) || 0
            await makeJsonApiCall(`/content/?from_user_id=${from_user_id}`, contentData);

			return { success: true, uniqueFileName };
		} catch (error) {
			console.error('Error uploading file:', error);
			return { success: false, error: 'Failed to upload file' };
		}
	},

	uploadJSONL: async ({ request }: RequestEvent) => {
		const formData = await request.formData();
		const file = formData.get('file');
		const userId = formData.get('userId');

		if (!(file instanceof Blob)) {
			return { success: false, error: 'No file uploaded' };
		}

		if (!userId || typeof userId !== 'string') {
			return { success: false, error: 'No user ID provided' };
		}

		try {
			const originalFilename = file.name;
			const fileExtension = originalFilename.split('.').pop();
			const timestamp = new Date().toISOString().replace(/[-:.]/g, '');
			const uniqueFileName = `${userId}_${timestamp}.${fileExtension}`;

			const fileContent = await file.text();
            const jsonlLines = fileContent.trim().split('\n');

			const contentData = {
                name: uniqueFileName,
                type: "image",
                hash: "", // Needs calculated elsewhere
                phash: "", // Needs calculated elsewhere
                width: 0, // Need image to calculate
                height: 0, // Need image to calculate
                url: [], // S3 URL?
                format: fileExtension, // This is currently jsonl for all images.
                size: file.size, // This is currently the jsonL size without the image.
                status: "pending",
                license: "CDLA-Permissive-2.0",
                license_url: "https://cdla.dev/permissive-2-0/",
                flags: 0,
                meta: {},
                content_authors: [],
                sources: []
            };

			const from_user_id = Number(userId) || 0
            const contentResponse = await makeJsonApiCall(`/content/?from_user_id=${from_user_id}`, contentData);


			for (const line of jsonlLines) {
                const jsonData = JSON.parse(line);
				const parsed = jsonData.parsed;
				const contentId = contentResponse.id

                const tags = parsed.tags_list.map((tagObj: any) => tagObj.tag);

				const annotations = {
					'short_caption': parsed.short_caption,
					'dense_caption': parsed.dense_caption,
					'tags': tags
				}

                const annotationData = {
                    annotation: annotations,
                    manually_adjusted: false,
                    overall_rating: 5,
                    content_id: contentId,
                    from_user_id: Number(userId) || 0,
                    // from_team_id: 0,
                    annotation_source_ids: []
                };

                await makeJsonApiCall('/annotations', annotationData);
            }

			if (process.env.NODE_ENV === 'production') {
			  	// S3 upload for production
				if (!s3Client) {
					throw new Error('S3 client is not initialized');
				}

				const fileBuffer = await file.arrayBuffer();

				await s3Client.send(new PutObjectCommand({
					Bucket: process.env.S3_BUCKET_NAME,
					Key: uniqueFileName,
					Body: Buffer.from(fileBuffer),
				}));

				console.log(`JSONL file uploaded to S3: ${uniqueFileName}`);
			} else {
				// Local file system for development

				await mkdir(JSONL_DIR, { recursive: true });

				const filePath = join(JSONL_DIR, uniqueFileName);
				const fileBuffer = await file.arrayBuffer();
				await writeFile(filePath, new Uint8Array(fileBuffer));
				console.log(`JSONL file saved locally: ${filePath}`);
			}

			return { success: true, uniqueFileName };
		} catch (error) {
			console.error('Error uploading file:', error);
			return { success: false, error: 'Failed to upload file' };
		}
	}
};

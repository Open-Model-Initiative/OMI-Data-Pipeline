// SPDX-License-Identifier: Apache-2.0
import { type RequestEvent } from '@sveltejs/kit';
import type { PageServerLoad } from './$types';

import { S3Client } from "@aws-sdk/client-s3";
import { db } from '../../../db';
import { contents } from '../../../db/schemas/contents';

import {
    handlePageLoad,
    handleFileUpload,
    PENDING_DIR,
    saveFileLocally,
    setupLocalDirectories,
    setupS3Client,
    uploadToS3,
		getFormData
} from '$lib/upload/shared';

export const load: PageServerLoad = async (event) => {
    await handlePageLoad(event);
};

const API_BASE_URL = process.env.API_SERVICE_URL ?? 'http://odr-api:31100/api/v1';

const s3Client: S3Client | null = setupS3Client();
setupLocalDirectories()

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

export const actions = {
	uploadHDR: async ({ request }: RequestEvent) => {
		const { file, userId } = await getFormData(request)
		const timestamp = new Date().toISOString().replace(/[-:.]/g, '');

		const { uniqueFileName, fileExtension } = handleFileUpload(file, timestamp, userId);

		try {
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

			if (process.env.NODE_ENV === 'production' && process.env.AWS_S3_BUCKET) {
			  // S3 upload for production
				await uploadToS3(s3Client, uniqueFileName, cleanedBuffer);
				await uploadToS3(s3Client, jpgFileName, jpgBuffer);
        await uploadToS3(s3Client, metadataFileName, metadataContent);
			} else {
				// Local file system for development
				await saveFileLocally(PENDING_DIR, uniqueFileName, cleanedBuffer);
				await saveFileLocally(PENDING_DIR, jpgFileName, jpgBuffer);
				await saveFileLocally(PENDING_DIR, metadataFileName, metadataContent);
			}

			// Create a content record for this image
			const newContent = await db.insert(contents).values({
				name: uniqueFileName,
				type: 'IMAGE',
				hash: "", // Needs calculated elsewhere
				phash: "", // Needs calculated elsewhere
				width: metadataData.width || 0,
				height: metadataData.height || 0,
				url: [],
				format: fileExtension,
				size: file.size,
				status: 'PENDING',
				license: "CDLA-Permissive-2.0",
				licenseUrl: "https://cdla.dev/permissive-2-0/",
				flags: 0,
				meta: metadataData,
				fromUserId: Number(userId) || 1,
				updatedAt: new Date().toISOString()
			}).returning();

			const contentRecord = newContent[0];
			console.log(`Created content record for ${uniqueFileName}:`, contentRecord.id);

			return { success: true, uniqueFileName };
		} catch (error) {
			console.error('Error uploading file:', error);
			return { success: false, error: 'Failed to upload file' };
		}
	}
};

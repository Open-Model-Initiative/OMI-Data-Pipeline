// SPDX-License-Identifier: Apache-2.0
import { redirect, type RequestEvent } from '@sveltejs/kit';
import type { PageServerLoad } from './$types';
import { PG_API } from '$lib/server/pg';
import { writeFile, mkdir } from 'fs/promises';
import { join } from 'path';
import fs from 'fs';
import path from 'path';

import { S3Client, PutObjectCommand } from "@aws-sdk/client-s3";
import { db } from '../db';
import { contents, contentSources } from '../db/schemas/contents';
import { annotations } from '../db/schemas/annotations';
import { contenttype, contentstatus, contentsourcetype } from '../db/schemas/enums';
import { eq } from 'drizzle-orm';

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

const UPLOAD_DIR = join(process.cwd(), 'uploads');
const IMAGE_DIR = join(UPLOAD_DIR, 'images');
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

function handleFileUpload(file: File, timestamp: string, userId: string): { uniqueFileName: string, fileExtension: string } {
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

async function uploadToS3(key: string, body: Buffer | string) {
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

async function saveFileLocally(directory: string, fileName: string, content: Buffer | ArrayBuffer | string) {
    await mkdir(directory, { recursive: true });
    const filePath = join(directory, fileName);
	if (Buffer.isBuffer(content) || content instanceof ArrayBuffer) {
		await writeFile(filePath, new Uint8Array(content));
	} else {
		await writeFile(filePath, content);
	}

    console.log(`File saved locally: ${filePath}`);
}

// Ensure directories exist
if (!fs.existsSync(UPLOAD_DIR)) {
    fs.mkdirSync(UPLOAD_DIR, { recursive: true });
}
if (!fs.existsSync(IMAGE_DIR)) {
    fs.mkdirSync(IMAGE_DIR, { recursive: true });
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

export const actions = {
	uploadHDR: async ({ request }: RequestEvent) => {
		const formData = await request.formData();
		const file = formData.get('file') as File;
		const userId = formData.get('userId') as string;
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

			if (process.env.NODE_ENV === 'production') {
			  	// S3 upload for production

				await uploadToS3(uniqueFileName, cleanedBuffer);
				await uploadToS3(jpgFileName, jpgBuffer);
            	await uploadToS3(metadataFileName, metadataContent);
			} else {
				// Local file system for development
				await mkdir(REJECTED_DIR, { recursive: true });
				await mkdir(FLAGGED_DIR, { recursive: true });

				await saveFileLocally(IMAGE_DIR, uniqueFileName, cleanedBuffer);
				await saveFileLocally(IMAGE_DIR, jpgFileName, jpgBuffer);
				await saveFileLocally(IMAGE_DIR, metadataFileName, metadataContent);
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
		const file = formData.get('file') as File;
		const userId = formData.get('userId') as string;
		const timestamp = new Date().toISOString().replace(/[-:.]/g, '');

		const { uniqueFileName, fileExtension } = handleFileUpload(file, timestamp, userId);

		try {
			const fileContent = await file.text();
            const jsonlLines = fileContent.trim().split('\n');

            // Parse all lines to extract unique filenames and their annotations
            const fileAnnotationsMap = new Map<string, any[]>();

            for (const line of jsonlLines) {
                try {
                    const jsonData = JSON.parse(line);
                    const filename = jsonData.filename;

                    if (!filename) {
                        console.error('Missing filename in JSONL line:', line);
                        continue;
                    }

                    // Get or create array for this filename
                    if (!fileAnnotationsMap.has(filename)) {
                        fileAnnotationsMap.set(filename, []);
                    }

                    // Add this annotation to the filename's array
                    fileAnnotationsMap.get(filename)?.push(jsonData);
                } catch (parseError) {
                    console.error('Error parsing JSONL line:', parseError);
                    // Continue processing other lines
                }
            }

            console.log(`Found ${fileAnnotationsMap.size} unique filenames in JSONL file`);
            let totalAnnotations = 0;
            fileAnnotationsMap.forEach((annotations, filename) => {
                console.log(`File ${filename} has ${annotations.length} annotation(s)`);
                totalAnnotations += annotations.length;
            });
            console.log(`Total annotations to process: ${totalAnnotations}`);

            // Create content records for each unique filename
            const contentRecords = [];

            try {
                // Process each unique filename
                for (const [filename, annotations] of fileAnnotationsMap.entries()) {
                    // Extract just the filename without path
                    const baseFilename = filename.split('/').pop() || filename;

                    // Create a content record for this filename
                    const newContent = await db.insert(contents).values({
                        name: baseFilename,
                        type: 'IMAGE',
                        hash: "", // Needs calculated elsewhere
                        phash: "", // Needs calculated elsewhere
                        width: 0, // Need image to calculate
                        height: 0, // Need image to calculate
                        url: [],
                        format: baseFilename.split('.').pop() || 'jpg',
                        size: 0, // We don't have the actual file size
                        status: 'PENDING',
                        license: "CDLA-Permissive-2.0",
                        licenseUrl: "https://cdla.dev/permissive-2-0/",
                        flags: 0,
                        meta: {},
                        fromUserId: Number(userId) || 1,
                        updatedAt: new Date().toISOString()
                    }).returning();

                    const contentRecord = newContent[0];
                    contentRecords.push(contentRecord);
                    console.log(`Created content record for ${baseFilename}:`, contentRecord.id);

                    // Process all annotations for this filename
                    for (const annotation of annotations) {
                        const parsed = annotation.parsed;

                        if (parsed) {
                            // Extract tags if available
                            const tags = parsed.tags_list ?
                                parsed.tags_list.map((tagObj: any) => tagObj.tag) :
                                [];

                            // Create annotation record with all available data
                            const annotationData = {
                                annotation: {
                                    // Include all parsed data
                                    ...parsed,
                                    // Ensure these specific fields are included
                                    'short_caption': parsed.short_caption || '',
                                    'dense_caption': parsed.dense_caption || '',
                                    'tags': tags,
                                    'tags_list': parsed.tags_list || [],
                                    'verification': parsed.verification || '',
                                    // Include model information
                                    'model': annotation.model || '',
                                    'provider': annotation.provider || '',
                                    'config_name': annotation.config_name || '',
                                    'version': annotation.version || ''
                                },
                                manually_adjusted: false,
                                overall_rating: 5,
                                content_id: contentRecord.id,
                                from_user_id: Number(userId) || 1,
                                annotation_source_ids: []
                            };

                            // Create annotation using API call
                            try {
                                const response = await makeJsonApiCall('/annotations', annotationData);
                                console.log(`Added annotation for content ID ${contentRecord.id}, annotation ID: ${response.id}`);
                            } catch (annotationError) {
                                console.error('Error adding annotation:', annotationError);
                            }
                        } else {
                            console.warn(`No parsed data found for annotation in file ${filename}`);
                        }
                    }
                }
            } catch (dbError) {
                console.error('Database connection error:', dbError);
                console.log('Falling back to API for content creation');

                // Fallback to API if database connection fails
                for (const [filename, annotations] of fileAnnotationsMap.entries()) {
                    // Extract just the filename without path
                    const baseFilename = filename.split('/').pop() || filename;

                    const contentData = {
                        name: baseFilename,
                        type: "image",
                        hash: "",
                        phash: "",
                        width: 0,
                        height: 0,
                        url: [],
                        format: baseFilename.split('.').pop() || 'jpg',
                        size: 0,
                        status: "pending",
                        license: "CDLA-Permissive-2.0",
                        license_url: "https://cdla.dev/permissive-2-0/",
                        flags: 0,
                        meta: {},
                        content_authors: [],
                        sources: []
                    };

                    const from_user_id = Number(userId) || 0;
                    const contentResponse = await makeJsonApiCall(`/content/?from_user_id=${from_user_id}`, contentData);
                    contentRecords.push(contentResponse);

                    // Process all annotations for this filename
                    for (const annotation of annotations) {
                        const parsed = annotation.parsed;

                        if (parsed) {
                            // Extract tags if available
                            const tags = parsed.tags_list ?
                                parsed.tags_list.map((tagObj: any) => tagObj.tag) :
                                [];

                            // Create annotation record with all available data
                            const annotationData = {
                                annotation: {
                                    // Include all parsed data
                                    ...parsed,
                                    // Ensure these specific fields are included
                                    'short_caption': parsed.short_caption || '',
                                    'dense_caption': parsed.dense_caption || '',
                                    'tags': tags,
                                    'tags_list': parsed.tags_list || [],
                                    'verification': parsed.verification || '',
                                    // Include model information
                                    'model': annotation.model || '',
                                    'provider': annotation.provider || '',
                                    'config_name': annotation.config_name || '',
                                    'version': annotation.version || ''
                                },
                                manually_adjusted: false,
                                overall_rating: 5,
                                content_id: contentResponse.id,
                                from_user_id: Number(userId) || 0,
                                annotation_source_ids: []
                            };

                            try {
                                const response = await makeJsonApiCall('/annotations', annotationData);
                                console.log(`Added annotation for content ID ${contentResponse.id}, annotation ID: ${response.id}`);
                            } catch (annotationError) {
                                console.error('Error adding annotation:', annotationError);
                            }
                        } else {
                            console.warn(`No parsed data found for annotation in file ${filename}`);
                        }
                    }
                }
            }

			// Save the file to disk or S3
			if (process.env.NODE_ENV === 'production' && process.env.AWS_S3_BUCKET) {
				// S3 upload for production
				const fileBuffer = await file.arrayBuffer();
				await uploadToS3(uniqueFileName, Buffer.from(fileBuffer));
			} else {
				// Local file system for development
				await mkdir(JSONL_DIR, { recursive: true });
				const fileBuffer = await file.arrayBuffer();
				await saveFileLocally(JSONL_DIR, uniqueFileName, fileBuffer);
			}

			return {
				type: 'success',
				data: JSON.stringify([true, true, `Successfully uploaded ${uniqueFileName}`, { contentCount: contentRecords.length }])
			};
		} catch (error) {
			console.error('Error uploading JSONL file:', error);
			return {
				type: 'error',
				data: JSON.stringify([true, false, `Failed to upload JSONL file: ${error instanceof Error ? error.message : String(error)}`])
			};
		}
	}
};

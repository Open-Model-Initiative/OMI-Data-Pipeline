<!--
  SPDX-License-Identifier: Apache-2.0
-->
<script lang="ts">
	import './moderation.css';
	import { goto } from '$app/navigation';
	import { TriangleExclamationSolid } from 'svelte-awesome-icons';
	import type { PageData } from './$types';
	import { toaster } from '$lib/toaster-svelte'

	export let data: PageData;

	$: ({ images, currentPage, totalPages } = data);

	function goToPage(page: number) {
		goto(`?page=${page}`);
	}

	async function handleAction(action: 'accept' | 'reject' | 'flag', filename: string) {
		const form = new FormData();
		form.append('filename', filename);

		const response = await fetch(`?/${action}`, {
			method: 'POST',
			body: form
		});

		if (response.ok) {
			// Remove the image from the list
			images = images.filter(img => img.filename !== filename);
			toaster.success({
				title: `Image ${action}ed successfully.`
			});
		} else {
			console.error(`Failed to ${action} image`);
			toaster.error({
				title: `Failed to ${action} image`
			});
		}
	}

	let showPreview = false;
	let previewImageUrl = '';

	function openPreview(imageUrl: string) {
		previewImageUrl = imageUrl;
		showPreview = true;
	}

	function closePreview() {
		showPreview = false;
	}
</script>

<div class="moderation-page">
  <h1>HDR Image Moderation</h1>
  <div class="table-container">
	<table class="table">
	  <thead>
		<tr>
		  <th>Image</th>
		  <th>User</th>
		  <th>Metadata</th>
		  <th>Action</th>
		</tr>
	  </thead>
	  <tbody>
		{#each images as image}
		  <tr>
			<td>
				<button
					class="image-preview-button"
					onclick={() => openPreview(image.previewUrl)}
				>
					<img
						src={image.previewUrl}
						alt="Preview"
						class="preview-image"
					/>
				</button>
			</td>
			<td>{image.metadata.uploadedByUser}</td>
			<td>
			  <pre>{JSON.stringify(image.metadata, null, 2)}</pre>
			</td>
			<td>
				<div class="button-group">
				  <button
						class="btn btn-sm preset-filled-success-500"
						onclick={() => handleAction('accept', image.filename)}
						title="Accept the image"
				  >
						Accept
				  </button>
				  <button
						class="btn btn-sm preset-filled-error-500"
						onclick={() => handleAction('reject', image.filename)}
						title="Reject the image"
				  >
						Reject
				  </button>
				  <button
						class="btn btn-sm preset-filled-warning-500 flag-button"
						onclick={() => handleAction('flag', image.filename)}
						title="Flag suspected illegal content"
				  >
					<TriangleExclamationSolid size="23" />
				  </button>
				</div>
			  </td>
		  </tr>
		{/each}
	  </tbody>
	</table>
  </div>

{#if showPreview}
	<div class="modal-overlay">
		<button class="close-button" onclick={closePreview}>×</button>
		<div class="modal-content">
			<img src={previewImageUrl} alt="Large Preview" />
		</div>
  </div>
{/if}


  <div class="pagination">
	{#if currentPage > 1}
	  <button class='btn btn-sm variant-outline-primary' onclick={() => goToPage(currentPage - 1)}>Previous</button>
	{/if}

	<span>Page {currentPage} of {totalPages}</span>

	{#if currentPage < totalPages}
	  <button class='btn btn-sm variant-outline-primary' onclick={() => goToPage(currentPage + 1)}>Next</button>
	{/if}
  </div>
</div>

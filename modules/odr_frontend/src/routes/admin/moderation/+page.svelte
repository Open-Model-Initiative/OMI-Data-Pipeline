<script lang="ts">
	import { goto } from '$app/navigation';
	import type { PageData } from './$types';

	export let data: PageData;

	$: ({ images, currentPage, totalPages } = data);

	function goToPage(page: number) {
		goto(`?page=${page}`);
	}

	async function handleAction(action: 'accept' | 'reject', filename: string) {
		const form = new FormData();
		form.append('filename', filename);

		const response = await fetch(`?/${action}`, {
			method: 'POST',
			body: form
		});

		if (response.ok) {
			// Remove the image from the list
			images = images.filter(img => img.filename !== filename);
		} else {
			console.error(`Failed to ${action} image`);
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

  <h1>HDR Image Moderation</h1>
  <div class="table-container">
	<table class="table table-hover">
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
					on:click={() => openPreview(image.previewUrl)}
				>
					<img
					src={image.previewUrl}
					alt="Preview"
					style="max-width: 100px; max-height: 100px;"
					/>
				</button>
			</td>
			<td>{image.metadata.uploadedByUser}</td>
			<td>
			  <pre>{JSON.stringify(image.metadata, null, 2)}</pre>
			</td>
			<td>
				<button
					class="btn btn-sm variant-filled-success"
					on:click={() => handleAction('accept', image.filename)}
				>
				Accept
			  </button>
			  <button
				class="btn btn-sm variant-filled-error"
				on:click={() => handleAction('reject', image.filename)}
			  >
				Reject
			  </button>
			</td>
		  </tr>
		{/each}
	  </tbody>
	</table>
  </div>

{#if showPreview}
	<div class="modal-overlay">
		<button class="close-button" on:click={closePreview}>×</button>
		<div class="modal-content">
		<img src={previewImageUrl} alt="Large Preview" />
		</div>
  	</div>
{/if}


  <div class="pagination">
	{#if currentPage > 1}
	  <button on:click={() => goToPage(currentPage - 1)}>Previous</button>
	{/if}

	<span>Page {currentPage} of {totalPages}</span>

	{#if currentPage < totalPages}
	  <button on:click={() => goToPage(currentPage + 1)}>Next</button>
	{/if}
  </div>

  <!-- TODO: Move to a stylesheet. -->
  <style>
	.modal-overlay {
	  position: fixed;
	  top: 0;
	  left: 0;
	  width: 100%;
	  height: 100%;
	  background-color: rgba(0, 0, 0, 0.8);
	  display: flex;
	  justify-content: center;
	  align-items: center;
	  z-index: 1000;
	}

	.modal-content {
	  max-width: 90vw;
	  max-height: 90vh;
	  display: flex;
	  justify-content: center;
	  align-items: center;
	}

	.modal-content img {
	  max-width: 90vw;
	  max-height: 90vh;
	  object-fit: contain;
	}

	.close-button {
		position: absolute;
		top: 20px;
		right: 20px;
		width: 30px;
		height: 30px;
		background-color: rgba(255, 255, 255, 0.7);
		border: none;
		border-radius: 50%;
		font-size: 20px;
		line-height: 1;
		display: flex;
		justify-content: center;
		align-items: center;
		cursor: pointer;
		padding: 0;
		color: #333;
	}

	.close-button:hover,
	.close-button:focus {
		background-color: rgba(255, 255, 255, 0.9);
		outline: none;
	}

	.image-preview-button {
	  background: none;
	  border: none;
	  padding: 0;
	  cursor: pointer;
	}

	.image-preview-button:focus {
	  outline: 2px solid blue;
	}
  </style>

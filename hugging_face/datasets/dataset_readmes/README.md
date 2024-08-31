---
license: cc-by-4.0
language:
- en
pretty_name: "OMI Initial Test Dataset"
---


# OMI Initial Test Dataset

   ## Dataset Description

   - **Repository:** https://huggingface.co/datasets/openmodelinitiative/initial-test-dataset

   ### Dataset Summary

   This dataset contains an initial batch of test images pulled from other datasets to test our basic architecture.

   ### Languages

   The captions and all information is presented in English.

   ## Dataset Structure

   ### Data Fields

- `id`: A unique identifier for the content
- `name`: The name or title of the content
- `type`: The type of content (e.g., "image")
- `hash`: A hash value for the image (implementation to be determined)
- `phash`: A perceptual hash value for the image (implementation to be determined)
- `urls`: An array of URLs where the image can be accessed
- `width`: The width of the image in pixels (none if not an image)
- `height`: The height of the image in pixels (none if not an image)
- `format`: The file format of the content (e.g., "jpg", "png")
- `size`: The file size in bytes
- `status`: The availability status of the content (e.g., "available")
- `license`: The license under which the content is released
- `licenseUrl`: URL to the full text of the license
- `contentAuthor`: An array of objects containing information about the content creator(s)
  - `id`: Identifier for the author
  - `name`: Name of the author or organization
  - `url`: URL associated with the author or organization
- `flags`: A numeric value representing any flags associated with the content
- `meta`: An object for additional metadata.
- `fromUser`: Information about the user who uploaded the content
- `fromTeam`: Information about the team who uploaded the content
- `annotations`: An array of annotation objects associated with the content
  - `id`: Unique identifier for the annotation
  - `content`: A brief content descriptor
  - `annotation`: An object containing detailed annotation information
    - `type`: The type of annotation (e.g., "image-description")
    - `text`: A textual description or annotation of the content
    - `tags`: An array of relevant tags (Important Note: this will be removed and made its own annotation soon!)
  - `manuallyAdjusted`: Boolean indicating if the annotation was manually adjusted
  - `embedding`: Embedding of the annotation
  - `fromUser`: User who created the annotation
  - `fromTeam`: Team associated with the annotation
  - `createdAt`: Timestamp of when the annotation was created
  - `updatedAt`: Timestamp of when the annotation was last updated
  - `overallRating`: A numeric rating for the annotation
- `embeddings`: An array for storing embedding information
- `createdAt`: Timestamp of when the content entry was created
- `updatedAt`: Timestamp of when the content entry was last updated

import argparse
import base64
import io
import json
import os
import requests
import shutil
from pathlib import Path
from PIL import Image, UnidentifiedImageError
from io import BytesIO
from datasets import load_dataset, Dataset

from embeddings.image_embeddings import calculate_image_embedding, instantiate_model, is_unique_image

# Taken from https://github.com/huggingface/diffusers/blob/2dad462d9bf9890df09bfb088bf0a446c6074bec/src/diffusers/pipelines/pixart_alpha/pipeline_pixart_alpha.py#L135
ASPECT_RATIO_256_BIN = {
    "0.25": [128.0, 512.0],
    "0.28": [128.0, 464.0],
    "0.32": [144.0, 448.0],
    "0.33": [144.0, 432.0],
    "0.35": [144.0, 416.0],
    "0.4": [160.0, 400.0],
    "0.42": [160.0, 384.0],
    "0.48": [176.0, 368.0],
    "0.5": [176.0, 352.0],
    "0.52": [176.0, 336.0],
    "0.57": [192.0, 336.0],
    "0.6": [192.0, 320.0],
    "0.68": [208.0, 304.0],
    "0.72": [208.0, 288.0],
    "0.78": [224.0, 288.0],
    "0.82": [224.0, 272.0],
    "0.88": [240.0, 272.0],
    "0.94": [240.0, 256.0],
    "1.0": [256.0, 256.0],
    "1.07": [256.0, 240.0],
    "1.13": [272.0, 240.0],
    "1.21": [272.0, 224.0],
    "1.29": [288.0, 224.0],
    "1.38": [288.0, 208.0],
    "1.46": [304.0, 208.0],
    "1.67": [320.0, 192.0],
    "1.75": [336.0, 192.0],
    "2.0": [352.0, 176.0],
    "2.09": [368.0, 176.0],
    "2.4": [384.0, 160.0],
    "2.5": [400.0, 160.0],
    "3.0": [432.0, 144.0],
    "4.0": [512.0, 128.0],
}


annotationReplacementList = [
    ('The image showcases ', ''),
    ('The image portrays ', ''),
    ('The image appears to be ', ''),
    ('The image is ', ''),
    ('The image depicts ', ''),
    ('The image features ', ''),
    ('The image captures ', ''),
    ('The image shows ', ''),
    ('The image displays ', ''),
    ('The image presents ', ''),
    ('This image showcases ', ''),
    ('This image portrays ', ''),
    ('This image appears to be ', ''),
    ('This image is ', ''),
    ('This image depicts ', ''),
    ('This image features ', ''),
    ('This image captures ', ''),
    ('This image shows ', ''),
    ('This image displays ', ''),
    ('This image presents ', ''),
    ('In this picture, ', ''),
    ('In this artwork, ', 'Artwork of '),
    ('In this illustration, ', 'Illustration of '),
    ('In this depiction, ', ''),
    ('In this piece, ', ''),
    ('In this image, ', ''),
    ('In this art piece, ', 'Art of '),
    ('In this scene, ', ''),
    ('In the picture, ', ''),
    ('In the artwork, ', 'Artwork of '),
    ('In the illustration, ', 'Illustration of '),
    ('In the depiction, ', ''),
    ('In the piece, ', ''),
    ('In the image, ', ''),
    ('In the art piece, ', 'Art of '),
    ('In the scene, ', ''),
]


def process_chunk(output_dir, dataset_repo, chunk_number, dataset_name):
    chunk_dir = output_dir / f"{dataset_name}_chunk{chunk_number}"
    upload_chunk(chunk_dir, dataset_repo)
    delete_chunk(chunk_dir)


def upload_chunk(chunk_dir, dataset_repo):
    print(f"Uploading Chunk {chunk_dir.name}...")
    jsonFile = chunk_dir / 'metadata.jsonl'
    dataset = load_dataset('json', data_files=str(jsonFile))['train']
    dataset.push_to_hub(dataset_repo, private=True)  # Private as we do not want to host image data for others.


def delete_chunk(chunk_dir):
    print(f"Processed {chunk_dir.name}. Deleting chunk directory...")
    shutil.rmtree(chunk_dir)


def get_target_size(img):
    width, height = img.size
    aspect_ratio = width / height

    closest_ratio = min(ASPECT_RATIO_256_BIN.keys(), key=lambda x: abs(float(x) - aspect_ratio))
    target_width, target_height = ASPECT_RATIO_256_BIN[closest_ratio]

    return int(target_width), int(target_height)


def get_image_bytes(img, format='JPEG'):
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format=format)
    contents = img_byte_arr.getvalue()

    return len(contents)


def image_to_base64(img):
    buffered = BytesIO()
    img.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue()).decode()


def try_downloading_image(data):
    def try_hugging_face(meta, image_column):
        try:
            dataset_name = meta.get('hf-dataset-name')
            split = meta.get('hf-dataset-split')
            id = meta.get('hf-dataset-id')

            if not all([dataset_name, split, id, image_column]):
                missing_values = []
                if not dataset_name:
                    missing_values.append("dataset_name")
                if not split:
                    missing_values.append("split")
                if not id:
                    missing_values.append("id")
                if not image_column:
                    missing_values.append("image_column")

                if missing_values:
                    print(f"Missing information for: {', '.join(missing_values)}")
                    return None

            dataset = load_dataset(dataset_name, split=split)
            if image_column not in dataset.features:
                print(f"{image_column} was not in dataset features")
                return None

            item = dataset[id][image_column]

            if isinstance(item, dict) and 'bytes' in item:
                return Image.open(io.BytesIO(item['bytes']))
            elif isinstance(item, Image.Image):
                return item
            elif isinstance(item, str):
                return Image.open(item)
            else:
                return None
        except Exception as exception:
            print(f"An exception occurred while trying to load image from hugging face: {str(exception)}")
            return None

    def try_urls(urls):
        for url in urls:
            try:
                response = requests.get(url, timeout=10)
                response.raise_for_status()
                try:
                    return Image.open(io.BytesIO(response.content))
                except (IOError, UnidentifiedImageError) as img_error:
                    print(f"Failed to open image from {url}: {str(img_error)}")
                    continue
            except requests.RequestException as req_error:
                print(f"Failed to download image from {url}: {str(req_error)}")
                continue

        print("Could not download or open image from any of the provided URLs")
        return None

    # Try downloading from Hugging Face image first
    image = try_hugging_face(data.get('meta', {}), data.get('image_column'))

    # If Hugging Face download fails, try URLs
    if image is None:
        image = try_urls(data.get('urls', []))

    return (image is not None, image)


def clean_annotation(annotation):
    cleaned_annotation = annotation
    for old, new in annotationReplacementList:
        cleaned_annotation = cleaned_annotation.replace(old, new)

    return cleaned_annotation


def process_jsonl(dataset_repo, input_file, chunk_size):
    input_path = Path(input_file).resolve()
    input_dir = input_path.parent
    output_dir = input_dir.parent / f"{input_dir.name}_processed"
    output_dir.mkdir(exist_ok=True)

    dataset_name = input_path.stem
    processed_count = 0
    chunk_number = 1

    embedding_model, model_name, collection = instantiate_model()

    current_chunk_dir = output_dir / f"{dataset_name}_chunk{chunk_number}"
    current_chunk_dir.mkdir(exist_ok=True)
    current_chunk_file = current_chunk_dir / 'metadata.jsonl'

    with open(input_file, 'r') as f:
        for line in f:
            data = json.loads(line)

            if data.get('processed', False):
                continue

            image_downloaded, image = try_downloading_image(data)

            if not image_downloaded:
                data['status'] = 'unavailable'
            else:
                data['original_width'], data['original_height'] = image.size

                target_width, target_height = get_target_size(image)
                data['width'] = target_width
                data['height'] = target_height

                image_resized = image.resize((target_width, target_height))

                # Save the image in the current chunk directory
                image_filename = f"image_{processed_count}.jpg"
                image_path = current_chunk_dir / image_filename
                image_resized.save(image_path, format="JPEG")

                data['image'] = image_to_base64(image_resized)
                data['processed_size'] = get_image_bytes(image_resized)

                for annotation in data["annotations"]:
                    annotation_text = annotation["annotation"]["text"]
                    cleaned_annotation = clean_annotation(annotation_text)
                    annotation["annotation"]["clean_text"] = cleaned_annotation

                embedding = calculate_image_embedding(embedding_model, image_resized)
                data['embeddings'].append({
                    "model": model_name,
                    "embedding": embedding.tolist()
                })

                image_id = str(processed_count)
                unique_image = is_unique_image(collection, embedding, image_id)
                data['is_unique'] = unique_image

                data['processed'] = True

            with open(current_chunk_file, 'a') as f:
                json.dump(data, f)
                f.write('\n')

            processed_count += 1

            if processed_count % chunk_size == 0:
                process_chunk(output_dir, dataset_repo, chunk_number, dataset_name)
                chunk_number += 1
                current_chunk_dir = output_dir / f"{dataset_name}_chunk{chunk_number}"
                current_chunk_dir.mkdir(exist_ok=True)
                current_chunk_file = current_chunk_dir / 'metadata.jsonl'

    # Process any remaining data after finishing
    if processed_count % chunk_size != 0:
        process_chunk(output_dir, dataset_repo, chunk_number, dataset_name)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process JSONL dataset file and download images.")
    parser.add_argument("-d", "--dataset_repo", required=True, help="The repository name for the dataset on Hugging Face Hub")
    parser.add_argument("-f", "--dataset_file", help="Path to the input JSONL file")
    parser.add_argument("-c", "--chunk_size", type=int, default=50, help="Number of items to process in a batch before uploading the dataset")
    args = parser.parse_args()

    process_jsonl(args.dataset_repo, args.dataset_file, args.chunk_size)

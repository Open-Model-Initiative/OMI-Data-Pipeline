import argparse
import json
import io
import math
import os

from io import BytesIO
from pathlib import Path

import requests
from PIL import Image
from datasets import load_dataset, Dataset, Image as HF_Image


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


def process_chunk(output_dir):
    upload_chunk(output_dir)
    delete_chunk(output_dir)


def upload_chunk(output_dir):
    print("Uploading Chunk ...")

    jsonFile = os.path.join(output_dir, 'metadata.jsonl')

    # Load the dataset
    dataset = load_dataset('json', data_files=jsonFile)['train']

    # Get the list of image paths
    image_paths = [os.path.join(output_dir, example['image']) if 'image' in example and example['image'] is not None else None
                   for example in dataset]

    # Create a new dataset with the image paths
    image_dataset = Dataset.from_dict({"image": image_paths})

    # Cast the 'image' column to Image type
    image_dataset = image_dataset.cast_column("image", HF_Image())

    # Combine the original dataset with the image dataset
    combined_dataset = Dataset.from_dict({
        **{col: dataset[col] for col in dataset.column_names},
        "image": image_dataset["image"]
    })

    print(combined_dataset)
    # combined_dataset.push_to_hub("openmodelinitiative/initial-test-dataset-private", private=True)


def delete_chunk(output_dir):
    print("Processed next chunk. Deleting processed images...")
    for file in output_dir.glob('*'):
        if file.is_file() and file.suffix.lower() in ['.jpg', '.jpeg', '.png', '.gif']:
            file.unlink()


def get_target_size(img):
    width, height = img.size
    aspect_ratio = width / height

    closest_ratio = min(ASPECT_RATIO_256_BIN.keys(), key=lambda x: abs(float(x) - aspect_ratio))
    target_width, target_height = ASPECT_RATIO_256_BIN[closest_ratio]

    return int(target_width), int(target_height)


def process_jsonl(input_file, chunk_size):
    input_path = Path(input_file).resolve()
    input_dir = input_path.parent
    output_dir = input_dir.parent / f"{input_dir.name}_processed"
    output_dir.mkdir(exist_ok=True)

    processed_count = 0

    with open(input_file, 'r') as f:
        for line in f:
            data = json.loads(line)

            image_downloaded = False
            for url in data.get('urls', []):
                try:
                    response = requests.get(url, timeout=10)
                    response.raise_for_status()
                    image_content = response.content
                    image_downloaded = True
                    break
                except requests.RequestException:
                    continue

            if not image_downloaded:
                data['status'] = 'unavailable'
            else:
                image_filename = url.split('/')[-1]
                data['image'] = image_filename

                img = Image.open(BytesIO(image_content))

                data['original_width'], data['original_height'] = img.size

                target_width, target_height = get_target_size(img)
                data['width'] = target_width
                data['height'] = target_height

                img_resized = img.resize((target_width, target_height))

                img_resized.save(output_dir / image_filename)

            output_file = output_dir / f"{input_path.name}"
            with open(output_file, 'a') as f:
                json.dump(data, f)
                f.write('\n')

            processed_count += 1

            if processed_count % chunk_size == 0:
                process_chunk(output_dir)

    # Process any remaining data after finishing
    process_chunk(output_dir)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process JSONL file and download images.")
    parser.add_argument("input_file", help="Path to the input JSONL file")
    parser.add_argument("--chunk_size", type=int, default=100, help="Number of images to process in a batch before uploading the dataset")
    args = parser.parse_args()

    process_jsonl(args.input_file, args.chunk_size)

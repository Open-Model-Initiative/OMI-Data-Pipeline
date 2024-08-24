import argparse
import json
import io
import os

from io import BytesIO
from pathlib import Path

import requests
from PIL import Image
from datasets import load_dataset, Dataset, Image as HF_Image


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

                data['original_width'] = data.get('width')
                data['original_height'] = data.get('height')

                data['width'] = 256
                data['height'] = 256

                img = Image.open(BytesIO(image_content))
                img_resized = img.resize((256, 256))

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

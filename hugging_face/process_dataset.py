import argparse
import base64
import io
import json
import os
import requests
from pathlib import Path
from PIL import Image
from io import BytesIO
from datasets import load_dataset, Dataset

dataset_repo = "openmodelinitiative/initial-test-dataset-private"

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
    dataset = load_dataset('json', data_files=jsonFile)['train']

    dataset.push_to_hub(dataset_repo, private=True)  # Private as we do not want to host image data for others.


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


def get_image_bytes(img, format='JPEG'):
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format=format)
    contents = img_byte_arr.getvalue()

    return len(contents)


def image_to_base64(img):
    buffered = BytesIO()
    img.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue()).decode()


def process_jsonl(input_file, chunk_size):
    input_path = Path(input_file).resolve()
    input_dir = input_path.parent
    output_dir = input_dir.parent / f"{input_dir.name}_processed"
    output_dir.mkdir(exist_ok=True)

    output_file = output_dir / f"{input_path.name}"

    if output_file.exists():
        output_file.unlink()

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
                img = Image.open(BytesIO(image_content))

                data['original_width'], data['original_height'] = img.size

                target_width, target_height = get_target_size(img)
                data['width'] = target_width
                data['height'] = target_height

                img_resized = img.resize((target_width, target_height))

                data['image'] = image_to_base64(img_resized)
                data['processed_size'] = get_image_bytes(img_resized)

            with open(output_file, 'a') as f:
                json.dump(data, f)
                f.write('\n')

            processed_count += 1

            if processed_count % chunk_size == 0:
                process_chunk(output_dir)

    # Process any remaining data after finishing
    process_chunk(output_dir)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process JSONL dataset file and download images.")
    parser.add_argument("-f", "--dataset_file", help="Path to the input JSONL file")
    parser.add_argument("-c", "--chunk_size", type=int, default=50, help="Number of items to process in a batch before uploading the dataset")
    args = parser.parse_args()

    process_jsonl(args.dataset_file, args.chunk_size)

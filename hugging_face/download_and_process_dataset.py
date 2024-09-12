import argparse
import base64
import hashlib
import io
import json
import logging
import requests
import shutil
import tempfile
from pathlib import Path
from PIL import Image, UnidentifiedImageError
from io import BytesIO
from datasets import Dataset, load_dataset

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

datasets = {}


def get_target_size(img: Image.Image) -> tuple[int, int]:
    width, height = img.size
    aspect_ratio = width / height

    closest_ratio = min(ASPECT_RATIO_256_BIN.keys(), key=lambda x: abs(float(x) - aspect_ratio))
    target_width, target_height = ASPECT_RATIO_256_BIN[closest_ratio]

    return int(target_width), int(target_height)


def standardize_image(img: Image.Image) -> Image.Image:
    if img.mode not in ('RGB', 'RGBA'):
        return img.convert('RGBA')
    return img


def image_to_base64(img: Image.Image) -> str:
    img = standardize_image(img)
    buffered = BytesIO()

    try:
        img.save(buffered, format="PNG")
    except Exception as e:
        logging.error(f"Error saving image as PNG: {e}")
        return ""

    contents = buffered.getvalue()
    return base64.b64encode(contents).decode(), len(contents)


def generate_image_filename(data):
    # Create a unique hash based on the image data
    hash_object = hashlib.md5(json.dumps(data, sort_keys=True).encode())
    return f"image_{hash_object.hexdigest()}"


def try_downloading_image(data: dict, local_image_dir: Path) -> tuple[bool, Image.Image | None]:
    def try_hugging_face(meta, image_column):
        global datasets

        try:
            dataset_name = meta.get('hf-dataset-name')
            split = meta.get('hf-dataset-split')
            item_id = meta.get('hf-dataset-id')

            if not all([dataset_name, split, item_id, image_column]):
                missing_values = []
                if dataset_name is None or dataset_name == "":
                    missing_values.append("dataset_name")
                if split is None or split == "":
                    missing_values.append("split")
                if item_id is None or item_id == "":
                    missing_values.append("item_id")
                if image_column is None or image_column == "":
                    missing_values.append("image_column")

                if missing_values:
                    logging.debug(f"Missing information for: {', '.join(missing_values)}")
                    return None

            dataset_key = f"{dataset_name}_{split}"

            if dataset_key not in datasets:
                datasets[dataset_key] = load_dataset(dataset_name, split=split)

            dataset = datasets[dataset_key]

            if image_column not in dataset.features:
                logging.debug(f"{image_column} was not in dataset features")
                return None

            item = dataset[item_id][image_column]

            if isinstance(item, dict) and 'bytes' in item:
                return Image.open(io.BytesIO(item['bytes']))
            elif isinstance(item, Image.Image):
                return item
            elif isinstance(item, str):
                return Image.open(item)
            else:
                return None
        except Exception as exception:
            logging.debug(f"An exception occurred while trying to load image from hugging face: {str(exception)}")
            return None

    def try_urls(urls):
        for url in urls:
            try:
                response = requests.get(url, timeout=10)
                response.raise_for_status()
                try:
                    return Image.open(io.BytesIO(response.content))
                except (IOError, UnidentifiedImageError) as img_error:
                    logging.warning(f"Failed to open image from {url}: {str(img_error)}")
                    continue
            except requests.RequestException as req_error:
                logging.warning(f"Failed to download image from {url}: {str(req_error)}")
                continue

        logging.warning("Could not download or open image from any of the provided URLs")
        return None

    image_filename = generate_image_filename(data)
    local_image_path = local_image_dir / f"{image_filename}.png"

    if local_image_path.exists():
        try:
            image = Image.open(local_image_path)
            return True, standardize_image(image), True
        except Exception as e:
            logging.warning(f"Error opening local image {local_image_path}: {e}")

    # Try downloading from Hugging Face image first
    image = try_hugging_face(data.get('meta', {}), data.get('image_column'))

    # If Hugging Face download fails, try URLs
    if image is None:
        image = try_urls(data.get('urls', []))

    if image is not None:
        image = standardize_image(image)

    return (image is not None, image, False)


def save_processed_image(image: Image, data: dict, local_image_dir: Path):
    image_standardized = standardize_image(image)

    image_filename = generate_image_filename(data)
    image_path = local_image_dir / image_filename
    image_standardized.save(image_path, format="PNG")


def process_all_images(dataset_file: str, local_image_dir: Path) -> None:
    local_image_dir.mkdir(parents=True, exist_ok=True)
    temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False)

    processed = 0

    with open(dataset_file, 'r') as input_jsonl:
        for line in input_jsonl:
            logging.info(f"Processing row {processed + 1} . . .")

            data = json.loads(line)
            image_downloaded, image, is_local = try_downloading_image(data, local_image_dir)

            if not image_downloaded:
                data['status'] = 'unavailable'
            else:
                try:
                    if not is_local:
                        data['original_width'], data['original_height'] = image.size
                        target_width, target_height = get_target_size(image)
                        data['width'] = target_width
                        data['height'] = target_height

                        image_resized = image.resize((target_width, target_height))
                        save_processed_image(image_resized, data, local_image_dir)

                        data['image'], data['processed_size'] = image_to_base64(image_resized)
                    else:
                        # If the image was loaded locally, we don't need to process it again
                        data['width'], data['height'] = image.size
                        data['image'], data['processed_size'] = image_to_base64(image)
                except Exception as e:
                    logging.warning(f"Error processing image: {e}")
                    data['status'] = 'unavailable'

            processed += 1

            json.dump(data, temp_file)
            temp_file.write('\n')

    temp_file.close()
    shutil.move(temp_file.name, dataset_file)


def main() -> None:
    parser = argparse.ArgumentParser(description="Process JSONL dataset file and download all images.")
    parser.add_argument("-f", "--dataset_file", help="Path to the input JSONL file")
    parser.add_argument("-d", "--image_dir", default="./dataset_images/processed", help="Directory to store processed images")
    args = parser.parse_args()

    local_image_dir = Path(args.image_dir)
    process_all_images(args.dataset_file, local_image_dir)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    main()

# SPDX-License-Identifier: Apache-2.0
import argparse
import base64
import io
import logging
import os
from datasets import load_dataset
from io import BytesIO
from PIL import Image, UnidentifiedImageError

import get_hf_features

skip_fields = [
    'original_caption'
]


def load_bad_images(bad_images_folder: str = 'datasets/bad_images') -> list:
    """
    Load all bad images from the specified folder into memory.
    """
    bad_images = []
    for filename in os.listdir(bad_images_folder):
        if filename.endswith(('.png', '.jpg', '.jpeg')):
            bad_image_path = os.path.join(bad_images_folder, filename)
            bad_image = Image.open(bad_image_path)
            bad_images.append(list(bad_image.getdata()))
    return bad_images


def is_bad_image(image: Image.Image, bad_images: list) -> bool:
    """
    Compare the given image with known bad images.
    Return True if the image matches any of the bad images, False otherwise.
    """
    image_data = list(image.getdata())
    return any(image_data == bad_image for bad_image in bad_images)


def process_item(item: dict, dataset_name: str, bad_images: list) -> bool:
    """
    Process a single item from the dataset.
    Display its properties and save it if it is valid.
    """
    try:
        display_item_properties(item)

        image_data = item.get('image')
        if not image_data:
            logging.debug("No image found in the item.")
            return False

        try:
            image = base64_to_image(image_data)
        except (ValueError, UnidentifiedImageError) as e:
            logging.warning(f"Error processing image: {e}")
            return False

        # Note: only one image matched the currently know bad image (the first image), so this may be redudant.
        if is_bad_image(image, bad_images):
            logging.info("Detected a known bad image. Skipping processing.")
            return False

        # image.show()
        content_id = item.get('id')
        save_image(image, content_id, dataset_name)

        print(f'\nAnnotations for {content_id}:')
        annotations = item.get('annotations', [])
        for annotation in annotations:
            annotation_item = annotation.get('annotation', {})
            annotation_field = annotation_item.get('original_field', '')

            if (annotation_field not in skip_fields):
                annotation_text = annotation_item.get('clean_text', '').replace('This image displays: ', '').strip()
                print(f'{annotation_field}: {annotation_text}')
                # TODO: Valid item to train on

        return True
    except Exception as e:
        logging.error(f"Unexpected error processing item: {e}")
        return False


def display_item_properties(item: dict) -> None:
    """
    Display the properties of the given item.
    """
    logging.debug("Item properties:")
    for key, value in item.items():
        if key != 'image':
            logging.debug(f"{key}: {value}")


def base64_to_image(base64_string: str) -> Image.Image:
    img_data = base64.b64decode(base64_string)
    return Image.open(BytesIO(img_data))


def save_image(image: Image.Image, image_id: str, dataset_name: str) -> None:
    """
    Save the image to a folder called dataset_images/{dataset_name}.
    Create the folders if they don't exist.
    """
    base_folder = 'dataset_images'
    dataset_folder = os.path.join(base_folder, dataset_name)

    # Create the base folder if it doesn't exist
    if not os.path.exists(base_folder):
        os.makedirs(base_folder)

    # Create the dataset-specific folder if it doesn't exist
    if not os.path.exists(dataset_folder):
        os.makedirs(dataset_folder)

    file_name = f"{image_id}.png"
    file_path = os.path.join(dataset_folder, file_name)

    image.save(file_path)
    logging.debug(f"Image saved as {file_path}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Load one of our private Hugging Face datasets locally.")
    parser.add_argument("-d", "--dataset_name", help="Name of the Hugging Face dataset")
    parser.add_argument("-n", "--num_items", type=int, default=1, help="Number of items to download (default: 1)")
    args = parser.parse_args()

    dataset_name = args.dataset_name
    num_items = args.num_items

    bad_images = load_bad_images()

    ds_builder = get_hf_features.get_ds_builder(dataset_name)
    get_hf_features.print_splits(ds_builder)

    dataset = load_dataset(dataset_name, split='train', streaming=True)

    available_items = dataset.filter(lambda example: example.get('status') == 'available')

    total_processed = 0
    successful_count = 0
    unsuccessful_count = 0

    for i, item in enumerate(available_items.take(num_items)):
        if process_item(item, dataset_name, bad_images):
            successful_count += 1
        else:
            unsuccessful_count += 1

        total_processed += 1

        if total_processed % 1000 == 0:
            logging.info(f"Processed {total_processed} items. Successful: {successful_count}, Unsuccessful: {unsuccessful_count}")

    logging.info(f"\nProcessing complete. Successful items: {successful_count}, Unsuccessful items: {unsuccessful_count}")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    main()

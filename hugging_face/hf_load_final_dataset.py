import argparse
import base64
import io
import logging
import os
from datasets import load_dataset
from io import BytesIO
from PIL import Image

import get_hf_features

skip_fields = [
    'original_caption'
]


def process_item(item: dict, dataset_name: str) -> None:
    """
    Process a single item from the dataset.
    Display its properties, show the image, and save it.
    """
    display_item_properties(item)

    image_data = item.get('image')
    if image_data:
        image = base64_to_image(image_data)
        # image.show()
        content_id = item.get('id')
        save_image(image, content_id, dataset_name)

        annotations = item.get('annotations', [])
        for annotation in annotations:
            annotation_item = annotation.get('annotation', {})
            annotation_field = annotation_item.get('original_field', '')

            if (annotation_field not in skip_fields):
                annotation_text = annotation_item.get('clean_text', '').replace('This image displays: ', '').strip()
                print(f'\nAnnotation for {content_id}:')
                print(f'{annotation_field}: {annotation_text}')
                # TODO: Valid item to train on
    else:
        logging.debug("No image found in the item.")


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

    ds_builder = get_hf_features.get_ds_builder(dataset_name)
    get_hf_features.print_splits(ds_builder)

    dataset = load_dataset(dataset_name, split='train', streaming=True)

    available_items = dataset.filter(lambda example: example.get('status') == 'available')

    for i, item in enumerate(available_items.take(num_items)):
        process_item(item, dataset_name)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    main()

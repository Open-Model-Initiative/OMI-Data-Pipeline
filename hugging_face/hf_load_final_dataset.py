import argparse
import base64
import io
import os
from datasets import load_dataset
from io import BytesIO
from PIL import Image

import get_hf_features


def process_item(item, dataset_name):
    """
    Process a single item from the dataset.
    Display its properties, show the image, and save it.
    """
    display_item_properties(item)

    image_data = item.get('image')
    if image_data:
        image = base64_to_image(image_data)
        # image.show()
        id = item.get('id')
        save_image(image, id, dataset_name)
    else:
        print("No image found in the item.")


def display_item_properties(item):
    """
    Display the properties of the given item.
    """
    print("Item properties:")
    for key, value in item.items():
        if key != 'image':
            print(f"{key}: {value}")


def base64_to_image(base64_string):
    img_data = base64.b64decode(base64_string)
    return Image.open(BytesIO(img_data))


def save_image(image, image_id, dataset_name):
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
    print(f"Image saved as {file_path}")


def main():
    parser = argparse.ArgumentParser(description="Load one of our private Hugging Face datasets locally.")
    parser.add_argument("-d", "--dataset_name", help="Name of the Hugging Face dataset")
    parser.add_argument("-n", "--num_items", type=int, default=1, help="Number of items to download (default: 1)")
    args = parser.parse_args()

    dataset_name = args.dataset_name
    num_items = args.num_items

    get_hf_features.get_ds_builder(dataset_name)

    dataset = load_dataset(dataset_name, split='train', streaming=True)

    available_items = dataset.filter(lambda example: example.get('status') == 'available')

    for i, item in enumerate(available_items.take(num_items)):
        process_item(item, dataset_name)


if __name__ == "__main__":
    main()

import argparse
import base64
import io
import os
from datasets import load_dataset
from io import BytesIO
from PIL import Image

import get_hf_features


def process_item(item):
    """
    Process a single item from the dataset.
    Display its properties, show the image, and save it.
    """
    display_item_properties(item)

    image_data = item.get('image')
    if image_data:
        image = base64_to_image(image_data)
        image.show()
        id = item.get('id')
        save_image(image, id)
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


def save_image(image, image_id):
    """
    Save the image to a folder called dataset_images.
    Create the folder if it doesn't exist.
    """
    folder_name = 'dataset_images'
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    file_name = f"{image_id}.png"
    file_path = os.path.join(folder_name, file_name)

    image.save(file_path)
    print(f"Image saved as {file_path}")


def main():
    parser = argparse.ArgumentParser(description="Load one of our private Hugging Face datasets locally.")
    parser.add_argument("-d", "--dataset_name", help="Name of the Hugging Face dataset")
    args = parser.parse_args()

    dataset_name = args.dataset_name

    get_hf_features.get_ds_builder(dataset_name)

    dataset = load_dataset(dataset_name, split='train', streaming=True)

    available_items = dataset.filter(lambda example: example.get('status') == 'available')

    num_items = 1

    for i, item in enumerate(available_items.take(num_items)):
        process_item(item)


if __name__ == "__main__":
    main()

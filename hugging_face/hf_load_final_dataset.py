import argparse
from datasets import load_dataset
from PIL import Image
import io


def process_item(item):
    """
    Process a single item from the dataset.
    Display its properties and show the image.
    """
    display_item_properties(item)
    display_item_image(item)


def display_item_properties(item):
    """
    Display the properties of the given item.
    """
    print("Item properties:")
    for key, value in item.items():
        if key != 'image':
            print(f"{key}: {value}")


def display_item_image(item):
    """
    Display the image from the given item.
    """
    image_data = item.get('image')
    # image_data = item.get('jpg')
    if image_data:
        image_data.show()
    else:
        print("No image found in the item.")


def main():
    parser = argparse.ArgumentParser(description="Process the first available item from a Hugging Face dataset.")
    parser.add_argument("dataset_name", help="Name of the Hugging Face dataset")
    args = parser.parse_args()

    dataset = load_dataset(args.dataset_name, split='train', streaming=True)

    available_items = dataset.filter(lambda example: example.get('status') == 'available')

    num_items = 1

    for i, item in enumerate(available_items.take(num_items)):
        process_item(item)


if __name__ == "__main__":
    main()

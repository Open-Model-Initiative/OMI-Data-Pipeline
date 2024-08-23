# Standard library imports
import io
import re

# Third-party library imports
import requests
from datasets import load_dataset
from PIL import Image


def parse_hf_url(hf_url):
    pattern = r"hf://([^[]+)\[['\"]([\w]+)['\"]]\[(\d+)]\[['\"]([\w]+)['\"]]"
    match = re.match(pattern, hf_url)

    if match:
        return {
            "name": match.group(1),
            "split": match.group(2),
            "id": int(match.group(3)),
            "column": match.group(4)
        }
    else:
        return None


def load_hugging_face_image(input: str) -> Image.Image:
    """
    Load an image from a Hugging Face dataset.
    """

    print(f"Loading Hugging Face Image from {input}")

    result = parse_hf_url(input)

    if result:
        dataset_name = result['name']
        split = result['split']
        id = result['id']
        column = result['column']
    else:
        raise ValueError("Invalid HF URL")

    dataset = load_dataset(dataset_name, split=split)

    if column not in dataset.features:
        raise ValueError(f"Dataset {dataset_name} does not contain a column with the name '{column}'")

    item = dataset[id][column]

    image_type = "unknown"

    if isinstance(item, dict) and 'bytes' in item:
        image_type = "dictionary"
    elif isinstance(item, Image.Image):
        image_type = "image"
    elif isinstance(item, str):
        image_type = "string"
    else:
        raise ValueError(f"Unknown image format: {type(item)}")

    if image_type == 'dictionary':
        # If it's a dict with 'bytes', convert to PIL Image
        image = Image.open(io.BytesIO(item['bytes']))
    elif image_type == 'image':
        # If it's already a PIL Image, use it directly
        image = item
    elif image_type == 'string':
        # If it's a string (possibly a file path), try to open it
        image = Image.open(item)
    else:
        # If we can't handle the image format throw an error
        raise ValueError(f"Unknown image format: {type(item)}")

    return image


def load_image_from_url(input: str) -> Image.Image:
    """
    Load an image from a given URL.
    """
    print(f"Loading image from URL {input}")

    response = requests.get(input, stream=True)
    response.raise_for_status()
    image = Image.open(response.raw)

    return image


def load_image(image_input: str) -> Image.Image:
    """
    Load an images from the given URL.
    """

    print("Loading image...")
    if image_input.startswith(('http://', 'https://')):
        image = load_image_from_url(image_input)
    elif image_input.startswith('hf://'):
        image = load_hugging_face_image(image_input)
    else:
        raise ValueError(f"Warning: Invalid image input: {input}")

    return image


def display_images_side_by_side(image_1, image_2, spacing=10):
    height_1 = image_1.height
    height_2 = image_2.height
    max_height = max(height_1, height_2)

    total_width = image_1.width + image_2.width + spacing

    combined_image = Image.new('RGB', (total_width, max_height), color='white')
    combined_image.paste(image_1, (0, (max_height - height_1) // 2))
    combined_image.paste(image_2, (image_1.width + spacing, (max_height - height_2) // 2))

    combined_image.show()


image_url = "https://media.newyorker.com/cartoons/63dc6847be24a6a76d90eb99/master/w_1160,c_limit/230213_a26611_838.jpg"
# TODO: Change format to support optional "configurations"/sub-datasets: https://huggingface.co/docs/datasets/load_hub#configurations
hf_url = "hf://huggan/wikiart['train'][0]['image']"

image_1 = load_image(image_url)
image_2 = load_image(hf_url)

display_images_side_by_side(image_1, image_2)

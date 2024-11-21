# SPDX-License-Identifier: Apache-2.0
from PIL import Image
from pathlib import Path
from urllib.request import urlopen
from io import BytesIO


def load_image(image_path, max_edge_size=1920) -> Image.Image:
    img = Image.open(image_path).convert("RGB")
    if max(img.size) > max_edge_size:
        print(
            f"Resizing image from {img.size} to fit within {max_edge_size}x{max_edge_size}"
        )
        img.thumbnail((max_edge_size, max_edge_size), Image.LANCZOS)
    return img


def load_images(image_paths, max_edge_size=1920) -> list[Image.Image]:
    return [load_image(image_path, max_edge_size) for image_path in image_paths]


def load_images_from_directory(directory, max_edge_size=1920) -> list[Image.Image]:
    if not Path(directory).exists():
        raise FileNotFoundError(f"Directory {directory} does not exist")
    return [
        load_image(image_path, max_edge_size)
        for image_path in Path(directory).glob("*.{jpg,png,jpeg}")
    ]


def load_img_from_url(url, max_edge_size=1920) -> Image.Image:
    img_byte_stream = BytesIO(urlopen(url).read())
    img = Image.open(img_byte_stream).convert("RGB")
    if max(img.size) > max_edge_size:
        img.thumbnail((max_edge_size, max_edge_size), Image.LANCZOS)
    return img


def get_image_prompt(
    images: list[Image.Image],
    instruction="Describe the image.",
    start_token="<s>",
    instruct_token="[INST]",
    image_token="[IMG]",
    end_token="[/INST]",
):
    """PROMPT = "<s>[INST] Describe the image. \n[IMG][/INST]"""
    return f"{start_token}{instruct_token} {instruction} \n{image_token * len(images)}{end_token}"


def load_png_images_from_directory(directory, max_edge_size=1920) -> dict[Image.Image]:
    directory_path = Path(directory)
    if not directory_path.exists():
        raise FileNotFoundError(f"Directory {directory} does not exist")

    png_files = list(directory_path.glob("*.png"))
    if not png_files:
        print(f"Warning: No PNG files found in {directory}")

    return {
        image_path.stem: load_image(image_path, max_edge_size)
        for image_path in png_files
    }

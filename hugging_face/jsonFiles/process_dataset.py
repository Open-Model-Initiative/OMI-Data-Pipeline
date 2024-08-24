import argparse
import json
import os

from io import BytesIO
from pathlib import Path

import requests
from PIL import Image


def process_jsonl(input_file):
    input_path = Path(input_file).resolve()
    input_dir = input_path.parent
    output_dir = input_dir.parent / f"{input_dir.name}_processed"
    output_dir.mkdir(exist_ok=True)

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


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process JSONL file and download images.")
    parser.add_argument("input_file", help="Path to the input JSONL file")
    args = parser.parse_args()

    process_jsonl(args.input_file)

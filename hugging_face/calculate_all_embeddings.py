# SPDX-License-Identifier: Apache-2.0
import argparse
import base64
import json
import logging
import shutil
import tempfile

from PIL import Image, UnidentifiedImageError
from io import BytesIO

from embeddings.image_embeddings import (
    calculate_image_embedding,
    instantiate_model,
    is_unique_image
)


def base64_to_image(base64_string: str) -> Image.Image:
    img_data = base64.b64decode(base64_string)
    return Image.open(BytesIO(img_data))


def process_all_images(dataset_file: str) -> None:
    embedding_model, model_name, collection = instantiate_model()

    processed_count = 0

    temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False)

    with open(dataset_file, 'r') as input_jsonl:
        for line in input_jsonl:
            data = json.loads(line)

            image_data = data.get('image')
            if image_data:
                image = base64_to_image(image_data)

                embedding = calculate_image_embedding(embedding_model, image)
                data['embeddings'].append({
                    "model": model_name,
                    "embedding": embedding.tolist()
                })

                image_id = str(processed_count)
                unique_image = is_unique_image(collection, embedding, image_id)
                data['is_unique'] = unique_image
            else:
                logging.debug("No image found in the item.")

            processed_count += 1

            json.dump(data, temp_file)
            temp_file.write('\n')

    temp_file.close()
    shutil.move(temp_file.name, dataset_file)


def main() -> None:
    parser = argparse.ArgumentParser(description="Process JSONL dataset file and calculate all image embeddings.")
    parser.add_argument("-f", "--dataset_file", help="Path to the input JSONL file")
    args = parser.parse_args()

    process_all_images(args.dataset_file)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    main()

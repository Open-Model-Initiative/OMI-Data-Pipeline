import os
import torch
from PIL import Image
from transformers import AutoTokenizer
from vllm import LLM, ModelRegistry, SamplingParams
from vllm.model_executor.models import _MULTIMODAL_MODELS
from aria.vllm.aria import AriaForConditionalGeneration
import matplotlib.pyplot as plt
import json
import pandas as pd
from pathlib import Path

# from prompt import STABLE_PROMPT
from prompt import COT_DENSE_CAPTION as STABLE_PROMPT
from datetime import datetime
import argparse
from tqdm import tqdm
import codecs

# Register Aria model
ModelRegistry.register_model(
    "AriaForConditionalGeneration", AriaForConditionalGeneration
)
_MULTIMODAL_MODELS["AriaForConditionalGeneration"] = (
    "aria",
    "AriaForConditionalGeneration",
)


def resize_image(image, max_size=1500):
    """Resize image so that the longest edge is no more than max_size."""
    width, height = image.size
    if max(width, height) > max_size:
        if width > height:
            new_width = max_size
            new_height = int(height * (max_size / width))
        else:
            new_height = max_size
            new_width = int(width * (max_size / height))
        image = image.resize((new_width, new_height), Image.LANCZOS)
    return image


def load_model_and_tokenizer(model_id_or_path="rhymes-ai/Aria", gpu_id=0):
    os.environ["CUDA_VISIBLE_DEVICES"] = str(gpu_id)

    model = LLM(
        model=model_id_or_path,
        tokenizer=model_id_or_path,
        dtype="bfloat16",
        limit_mm_per_prompt={"image": 256},
        enforce_eager=True,
        trust_remote_code=True,
        max_model_len=8192,
    )

    tokenizer = AutoTokenizer.from_pretrained(
        model_id_or_path, trust_remote_code=True, use_fast=False
    )

    return model, tokenizer


def process_image(image_path, split_image=False, max_size=1500):
    image = Image.open(image_path).convert("RGB")
    image = resize_image(image, max_size)
    return image, {"image": [image], "max_image_size": 980, "split_image": split_image}


def generate_response(model, tokenizer, image_data, prompt):
    messages = [
        {
            "role": "user",
            "content": [
                {"text": None, "type": "image"},
                {"text": prompt, "type": "text"},
            ],
        }
    ]
    text = tokenizer.apply_chat_template(messages, add_generation_prompt=True)

    with torch.inference_mode(), torch.cuda.amp.autocast(dtype=torch.bfloat16):
        outputs = model.generate(
            {
                "prompt_token_ids": text,
                "multi_modal_data": image_data,
            },
            sampling_params=SamplingParams(
                max_tokens=4096, top_k=1, stop=["<|im_end|>"]
            ),
        )
        for o in outputs:
            generated_tokens = o.outputs[0].token_ids
            result = tokenizer.decode(generated_tokens)

    return result


def extract_code(result):
    return result.split("```python")[-1].split("```")[0]


def extract_json(result):
    json_string = result.split("```json")[-1].split("```")[0]
    return json.loads(json_string)


def clean_prompt(prompt):
    # Remove <|im_end|> token and any trailing whitespace
    prompt = prompt.replace("<|im_end|>", "").strip()

    # Remove all double quotes
    prompt = prompt.replace('"', "")

    # Remove "Prompt:", "**Prompt:**", "Text Description:", or "**Text Description:**" from the start if it exists
    prefixes = [
        "Prompt:",
        "**Prompt:**",
        "Text Description:",
        "**Text Description:**",
        "Text description",
        "**Text description**",
        "Prompt:",
        "**Prompt:**",
    ]
    for prefix in prefixes:
        if prompt.startswith(prefix):
            prompt = prompt[len(prefix):].strip()
            break

    # If "Final Prompt:", "**Final Prompt**", "Text Description:", or "**Text Description:**" exists, remove everything before it
    markers = [
        "Final Prompt:",
        "**Final Prompt:**",
        "Text Description:",
        "**Text Description:**",
        "Final prompt:",
        "**Final prompt:**",
        "Prompt:",
        "**Prompt:**",
    ]
    for marker in markers:
        if marker in prompt:
            prompt = prompt.split(marker)[-1].strip()
            break

    # Remove any newlines and replace with a space
    prompt = " ".join(prompt.split())

    return prompt


def process_folder(model, tokenizer, input_folder, output_dir="./output"):
    results = []
    input_folder = Path(input_folder)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    for image_file in input_folder.glob("*"):
        if image_file.suffix.lower() in [".jpg", ".jpeg", ".png", ".bmp", ".gif"]:
            image, image_data = process_image(str(image_file), split_image=False)
            result = generate_response(model, tokenizer, image_data, STABLE_PROMPT)

            # Clean and extract the generated prompt
            generated_prompt = clean_prompt(result)

            results.append(
                {"image_path": str(image_file), "generated_prompt": generated_prompt}
            )

    # Create a DataFrame and save as parquet and csv
    df = pd.DataFrame(results)
    parquet_path = output_dir / "image_prompts.parquet"
    csv_path = output_dir / "image_prompts.csv"
    df.to_parquet(parquet_path)
    df.to_csv(csv_path, index=False)
    print(f"Results saved to {parquet_path} and {csv_path}")


def process_folder_batch(
    model,
    tokenizer,
    input_folder,
    output_dir="./output",
    batch_size=10,
    clean_prompt_flag=False,
    run_name=None,
):
    input_folder = Path(input_folder)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Recursively search for image files
    image_files = []
    for ext in [".jpg", ".jpeg", ".png", ".bmp", ".gif", ".webp"]:
        image_files.extend(input_folder.rglob(f"*{ext}"))
        image_files.extend(input_folder.rglob(f"*{ext.upper()}"))

    # Create a tqdm progress bar for all images
    pbar = tqdm(total=len(image_files), desc="Processing images")

    # Generate timestamp, folder name, and run name for output files
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    folder_name = input_folder.name
    run_suffix = f"_{run_name}" if run_name else ""
    base_filename = f"{folder_name}{run_suffix}_image_prompts_{timestamp}"
    parquet_path = output_dir / f"{base_filename}.parquet"
    csv_path = output_dir / f"{base_filename}.csv"

    all_results = []

    for i in range(0, len(image_files), batch_size):
        batch_files = image_files[i: i + batch_size]
        batch_image_data = []

        for image_file in batch_files:
            _, image_data = process_image(
                str(image_file), split_image=False, max_size=1500
            )
            batch_image_data.append(image_data)

        # Prepare batch prompts
        batch_prompts = [STABLE_PROMPT] * len(batch_files)

        # Generate responses for the batch
        batch_results = generate_response_batch(
            model, tokenizer, batch_image_data, batch_prompts
        )

        batch_data = []
        for file, result in zip(batch_files, batch_results):
            generated_prompt = clean_prompt(result) if clean_prompt_flag else result
            batch_data.append(
                {
                    "image_path": str(file.relative_to(input_folder)),
                    "generated_prompt": generated_prompt,
                }
            )

        all_results.extend(batch_data)

        # Create a DataFrame for the batch and append to the CSV file
        df_batch = pd.DataFrame(batch_data)
        if i == 0:
            df_batch.to_csv(
                csv_path, index=False, mode="w", header=True, encoding="utf-8-sig"
            )
        else:
            df_batch.to_csv(
                csv_path, index=False, mode="a", header=False, encoding="utf-8-sig"
            )

        # Update the progress bar
        pbar.update(len(batch_files))

    # Close the progress bar
    pbar.close()

    # Save all results to parquet file
    df_all = pd.DataFrame(all_results)
    df_all.to_parquet(parquet_path, index=False)

    # Save all results to CSV file with proper encoding
    with codecs.open(csv_path, "w", encoding="utf-8-sig") as f:
        df_all.to_csv(f, index=False)

    print(f"Results saved incrementally to {csv_path}")
    print(f"Final results saved to {parquet_path}")


def generate_response_batch(model, tokenizer, batch_image_data, batch_prompts):
    batch_messages = [
        [
            {
                "role": "user",
                "content": [
                    {"text": None, "type": "image"},
                    {"text": prompt, "type": "text"},
                ],
            }
        ]
        for prompt in batch_prompts
    ]

    batch_texts = [
        tokenizer.apply_chat_template(messages, add_generation_prompt=True)
        for messages in batch_messages
    ]

    with torch.inference_mode(), torch.cuda.amp.autocast(dtype=torch.bfloat16):
        outputs = model.generate(
            [
                {
                    "prompt_token_ids": tokenizer.encode(text),
                    "multi_modal_data": image_data,
                }
                for text, image_data in zip(batch_texts, batch_image_data)
            ],
            sampling_params=SamplingParams(
                max_tokens=4096, stop=["<|im_end|>"], temperature=1.1, top_p=0.9
            ),
        )

    results = []
    for output in outputs:
        generated_text = output.outputs[0].text
        results.append(generated_text)

    return results


def main():
    parser = argparse.ArgumentParser(
        description="Process images and generate prompts using Aria model."
    )
    parser.add_argument(
        "--input_folder",
        type=str,
        required=True,
        help="Path to the folder containing input images",
    )
    parser.add_argument(
        "--output_dir",
        type=str,
        default="./output",
        help="Path to the output directory",
    )
    parser.add_argument(
        "--batch_size", type=int, default=4, help="Batch size for processing images"
    )
    parser.add_argument(
        "--clean_prompt", action="store_true", help="Enable prompt cleaning"
    )
    parser.add_argument("--run_name", type=str, default=None, help="Name for this run")
    args = parser.parse_args()

    model, tokenizer = load_model_and_tokenizer()

    # Process a folder of images using batch inference
    process_folder_batch(
        model,
        tokenizer,
        args.input_folder,
        output_dir=args.output_dir,
        batch_size=args.batch_size,
        clean_prompt_flag=args.clean_prompt,
        run_name=args.run_name,
    )


if __name__ == "__main__":
    main()

# SPDX-License-Identifier: Apache-2.0
import os
import asyncio
from dotenv import load_dotenv
from odr_caption.agents.ImageCaptioner import ImageCaptioner
from odr_caption.utils.logger import logger

load_dotenv()

# Set vLLM's API server URL
vllm_api_base = "http://localhost:32000/v1"


async def main():
    cwd = os.getcwd()
    image_path = f"{cwd}/test/test_images/test_image_1.png"

    # Initialize ImageCaptioner
    captioner = ImageCaptioner(
        vllm_server_url=vllm_api_base,
        model_name="Qwen/Qwen2-7B-Instruct",
        max_tokens=2048,
        temperature=0.35,
    )

    # Define system message and prompt
    system_message = "You are a helpful assistant."
    prompt = "What is the text in the illustration?"

    # Caption the image
    response = await captioner.caption_image(image_path, system_message, prompt)

    # Print the response
    logger.info(f"Chat response: {response}")
    if response.choices:
        logger.info(f"Generated caption: {response.choices[0].message.content}")


if __name__ == "__main__":
    asyncio.run(main())

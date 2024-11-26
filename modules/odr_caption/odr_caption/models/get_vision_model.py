# SPDX-License-Identifier: Apache-2.0
import torch
from transformers import (
    LlavaForConditionalGeneration,
    Qwen2VLForConditionalGeneration,
    PreTrainedModel,
    AutoProcessor,
)
import outlines
import os
from outlines.models.transformers_vision import TransformersVision
from typing import Type
from odr_caption.utils.logger import logger


class VisionModel:
    def __init__(self, model_name: str, model_class: Type[PreTrainedModel]):
        self.model_name = model_name
        self.model_class = model_class
        self.processor = AutoProcessor.from_pretrained(model_name)
        self.model = self.setup_model()

    def setup_model(self):
        if "AWQ" in self.model_name:
            torch_dtype = torch.float16
        else:
            torch_dtype = torch.bfloat16
        model_kwargs = {
            "torch_dtype": torch_dtype,
            "device_map": "auto",
        }
        processor_kwargs = {
            "device": "cuda",
        }
        model = outlines.models.transformers_vision(
            self.model_name,
            model_class=self.model_class,
            model_kwargs=model_kwargs,
            processor_kwargs=processor_kwargs,
        )
        return model

    def format_instruction(self, instruction: str, images: list):
        logger.info(f"Formatting instruction: {instruction}")
        logger.info(f"Images: {images}")
        return self.processor.apply_chat_template(
            [
                {
                    "role": "user",
                    "content": [{"type": "text", "text": instruction}]
                    + [{"type": "image", "image": ""} for image in images],
                }
            ],
            add_generation_prompt=True,
        )


class PixtralVisionModel(VisionModel):
    img_token = "[IMG]"
    pixtral_format = """
        <s>[INST]
        {instruction}
        \n{img_tokens}[/INST]
        """

    def __init__(
        self,
        model_name: str = "unsloth/Pixtral-12B-2409",
        model_class: Type[PreTrainedModel] = LlavaForConditionalGeneration,
    ):
        super().__init__(model_name, model_class)

    def format_instruction(self, instruction: str, images: list):
        img_tokens = [self.img_token for _ in images]
        return self.pixtral_format.format(
            instruction=instruction, img_tokens=img_tokens
        )


def get_vision_model() -> tuple[TransformersVision, AutoProcessor]:
    model_name = os.getenv("ODR_VISION_MODEL", "unsloth/Pixtral-12B-2409")
    logger.info(f"Using model: {model_name}")
    # Select appropriate model class based on model name
    if "Qwen" in model_name:
        logger.info("Using Qwen2VLForConditionalGeneration")
        model_class = Qwen2VLForConditionalGeneration
        model = VisionModel(model_name, model_class)
    elif "Llama" in model_name:
        logger.info("Using MllamaForConditionalGeneration")
        logger.error("MllamaForConditionalGeneration is not yet supported")
        raise NotImplementedError("MllamaForConditionalGeneration is not yet supported")
    else:
        logger.info("Using LlavaForConditionalGeneration")
        model_class = LlavaForConditionalGeneration
        model = PixtralVisionModel(model_name, model_class)

    return model

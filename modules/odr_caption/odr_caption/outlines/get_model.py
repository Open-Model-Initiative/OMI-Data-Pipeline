from vllm import LLM
from vllm.sampling_params import SamplingParams
import torch
from transformers import (
    LlavaForConditionalGeneration,
    Qwen2VLForConditionalGeneration,
    PreTrainedModel,
)
import outlines

from dataclasses import dataclass
from typing import Type


@dataclass
class VisionModel:
    model_name: str
    model_class: Type[PreTrainedModel]
    image_token: str
    use_case: str


default_vision_model = VisionModel(
    model_name="mistral-community/pixtral-12b",
    model_class=LlavaForConditionalGeneration,
    image_token="[IMG]",
    use_case="detailed visual reasoning",
    # config_kwargs={
    #     "torch_dtype": torch.bfloat16,
    #     "attn_implementation": "flash_attention_2",
    #     "device_map": "auto",
    #     "load_in_8bit": True,
    #     "trust_remote_code": True,
    # },
)


def get_vision_model(model: VisionModel = default_vision_model):
    model_kwargs = {
        "torch_dtype": torch.bfloat16,
        # "attn_implementation": "flash_attention_2",
        "device_map": "auto",
    }
    processor_kwargs = {
        "device": "cuda",
    }

    model = outlines.models.transformers_vision(
        model.model_name,
        model_class=model.model_class,
        model_kwargs=model_kwargs,
        processor_kwargs=processor_kwargs,
    )
    return model


def get_text_model(model_name="Qwen/Qwen2.5-14B-Instruct-GPTQ-Int8", context=8096):
    llm = LLM(
        model=model_name,
        max_model_len=8096,
        dtype="bfloat16",
        gpu_memory_utilization=0.9,
        trust_remote_code=True,
        # tokenizer_mode="mistral"
    )

    model = outlines.models.VLLM(llm)
    return model


def get_default_params() -> SamplingParams:
    return SamplingParams(
        temperature=0.7,
        min_p=0.9,
        max_tokens=4096,
    )


def get_vision_model_list():
    return [
        "mistral-community/pixtral-12b",
        "Qwen/Qwen2-VL-7B-Instruct-GPTQ-Int8",
        "Qwen/Qwen2-VL-2B-Instruct",
        "Qwen/Qwen2-VL-2B-Instruct-GPTQ-Int8",
    ]


def get_text_model_list():
    return [
        "anthracite-org/magnum-v4-12b",
        "Qwen/Qwen2.5-14B-Instruct-GPTQ-Int8",
        "mistralai/Mistral-Nemo-Instruct-2407",
    ]

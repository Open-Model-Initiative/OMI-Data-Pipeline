# SPDX-License-Identifier: Apache-2.0
from vllm import LLM
from vllm.sampling_params import SamplingParams
import outlines
import os


def get_text_model(context=8096):
    model_name = os.getenv("ODR_TEXT_MODEL", "Qwen/Qwen2.5-14B-Instruct-GPTQ-Int8")
    llm = LLM(
        model=model_name,
        max_model_len=8096,
        dtype="bfloat16",
        gpu_memory_utilization=0.9,
        trust_remote_code=True,
    )

    model = outlines.models.VLLM(llm)
    return model


def get_default_params() -> SamplingParams:
    return SamplingParams(
        temperature=0.7,
        min_p=0.9,
        max_tokens=4096,
    )

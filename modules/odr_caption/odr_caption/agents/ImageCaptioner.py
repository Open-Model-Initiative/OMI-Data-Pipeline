import base64
from typing import Optional, Union
from PIL import Image
import io
import time
import asyncio
from openai import AsyncOpenAI
from odr_caption.utils.logger import logger
from odr_caption.schemas.vllm_schemas import VLLMResponse, VLLMRequest, Interaction
from odr_caption.utils.message_logger import MessageLogger


class ImageCaptioner:
    def __init__(
        self,
        vllm_server_url: str,
        model_name: str,
        message_logger: Optional[MessageLogger] = None,
        max_tokens: int = 2048,
        temperature: float = 0.35,
        max_size: int = 1280,
        repetition_penalty: float = 1.0,
    ):
        self.client = AsyncOpenAI(api_key="EMPTY", base_url=vllm_server_url)
        self.model_name = model_name
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.max_size = max_size
        self.repetition_penalty = repetition_penalty
        self.message_logger = message_logger
        logger.info(
            f"ImageCaptioner initialized with model_name: {self.model_name} and base_url: {vllm_server_url}"
        )

    def encode_image(self, image_path: str) -> str:
        with Image.open(image_path) as img:
            img = img.convert("RGB")

            # Resize image if the longest edge is greater than max_size
            original_size = img.size
            img.thumbnail((self.max_size, self.max_size))
            resized_size = img.size

            if original_size != resized_size:
                logger.info(f"Image resized from {original_size} to {resized_size}")

            buffered = io.BytesIO()
            img.save(buffered, format="PNG")
            return base64.b64encode(buffered.getvalue()).decode("utf-8")

    async def caption_image(
        self, image_path: str, system_message: str, prompt: Optional[str] = None
    ) -> Union[VLLMResponse, str]:
        timestamp_start = time.time()
        encoded_image = self.encode_image(image_path)
        messages = [
            {"role": "system", "content": system_message},
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt or "Describe this image in detail.",
                    },
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/png;base64,{encoded_image}"},
                    },
                ],
            },
        ]

        try:
            response = await self.client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                max_tokens=self.max_tokens,
                temperature=self.temperature,
                presence_penalty=self.repetition_penalty,
            )

            vllm_response = self._convert_to_vllm_response(response)
            timestamp_end = time.time()
            duration = timestamp_end - timestamp_start

            self._log_interaction(
                messages, vllm_response, timestamp_start, timestamp_end, duration
            )
            return vllm_response

        except Exception as e:
            logger.error(f"Error captioning image: {e}", exc_info=True)
            error_response = self._create_error_response(str(e))
            timestamp_end = time.time()
            duration = timestamp_end - timestamp_start
            self._log_interaction(
                messages, error_response, timestamp_start, timestamp_end, duration
            )
            return error_response

    def _convert_to_vllm_response(self, openai_response) -> VLLMResponse:
        return VLLMResponse(
            id=openai_response.id,
            object=openai_response.object,
            created=openai_response.created,
            model=openai_response.model,
            choices=[
                {
                    "index": choice.index,
                    "message": {
                        "role": choice.message.role,
                        "content": choice.message.content,
                    },
                    "finish_reason": choice.finish_reason,
                }
                for choice in openai_response.choices
            ],
            usage={
                "prompt_tokens": openai_response.usage.prompt_tokens,
                "completion_tokens": openai_response.usage.completion_tokens,
                "total_tokens": openai_response.usage.total_tokens,
            },
        )

    def _create_error_response(self, error_message: str) -> VLLMResponse:
        return VLLMResponse(
            id="error",
            object="chat.completion",
            created=int(time.time()),
            model=self.model_name,
            choices=[
                {
                    "index": 0,
                    "message": {
                        "role": "assistant",
                        "content": f"Error: {error_message}",
                    },
                    "finish_reason": "error",
                }
            ],
            usage={"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0},
        )

    def _log_interaction(
        self,
        request,
        response: VLLMResponse,
        timestamp_start: float,
        timestamp_end: float,
        duration: float,
    ):
        if self.message_logger:
            interaction = Interaction(
                request=VLLMRequest(messages=request, model=self.model_name),
                response=response,
                timestamp_start=int(timestamp_start),
                timestamp_end=int(timestamp_end),
                duration=duration,
            )
            self.message_logger.log_interaction(interaction)

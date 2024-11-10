import json
from typing import List
from copy import deepcopy
from odr_caption.schemas.vllm_schemas import Interaction, VLLMRequest, VLLMResponse
from odr_caption.utils.logger import logger
import os
import logging


def configure_logger(output_log_dir: str) -> logging.Logger:
    logger.setLevel(logging.DEBUG)  # Set to DEBUG for detailed logs
    output_log_path = f"{output_log_dir}/graph_extraction.log"

    # Ensure the log directory exists
    os.makedirs(output_log_dir, exist_ok=True)

    # Create handlers
    c_handler = logging.StreamHandler()
    f_handler = logging.FileHandler(output_log_path)

    c_handler.setLevel(logging.INFO)
    f_handler.setLevel(logging.DEBUG)

    # Create formatters and add to handlers
    c_format = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    f_format = logging.Formatter("%(asctime)s - %(levelname)s - %(name)s - %(message)s")

    c_handler.setFormatter(c_format)
    f_handler.setFormatter(f_format)

    # Add handlers to the logger
    if not logger.hasHandlers():
        logger.addHandler(c_handler)
    logger.addHandler(f_handler)

    return logger


class MessageLogger:
    def __init__(self, output_dir: str):
        self.output_dir = output_dir
        self.interactions: List[Interaction] = []

    def _sanitize_request(self, request: VLLMRequest) -> VLLMRequest:
        sanitized_request = deepcopy(request.dict())
        for message in sanitized_request.get("messages", []):
            if isinstance(message.get("content"), list):
                for item in message["content"]:
                    if isinstance(item, dict) and item.get("type") == "image_url":
                        item["image_url"] = {"image_url": "[HIDDEN]"}
        return VLLMRequest(**sanitized_request)

    def log_interaction(self, interaction: Interaction):
        sanitized_request = self._sanitize_request(interaction.request)
        interaction = Interaction(
            request=sanitized_request,
            response=interaction.response,
            timestamp_start=interaction.timestamp_start,
            timestamp_end=interaction.timestamp_end,
            duration=interaction.duration,
        )
        self.interactions.append(interaction)
        logger.debug(f"Logged interaction: {interaction.model_dump_json(indent=2)}")

    def export_interactions(self, file_path: str = None):
        if not file_path:
            file_path = f"{self.output_dir}/message_interactions.json"
        try:
            sanitized_interactions = [
                interaction.dict(by_alias=True) for interaction in self.interactions
            ]
            for interaction in sanitized_interactions:
                interaction["request"] = self._sanitize_request(
                    VLLMRequest(**interaction["request"])
                ).model_dump()

            with open(file_path, "w") as f:
                json.dump(sanitized_interactions, f, indent=4)
            logger.info(f"Message interactions exported to {file_path}")
        except Exception as e:
            logger.error(f"Error exporting message interactions: {e}")

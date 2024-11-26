# SPDX-License-Identifier: Apache-2.0
from PIL import Image
import time
import outlines
import outlines.samplers
from odr_caption.utils.logger import logger

from odr_caption.models.get_vision_model import (
    VisionModel,
    get_vision_model,
)
from odr_caption.outlines.caption import instruction
from odr_caption.schemas.caption import ImageData


class StructuredCaption:
    def __init__(self):
        start_total = time.time()
        logger.info(
            "Initializing StructuredCaption"
        )

        # Time model loading
        start_model = time.time()
        self.model: VisionModel = get_vision_model()
        model_time = time.time() - start_model
        logger.info(f"Model initialization completed in {model_time:.2f} seconds")

        # Time decoder generation
        start_decoder = time.time()
        sampler = outlines.samplers.multinomial(temperature=0.5)
        logger.info("Generating decoder...")
        self.generator = outlines.generate.json(self.model.model, ImageData, sampler=sampler)
        decoder_time = time.time() - start_decoder
        logger.info(f"Decoder generation completed in {decoder_time:.2f} seconds")

        total_time = time.time() - start_total
        logger.info(f"Total StructuredCaption initialization took {total_time:.2f} seconds")
        logger.debug("StructuredCaption initialized successfully")

    def __call__(
        self, image: Image.Image, instruction: str = instruction, **kwargs
    ) -> ImageData:
        logger.info("Generating caption for image")

        instruction = self.model.format_instruction(instruction, [image])
        logger.debug(f"Instruction: {instruction}")
        try:
            result = self.generator(
                instruction,
                [image],
            )
            logger.debug("Caption generated successfully")
            return result
        except Exception as e:
            logger.error(f"Error generating caption: {str(e)}", exc_info=True)
            raise

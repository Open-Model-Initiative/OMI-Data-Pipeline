from PIL import Image
import time
import outlines
import outlines.samplers
from odr_caption.utils.logger import logger

from odr_caption.outlines.get_model import (
    VisionModel,
    get_vision_model,
    default_vision_model,
)
from odr_caption.outlines.caption import pixtral_instruction
from outlines.generate.api import SamplingParameters
from odr_caption.schemas.caption import ImageData


class StructuredCaption:
    def __init__(self, model_config: VisionModel = default_vision_model):
        start_total = time.time()
        self.model_config = model_config
        logger.info(
            f"Initializing StructuredCaption with model: {model_config.model_name}"
        )

        # Time model loading
        start_model = time.time()
        self.model = get_vision_model(model_config)
        model_time = time.time() - start_model
        logger.info(f"Model initialization completed in {model_time:.2f} seconds")

        # Time decoder generation
        start_decoder = time.time()
        sampler = outlines.samplers.multinomial(temperature=0.5)
        logger.info("Generating decoder...")
        self.generator = outlines.generate.json(self.model, ImageData, sampler=sampler)
        decoder_time = time.time() - start_decoder
        logger.info(f"Decoder generation completed in {decoder_time:.2f} seconds")

        total_time = time.time() - start_total
        logger.info(f"Total StructuredCaption initialization took {total_time:.2f} seconds")
        logger.debug("StructuredCaption initialized successfully")

    def __call__(
        self, image: Image.Image, instruction: str = pixtral_instruction, **kwargs
    ) -> ImageData:
        logger.info("Generating caption for image")

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

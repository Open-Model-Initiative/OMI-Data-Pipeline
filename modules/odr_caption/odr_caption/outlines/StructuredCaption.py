from PIL import Image
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
        self.model_config = model_config
        logger.info(
            f"Initializing StructuredCaption with model: {model_config.model_name}"
        )
        self.model = get_vision_model(model_config)
        logger.info("Model initialized successfully. Generating guided decoder...")

        sampler = outlines.samplers.multinomial(temperature=0.5)
        self.generator = outlines.generate.json(self.model, ImageData, sampler=sampler)
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

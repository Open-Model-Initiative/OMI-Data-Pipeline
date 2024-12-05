# SPDX-License-Identifier: Apache-2.0
import json
import re
from PIL import Image
from odr_caption.outlines.vision import load_images
from typing import List, Dict, Any
from pathlib import Path
import os
from outlines.generate.api import GenerationParameters, SamplingParameters
from tqdm import tqdm
from transformers import AutoProcessor


class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, str):
            # Remove escaped unicode characters
            return re.sub(r"\\u[0-9a-fA-F]{4}", "", obj)
        return super().default(obj)


instruction = """<Task>You are a structured image analysis agent. Generate comprehensive tag list, caption, and dense caption for an image classification system.</Task>
<TagCategories requirement="You should generate a minimum of 1 tag for each category." confidence="Confidence score for the tag, between 0 (exclusive) and 1 (inclusive).">
- Entity : The content of the image, including the objects, people, and other elements.
- Relationship : The relationships between the entities in the image.
- Style : The style of the image, including the color, lighting, and other stylistic elements.
- Attribute : The most important attributes of the entities and relationships in the image.
- Composition : The composition of the image, including the arrangement of elements.
- Contextual : The contextual elements of the image, including the background, foreground, and other elements.
- Technical : The technical elements of the image, including the camera angle, lighting, and other technical details.
- Semantic : The semantic elements of the image, including the meaning of the image, the symbols, and other semantic details.
<Examples note="These show the expected format as an abstraction.">
{
  "tags_list": [
    {
      "tag": "subject 1",
      "category": "Entity",
      "confidence": 0.98
    },
    {
      "tag": "subject 2",
      "category": "Entity",
      "confidence": 0.95
    },
    {
      "tag": "subject 1 runs from subject 2",
      "category": "Relationship",
      "confidence": 0.90
    },
  ]
}
</Examples>
</TagCategories>
<ShortCaption note="The short caption is a concise single sentence caption of the image content with a maximum length of 100 characters.">
<Verification note="The verification identifies issues with the extracted tags and simple caption where the tags do not match the visual content you can actually see. Be a critic.">
<DenseCaption note="The dense caption is a descriptive but grounded narrative paragraph of the image content. Only reference items you are confident you can see in the image.It uses straightforward confident and clear language without overt flowery prose. It incorporates elements from each of the tag categories to provide a broad dense caption">"""

NO_ARTIST = """Here is a guide to make prompts for generative AI stable diffusion models text to image. Only reply with only the prompt you are asked to create.
1. **Text Description**: Start with a detailed textual description of the image you want to generate. This description should be as specific as possible to guide the AI in creating the image. The more descriptive your prompt, the better, as anything not specified will be randomly defined by the AI.

2. **Image Style**: Define the style of your image by describing specific stylistic elements such as color palettes, brushwork, texture, composition techniques, and thematic motifs. For example, you might specify a vibrant color scheme with bold brushstrokes, a minimalist design with geometric shapes, or a dreamy atmosphere with soft lighting and ethereal elements.

3. **Subject**: Describe each subject well. If necessary, list the number of individuals.

4. **Environment**: Put your subjects in an environment to give context to your image.

5. **Lighting**: Specify the time of day to guide the lighting, colors, and contrasts of the image.

6. **Angle of View**: You can specify the viewing angle of the image, such as "Wide-Angle Shot", "Medium-Shot", or "Close-Up".

7. **Final Prompt**: Combine the text description, parameters, and the additional elements (image style, subject, environment, lighting, angle of view) to create the final prompt.

**Additional Tips**:

- Describe unique stylistic elements or combine different styles for a new aesthetic (e.g., "a serene landscape with impressionistic brushwork and vibrant colors").
- Specify composition, camera settings, and lighting to create a visually dramatic image.
- Use various art styles, mediums, and scene descriptors to guide the model.
- Combine well-defined concepts in unique ways (e.g., "cyberpunk shinto priest with neon accents and traditional garments").
- Describe the style through detailed characteristics instead of referencing specific artists.
- Be ultra-descriptive in your prompts. The more specific and detailed your prompt, the better the AI can generate an image that aligns with your vision.
- Experiment with different parameters and their values to get the desired output.

Now analyze the provided image and generate a prompt for it. Aim for a prompt of around 150-300 words. Just provide the prompt without saying anything else
Prompt:
"""

COT_DENSE_CAPTION = """Provide a detailed description of the image by listing each element step by step within the <Analysis> tags. Within <Analysis>, include specific details such as objects, subjects, their attributes (e.g., color, size, texture), their relationships, and positions in the image.

Scrutinize your analysis within the <Scrutiny> tags. Within <Scrutiny>, evaluate the accuracy and completeness of the <Analysis>, ensuring no elements are imagined that are not present in the image. Additionally, infer and describe stylistic elements, environment, lighting, and composition if you are confident they are present.

Include an inferred style description within the <Inferred_Style> tags. Within <Inferred_Style>, detail the artistic style elements such as color palette, brushwork or texture, composition techniques, thematic motifs, and any other relevant stylistic characteristics observed in the image.

Do not imagine any physical elements that are not present in the image. Ensure that the dense caption does not introduce any new elements and strictly reflects the analyzed content.

Then include your dense grounded image caption within the <Dense_Caption> tags. Within <Dense_Caption>, provide a rich and comprehensive description that incorporates aesthetic information such as color schemes, lighting quality, texture, mood, and overall composition, based solely on the elements identified in the <Analysis>.

Example Structure:
<Analysis>
- Element 1: Description
- Element 2: Description
- ...
</Analysis>
<Inferred_Style>
- Description of color palette
- Description of brushwork or texture
- Description of composition techniques
- Description of thematic motifs
- Additional stylistic characteristics
</Inferred_Style>
<Scrutiny>
- Evaluation of Analysis
- Inferred Stylistic Elements
- Inferred Environment, Lighting, Composition
</Scrutiny>
<Dense_Caption>
- Comprehensive descriptive caption with aesthetic details
- Includes no details not already referenced or judged to not be valid
</Dense_Caption>

"""

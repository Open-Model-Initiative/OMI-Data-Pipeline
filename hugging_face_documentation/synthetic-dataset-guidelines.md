# Synthetic Dataset Guidelines

While synthetic (AI created) data can be valuable for training models, it’s important that AI created data be curated to prevent current problems from being propagated to newer models.

With this in mind the OMI would like to offer some guidelines on what image contributions will be most useful for our training purposes.

## Literal resolution (larger is good but no fixed requirement)
- Minimum size of 1024x1024 is suggested, but not required. Smaller images may be useful for a variety of purposes.
- ‘Visual Resolution’ (see below) is more important.

## Visual ‘resolution’
- Detail level should be appropriate to the image and style. When viewed at a reasonable size, important details shouldn’t be muddy or indistinct.
- For example, a smaller image of a person with properly detailed eyes and facial features is preferable to a larger image with a muddy face/eyes.
- Does not apply to details that are intentionally blurry/indistinct. Includes things such as depth of field, art styles that are sketchy/loose, loss of detail towards the periphery of the image that directs attention towards the image focus, etc

## Anatomical/physical ‘rationality’ (abstract should be intentional)
- The image should make sense physically. Objects should not disappear, shift position, or morph into something else when interrupted or coming into contact with another object.
- Anatomy should be mostly correct and consistent, subject to image/art style.
- Intentionally abstract elements and images are fine, but they should be a feature of the image rather than an accident

## Lack of AI artifacts
- Avoid submitting images with common artifacts such as incorrect numbers of fingers, garbled text, or unidentifiable objects.

## Variety
- While AI makes it easy to generate large numbers of images of the same subject, avoid submitting many images generated with the same prompt and pick a few of the best ones. (suggest guideline of maximum 3 with same prompt?)
- If generating sets of related images with variations in pose, point of view, etc, more images can be submitted but limit the number of extremely similar images submitted.

# In Summary
## What we want:
- Your best finished and polished images that are mostly free of AI Artifacting (either through cherry picking images, hiresfix, or inpainting/retouching)
- Images with a variety of subjects, points of view, and styles

## What we don’t want:
- The unfiltered contents of your AI images folder
- Large amounts of images generated using the same prompt
- Images with AI artifacts such as distorted anatomy, extra fingers, or indistinct important details.

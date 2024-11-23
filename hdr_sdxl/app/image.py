# SPDX-License-Identifier: Apache-2.0
import os
import json
import cv2
import numpy as np
from app.logger import log


def adjust_gamma(image, gamma: float = 2.2):
    image = (image.astype(np.float32) / 65535.0) ** (1.0 / gamma)
    image = (65535.0 * image).astype(np.uint16)
    return image


def to_linear(srgb):
    linear = np.float32(srgb) / 65535.0
    less = linear <= 0.04045
    linear[less] = linear[less] / 12.92
    linear[~less] = np.power((linear[~less] + 0.055) / 1.055, 2.4)
    linear = (65535.0 * linear).astype(np.uint16)
    return linear


def from_linear(linear):
    srgb = linear.copy()
    less = linear <= 0.0031308
    srgb[less] = linear[less] * 12.92
    srgb[~less] = 1.055 * np.power(linear[~less], 1.0 / 2.4) - 0.055
    return srgb * 255.0


def save(args, hdr, ldr, dct, ts):
    if args.ldr:
        fn = os.path.join(args.output, f'{ts}-ldr.png')
        try:
            log.info(f'Save: type=ldr format=png file="{fn}"')
            cv2.imwrite(fn, ldr)
        except Exception as e:
            log.error(f'Save: type=ldr format=png file="{fn}" {e}')
    if args.format == 'png' or args.format == 'all':
        fn = os.path.join(args.output, f'{ts}.png')
        try:
            log.info(f'Save: type=hdr format=png file="{fn}"')
            cv2.imwrite(fn, hdr)
        except Exception as e:
            log.error(f'Save: type=hdr format=png file="{fn}" {e}')
    if args.format == 'hdr' or args.format == 'all':
        fn = os.path.join(args.output, f'{ts}.hdr')
        try:
            log.info(f'Save: type=hdr format=hdr file="{fn}"')
            adjusted = adjust_gamma(hdr, 1.0 / args.gamma)
            adjusted = adjusted.astype(np.float32) / 65535.0
            cv2.imwrite(fn, adjusted)
        except Exception as e:
            log.error(f'Save: type=hdr format=hdr file="{fn}" {e}')
    if args.format == 'tiff' or args.format == 'all':
        fn = os.path.join(args.output, f'{ts}.tiff')
        try:
            log.info(f'Save: type=hdr format=tif file="{fn}"')
            cv2.imwrite(fn, hdr)
        except Exception as e:
            log.error(f'Save: type=hdr format=tif file="{fn}" {e}')
    if args.format == 'dng' or args.format == 'all':
        fn = os.path.join(args.output, f'{ts}.dng')
        try:
            adjusted = to_linear(hdr)
            adjusted = cv2.cvtColor(adjusted, cv2.COLOR_BGR2RGB)
            write_dng(fn, adjusted, dct)
        except Exception as e:
            log.error(f'Save: type=hdr format=dng file="{fn}" {e}')
    if args.format == 'exr':  # or args.format == 'all': # dont include in all
        fn = os.path.join(args.output, f'{ts}.exr')
        try:
            log.warning(f'Save: type=hdr format=exr file="{fn}" exr is broken in current cv2')
            cv2.imwrite(fn, hdr)
        except Exception as e:
            log.error(f'Save: type=hdr format=exr file="{fn}" {e}')
    if args.json:
        fn = os.path.join(args.output, f'{ts}.json') if args.json else None
        log.info(f'Save: type=json file="{fn}"')
        with open(fn, 'w', encoding='utf8') as f:
            f.write(json.dumps(dct, indent=4))


def write_dng(name_dng: str, hdr, dct = {}):  # noqa: B006
    """
    lib: https://github.com/schoolpost/PiDNG
    specs: https://helpx.adobe.com/content/dam/help/en/photoshop/pdf/DNG_Spec_1_7_1_0.pdf
    issue: https://github.com/schoolpost/PiDNG/issues/85
    """
    from pidng.core import DNGBASE, DNGTags, Tag
    from pidng.defs import Orientation, PreviewColorSpace, PhotometricInterpretation
    ccm1 = [[3240454, 1000000], [-1537138, 1000000], [-498531, 1000000],
            [-969266, 1000000], [1876010, 1000000], [41556, 1000000],
            [55643, 1000000], [-204025, 1000000], [1057225, 1000000]]
    h, w, _c = hdr.shape
    tags = DNGTags()  # tags must be in exact order
    tags.set(Tag.ImageWidth, w)  # 256
    tags.set(Tag.ImageLength, h)  # 257
    tags.set(Tag.BitsPerSample, [16, 16, 16])  # 258
    tags.set(Tag.PhotometricInterpretation, PhotometricInterpretation.Linear_Raw)  # 262
    tags.set(Tag.ImageDescription, json.dumps(dct))  # 270
    tags.set(Tag.Orientation, Orientation.Horizontal)  # 274
    tags.set(Tag.SamplesPerPixel, 3)  # 277
    # tags.set(Tag.DateTime, datetime.datetime.now().isoformat()) # 306 # ISO-8601
    tags.set(Tag.UniqueCameraModel, "sdxl-hdr")  # 50708
    tags.set(Tag.ColorMatrix1, ccm1)  # 50721
    tags.set(Tag.AsShotNeutral, [[1, 1], [1, 1], [1, 1]])  # 50728
    tags.set(Tag.PreviewColorSpace, PreviewColorSpace.sRGB)  # 50970
    raw = DNGBASE()
    raw.options(tags, path="", compress=False)
    raw.convert(hdr, filename=name_dng)


"""
if __name__ == "__main__":
    import sys
    import subprocess
    from rich import print as rprint
    args = sys.argv
    args.pop(0)
    rprint(f'args: {args}')
    for f in args:
        img = cv2.imread(f, cv2.IMREAD_UNCHANGED)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        # img = adjust_gamma(img, 1.0/2.2)
        img = to_linear(img)
        fn = os.path.splitext(f)[0] + ".dng"
        rprint(f'image: input="{f}" shape={img.shape} dtype={img.dtype} output="{fn}"')
        write_dng(fn, img)
        proc = subprocess.run(['assets/dng_validate.exe', "-v", fn], check=False, capture_output=True, text=True)
        rprint(proc.stdout)
        rprint(proc.stderr)
"""

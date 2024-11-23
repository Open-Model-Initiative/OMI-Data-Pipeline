# SPDX-License-Identifier: Apache-2.0
import os
import time
import random
import inspect
import cv2
import numpy as np
import torch
import diffusers
import accelerate
from PIL import Image
from app.logger import log, trace
from app.utils import calculate_statistics
from app.image import save


pipe: diffusers.StableDiffusionXLPipeline = None
dtype = None
device = None
generator = None         # torch generator
iterations = 3           # run dark/normal/light
iteration = 0            # counter
latent = None            # saved latent
custom_timesteps = None  # custom timesteps
total_steps = 0          # counter for total steps
exp = 1.0                # exposure correction
timestep = 200           # correction timestep
trace()


def set_sampler(args):
    sampler = getattr(diffusers, args.sampler, None)
    if sampler is None:
        log.warning(f'Scheduler: sampler={args.sampler} invalid')
        log.info(f'Scheduler: current={pipe.scheduler.__class__.__name__}')
        return
    try:
        keys = inspect.signature(sampler, follow_wrapped=True).parameters.keys()
        config = {}
        for k, v in pipe.scheduler.config.items():
            if k in keys and not k.startswith('_'):
                config[k] = v
        pipe.scheduler = sampler.from_config(config)
        config = [{k: v} for k, v in pipe.scheduler.config.items() if not k.startswith('_')]
        log.info(f'Scheduler: sampler={pipe.scheduler.__class__.__name__} config={config}')
    except Exception as e:
        log.error(f'Scheduler: {e}')
        log.info(f'Scheduler: current={pipe.scheduler.__class__.__name__}')


def patch():
    def retrieve_timesteps(scheduler, num_inference_steps, device, timesteps, sigmas, **kwargs):  # pylint: disable=redefined-outer-name
        if custom_timesteps is None:
            return orig_retrieve_timesteps(scheduler, num_inference_steps, device, timesteps, sigmas, **kwargs)
        else:
            orig_retrieve_timesteps(scheduler, num_inference_steps, device, timesteps, sigmas, **kwargs)  # run original
            return custom_timesteps, len(custom_timesteps)  # but return reduced timesteps

    orig_retrieve_timesteps = diffusers.pipelines.stable_diffusion_xl.pipeline_stable_diffusion_xl.retrieve_timesteps
    diffusers.pipelines.stable_diffusion_xl.pipeline_stable_diffusion_xl.retrieve_timesteps = retrieve_timesteps


def load(args):
    global pipe, dtype, device, generator  # pylint: disable=global-statement
    if args.dtype == 'fp16' or args.dtype == 'float16':
        dtype = torch.float16
    elif args.dtype == 'bf16' or args.dtype == 'bfloat16':
        dtype = torch.bfloat16
    else:
        dtype = torch.float32
    patch()
    torch.set_default_dtype(dtype)
    torch.set_grad_enabled(False)
    torch.backends.cudnn.benchmark = True
    torch.backends.cudnn.benchmark_limit = 0
    torch.backends.cudnn.allow_tf32 = True
    torch.backends.cuda.matmul.allow_tf32 = True
    torch.backends.cuda.enable_flash_sdp(True)
    torch.backends.cuda.enable_mem_efficient_sdp(True)
    torch.backends.cuda.enable_math_sdp(True)
    torch.backends.cudnn.deterministic = True
    if args.device == 'auto':
        accelerator = accelerate.Accelerator()
        device = accelerator.device
    else:
        device = torch.device(args.device)
    generator = torch.Generator(device=device)
    if args.model is None or len(args.model) == 0:
        log.error('Model: not specified')
        return
    if not args.model.lower().endswith('.safetensors'):
        args.model += '.safetensors'
    if not os.path.exists(args.model):
        log.error(f'Model: path="{args.model}" not found')
        return
    log.debug(f'Device: current={torch.cuda.current_device()} cuda={torch.cuda.is_available()} count={torch.cuda.device_count()} name="{torch.cuda.get_device_name(0)}"')
    log.info(f'Loading: model="{args.model}" dtype="{dtype}" device="{device}"')
    t0 = time.time()
    kwargs = {
        'torch_dtype': dtype,
        'safety_checker': None,
        'low_cpu_mem_usage': True,
        'use_safetensors': True,
        'add_watermarker': False,
        'force_upcast': False
    }
    pipe = diffusers.StableDiffusionXLPipeline.from_single_file(args.model, **kwargs).to(dtype=dtype, device=device)
    pipe.set_progress_bar_config(disable=True)
    pipe.fuse_qkv_projections()
    pipe.unet.eval()
    pipe.vae.eval()
    if args.offload:
        pipe.enable_model_cpu_offload(device=device)
    t1 = time.time()
    log.info(f'Loaded: model="{args.model}" time={t1 - t0:.2f}')
    log.debug(f'Memory: allocated={torch.cuda.memory_allocated() / 1e9:.2f} cached={torch.cuda.memory_reserved() / 1e9:.2f}')
    log.debug(f'Model: unet="{pipe.unet.dtype}/{pipe.unet.device}" vae="{pipe.vae.dtype}/{pipe.vae.device}" te1="{pipe.text_encoder.dtype}/{pipe.text_encoder.device}" te2="{pipe.text_encoder_2.device}/{pipe.text_encoder_2.device}"')
    set_sampler(args)


def encode_prompt(prompt, negative_prompt=None, do_classifier_free_guidance=False):
    tokens = pipe.tokenizer(prompt)['input_ids']
    (
        prompt_embeds,
        negative_prompt_embeds,
        pooled_prompt_embeds,
        negative_pooled_prompt_embeds,
    ) = pipe.encode_prompt(
        prompt=prompt,
        negative_prompt=negative_prompt,
        device=device,
        num_images_per_prompt=1,
        do_classifier_free_guidance=do_classifier_free_guidance,
        clip_skip=0,
    )
    return tokens, prompt_embeds, negative_prompt_embeds, pooled_prompt_embeds, negative_pooled_prompt_embeds


def callback(p, step: int, ts: int, kwargs: dict):  # pylint: disable=unused-argument
    def center_tensor(tensor, channel_shift=0.0, full_shift=0.0, offset=0.0):
        tensor -= tensor.mean(dim=(-1, -2), keepdim=True) * channel_shift
        tensor -= tensor.mean() * full_shift - offset
        return tensor

    def exp_correction(channel):
        channel[0:1] = center_tensor(channel[0:1], channel_shift=0.0, full_shift=1.0, offset=exp * (iteration - 1) / 2)
        return channel

    global latent, total_steps  # pylint: disable=global-statement
    total_steps += 1
    latents = kwargs.get('latents', None)  # if we have latent stored, just use it and ignore what model returns
    if custom_timesteps is not None and latent is not None and ts == custom_timesteps[0]:  # replace latent with stored one
        latents = latent.clone()
    if ts < timestep:
        if latent is None:
            latent = latents.clone()  # store latent first time we get here
        for i in range(latents.shape[0]):
            latents[i] = exp_correction(latents[i])
    kwargs['latents'] = latents
    return kwargs


def decode(latents):
    image = pipe.vae.decode(latents / pipe.vae.config.scaling_factor, return_dict=False)[0]
    image = image.squeeze(0).permute(1, 2, 0)
    image = (image / 2 + 0.5).clamp(0, 1)
    image = (255 * image).float().cpu().numpy()
    image = image.astype(np.uint8)
    return image


def run(args, prompt, negative, init):
    global pipe, iteration, latent, custom_timesteps, total_steps, exp, timestep  # pylint: disable=global-statement
    exp = args.exp
    timestep = args.timestep
    if pipe is None:
        log.error('Model: not loaded')
        return
    torch.cuda.reset_peak_memory_stats()
    latent = None
    total_steps = 0

    # Determine if classifier-free guidance is needed
    do_cfg = args.cfg > 1.0
    tokens, prompt_embeds, negative_prompt_embeds, pooled_prompt_embeds, negative_pooled_prompt_embeds = encode_prompt(
        prompt=prompt,
        negative_prompt=negative,
        do_classifier_free_guidance=do_cfg,
    )

    seed = args.seed if args.seed >= 0 else int(random.randrange(4294967294))
    custom_timesteps = None
    kwargs = {
        'prompt_embeds': prompt_embeds,
        'negative_prompt_embeds': negative_prompt_embeds,
        'pooled_prompt_embeds': pooled_prompt_embeds,
        'negative_pooled_prompt_embeds': negative_pooled_prompt_embeds,
        'guidance_scale': args.cfg,
        'num_inference_steps': args.steps,
        'num_images_per_prompt': 1,
        'generator': generator,
        'output_type': 'latent',
        'return_dict': False,
        'callback_on_step_end': callback,
    }

    is_img2img = False
    if init is not None:
        try:
            img = Image.open(init) if isinstance(init, str) else init
            img = img.convert('RGB')
            if img.width == 0 or img.height == 0:
                raise ValueError('invalid image')
            if args.width > 0 and args.height > 0:
                img = img.resize((args.width, args.height))
            is_img2img = True
        except Exception as e:
            log.error(f'Image: file="{init}" {e}')
    if is_img2img:
        kwargs['image'] = img
        kwargs['strength'] = args.strength
        kwargs['num_inference_steps'] = min(int(args.steps // args.strength), 99)
        pipe = diffusers.AutoPipelineForImage2Image.from_pipe(pipe)
    else:
        img = None
        kwargs['width'] = args.width if args.width > 0 else 1024
        kwargs['height'] = args.height if args.width > 0 else 1024
        pipe = diffusers.AutoPipelineForText2Image.from_pipe(pipe)
    pipe.set_progress_bar_config(disable=True)
    log.info(f'Generate: pipeline={pipe.__class__.__name__} prompt="{prompt}" negative="{negative}" image="{img}" tokens={len(tokens)} seed={seed} steps={kwargs["num_inference_steps"]}')
    with torch.inference_mode():
        ts = int(time.time())
        images = []
        t0 = time.time()

        for i in range(iterations):
            iteration = i
            t1 = time.time()
            generator.manual_seed(seed)
            latents = pipe(**kwargs)[0]
            custom_timesteps = pipe.scheduler.timesteps.clone()
            custom_timesteps = custom_timesteps[custom_timesteps < timestep]  # only use timesteps below ts threshold for future runs
            image = decode(latents)
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            yield image
            images.append(image)
            t2 = time.time()
            if args.save:
                name = os.path.join(args.output, f'{ts}-{i}.png')
                cv2.imwrite(name, image)
                log.debug(f'Image: i={iteration + 1}/{iterations} seed={seed} shape={image.shape} name="{name}" time={t2 - t1:.2f} stats={calculate_statistics(image)}')

        try:
            align = cv2.createAlignMTB()
            align.process(images, images)
            merge = cv2.createMergeMertens()
            raw = merge.process(images)  # fp32 0..1
            ldr = np.clip(raw * 255, 0, 255).astype(np.uint8)  # uint8 0..255
            yield ldr
            hdr = np.clip(raw * 65535, 0, 65535).astype(np.uint16)  # uint16 0..65535
            its = len(images) * total_steps / (t2 - t0)
            dct = args.__dict__.copy()
            dct.update({
                'pipeline': pipe.__class__.__name__,
                'model': os.path.basename(dct['model']),
                'image': os.path.basename(init) if isinstance(init, str) else 'upload',
                'width': raw.shape[1],
                'height': raw.shape[0],
                'prompt': prompt,
                'negative': negative,
                'seed': seed,
                'ldr': calculate_statistics(ldr),
                'hdr': calculate_statistics(hdr),
            })
            save(args, hdr, ldr, dct, ts)
            log.info(f'Merge: seed={seed} format="{args.format}" time={t2 - t0:.2f} total-steps={total_steps} its={its:.2f}')
            log.debug(f'Stats: hdr={dct["hdr"]} ldr={dct["ldr"]}')
        except cv2.error as e:
            log.error(f'OpenCV: shapes={[img.shape for img in images]} dtypes={[img.dtype for img in images]} {e}')
            raise
    mem = dict(torch.cuda.memory_stats())
    log.debug(f'Memory: peak={mem["active_bytes.all.peak"] / 1e9:.2f} retries={mem["num_alloc_retries"]} oom={mem["num_ooms"]}')

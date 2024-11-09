# vLLM Deployment CLI Arguments

This section provides a comprehensive list of CLI arguments for the vLLM server. These arguments allow you to fine-tune the server's behavior, performance, and model loading process.

## Model and Tokenizer Configuration

### `--model MODEL`
**Description:**
Specifies the name or path of the Hugging Face model to use.

**Default:**
`"facebook/opt-125m"`

**Usage Context:**
Choose this argument to load a specific pre-trained model or a custom model you’ve developed. Models can be specified by their Hugging Face repository name or a local path.

**How to Select:**
- **Pre-trained Models:** Use the model's Hugging Face identifier, e.g., `"gpt-3"`.
- **Custom Models:** Provide the local file system path to your model directory, e.g., `"/path/to/my-model"`.

### `--tokenizer TOKENIZER`
**Description:**
Specifies the name or path of the Hugging Face tokenizer to use. If unspecified, the model name or path will be used by default.

**Usage Context:**
Use this argument when you need to use a different tokenizer than the one associated with the specified model. This can be useful if you've fine-tuned the tokenizer separately or are experimenting with different tokenization strategies.

**How to Select:**
- **Default Behavior:** Omit this argument to use the tokenizer that matches the model.
- **Custom Tokenizer:** Provide a different tokenizer name or path, e.g., `"bert-base-uncased"` or `"/path/to/custom-tokenizer"`.

### `--revision REVISION`
**Description:**
Specifies a specific model version to use, such as a branch name, tag name, or commit ID from the model repository.

**Usage Context:**
Use this when you need to lock your deployment to a specific version of the model, ensuring consistency across deployments or when testing specific model versions.

**How to Select:**
- **Branch Name:** e.g., `"main"` or `"development"`.
- **Tag Name:** e.g., `"v1.0"`.
- **Commit ID:** e.g., `"a1b2c3d4"`.

### `--tokenizer-revision TOKENIZER_REVISION`
**Description:**
Specifies a specific tokenizer revision to use, similar to `--revision` for the model.

**Usage Context:**
Use this when the tokenizer has its own versioning separate from the model and you need to ensure compatibility or specific features.

**How to Select:**
Same as `--revision`, using branch names, tag names, or commit IDs.

### `--tokenizer-mode {auto,slow,mistral}`
**Description:**
Sets the tokenizer mode.

**Default:**
`"auto"`

**Options:**
- **`auto`:** Automatically selects the best tokenizer mode based on the environment.
- **`slow`:** Uses a slower, more compatible tokenizer implementation.
- **`mistral`:** Utilizes the Mistral tokenizer for optimized performance.

**Usage Context:**
Choose the tokenizer mode based on your performance needs and compatibility requirements. For most users, `auto` suffices, but advanced users might opt for `mistral` for speed or `slow` for broader compatibility.

### `--trust-remote-code`
**Description:**
Allows the execution of remote code from Hugging Face repositories.

**Usage Context:**
Enable this if you are using models that require custom code beyond standard model definitions. This can be necessary for certain advanced models but comes with security considerations.

**How to Select:**
- **Enable:** Include this flag if your model relies on custom code from the repository.
- **Disable (Default):** Do not include the flag to ensure security by preventing execution of remote code.

---

## Model Loading and Format

### `--download-dir DOWNLOAD_DIR`
**Description:**
Specifies the directory to download and load model weights.

**Default:**
Hugging Face cache directory.

**Usage Context:**
Use this argument to control where model weights are stored, which can be important for managing disk space or using shared storage systems.

**How to Select:**
Provide a path to the desired directory, e.g., `"/mnt/models/downloads"`.

### `--load-format {auto,pt,safetensors,npcache,dummy,tensorizer,sharded_state,gguf,bitsandbytes,mistral}`
**Description:**
Defines the format of the model weights to load.

**Default:**
`"auto"`

**Options:**
- **`auto`:** Automatically detects the format.
- **`pt`:** PyTorch format.
- **`safetensors`:** Safe tensor format, optimized for security and speed.
- **`npcache`, `dummy`, `tensorizer`, `sharded_state`, `gguf`, `bitsandbytes`, `mistral`:** Various specialized formats for different optimizations and use cases.

**Usage Context:**
Select the load format based on how your model weights are stored and your performance requirements. For standard deployments, `auto` is typically sufficient, but specialized formats can offer performance benefits.

### `--dtype {auto,half,float16,bfloat16,float,float32}`
**Description:**
Specifies the data type for model weights and activations.

**Default:**
`"auto"`

**Options:**
- **`auto`:** Automatically selects the best data type based on the model and hardware.
- **`half` / `float16`:** 16-bit floating point, reducing memory usage with some precision loss.
- **`bfloat16`:** 16-bit Brain Floating Point, offering a balance between precision and memory.
- **`float` / `float32`:** 32-bit floating point for maximum precision.

**Usage Context:**
Choose the data type based on your hardware capabilities and the trade-off between performance and precision. Lower precision types like `float16` can speed up inference and reduce memory usage but may introduce minor inaccuracies.

### `--max-model-len MAX_MODEL_LEN`
**Description:**
Sets the maximum context length of the model.

**Default:**
Automatically derived based on the model if unspecified.

**Usage Context:**
Use this to limit the maximum number of tokens the model can handle in a single input. This is useful for managing memory usage and ensuring the model operates within desired constraints.

**How to Select:**
Specify an integer value representing the number of tokens, e.g., `8192`. Ensure this value aligns with your use case requirements and hardware limitations.

---

## Quantization and Optimization

### `--quantization {aqlm,awq,deepspeedfp,tpu_int8,fp8,fbgemm_fp8,modelopt,marlin,gguf,gptq_marlin_24,gptq_marlin,awq_marlin,gptq,compressed-tensors,bitsandbytes,qqq,experts_int8,neuron_quant,None}`
**Description:**
Determines the method used to quantize model weights, which can significantly impact performance and memory usage.

**Options:**
- **`None`:** No quantization; use full precision.
- **`bitsandbytes`:** A popular library for 8-bit quantization.
- **`gptq`, `gptq_marlin`, `gptq_marlin_24`:** Quantization techniques tailored for GPT models.
- **`awq`, `awq_marlin`:** Advanced weight quantization methods.
- **Other options (`aqlm`, `deepspeedfp`, etc.):** Specialized quantization methods for various use cases and optimizations.

**Usage Context:**
Quantization reduces the memory footprint and can speed up inference, especially on hardware with limited precision support. Different quantization methods offer varying balances between performance, memory savings, and model accuracy.

**How to Select:**
- **General Use:** `bitsandbytes` is widely supported and effective.
- **Specific Models:** Use `gptq` or related options for GPT-based models.
- **Advanced Needs:** Explore specialized quantization methods like `awq` or `deepspeedfp` based on your performance and compatibility requirements.
- **No Quantization:** Use `None` if precision is critical and resources are sufficient.

### `--kv-cache-dtype {auto,fp8,fp8_e5m2,fp8_e4m3}`
**Description:**
Specifies the data type for KV (Key-Value) cache storage, which is used to store intermediate states during model inference.

**Default:**
`"auto"`

**Options:**
- **`auto`:** Automatically selects the optimal data type.
- **`fp8`:** 8-bit floating point.
- **`fp8_e5m2`, `fp8_e4m3`:** Variants of 8-bit floating point with different exponent and mantissa configurations.

**Usage Context:**
Selecting the appropriate KV cache data type can impact memory usage and inference speed. Lower precision types reduce memory consumption but may affect accuracy.

**How to Select:**
- **Memory-Constrained Environments:** Opt for `fp8` variants to minimize memory usage.
- **Balanced Performance:** Use `auto` to let the system decide based on current settings and hardware.

### `--block-size {8,16,32}`
**Description:**
Sets the token block size for processing contiguous chunks of tokens.

**Default:**
`16`

**Usage Context:**
Block size affects how tokens are batched and processed, impacting both memory usage and throughput. Smaller block sizes can lead to more granular processing, while larger sizes can enhance throughput but may increase memory usage.

**How to Select:**
Choose based on your hardware's memory capacity and desired throughput:
- **Small Models / Limited Memory:** Smaller block sizes like `8`.
- **Large Models / High Throughput Needs:** Larger block sizes like `32`.
- **Balanced Approach:** Default value `16` is suitable for most scenarios.

### `--swap-space SWAP_SPACE`
**Description:**
Defines the CPU swap space size (in GiB) allocated per GPU.

**Default:**
`4`

**Usage Context:**
Swap space is used when GPU memory is insufficient to handle the model's requirements. Allocating more swap space can prevent out-of-memory errors but may lead to increased latency due to data transfer between CPU and GPU.

**How to Select:**
Set based on the size of your model and available system memory:
- **High Memory Models:** Increase swap space to accommodate larger models.
- **Latency-Sensitive Applications:** Use smaller swap space to minimize potential delays.
- **Default Use:** `4 GiB` is a balanced starting point.

### `--gpu-memory-utilization GPU_MEMORY_UTILIZATION`
**Description:**
Specifies the fraction of GPU memory to be utilized.

**Default:**
`0.9` (90%)

**Usage Context:**
Controls how much of the GPU's memory the vLLM server is allowed to use. Setting this helps prevent over-allocation, ensuring other processes can also use GPU resources.

**How to Select:**
- **High Utilization:** Values closer to `1.0` maximize GPU usage but risk overflows.
- **Lower Utilization:** Values like `0.7` provide a buffer for other processes.
- **Default Setting:** `0.9` offers a good balance for most deployments.

### `--enforce-eager`
**Description:**
Forces the use of eager-mode execution in PyTorch.

**Usage Context:**
Eager mode executes operations immediately, which can be useful for debugging or when dynamic computation graphs are required. However, it may not offer the same performance optimizations as other modes.

**How to Select:**
- **Enable:** Use this flag if you need the flexibility of eager execution, such as during development or debugging.
- **Disable (Default):** Omit the flag to allow vLLM to choose the most efficient execution mode.

---

## Parallelism and Distribution

### `--pipeline-parallel-size, -pp PIPELINE_PARALLEL_SIZE`
**Description:**
Sets the number of pipeline stages for model parallelism.

**Default:**
`1` (No pipeline parallelism)

**Usage Context:**
Pipeline parallelism splits the model across multiple devices, allowing different stages of the model to process data simultaneously. This is beneficial for very large models that cannot fit on a single GPU.

**How to Select:**
- **Single GPU Deployment:** Use the default value `1`.
- **Multi-GPU Deployment:** Increase the pipeline parallel size based on the number of available GPUs and the model's architecture. For example, `2` for two pipeline stages.

### `--tensor-parallel-size, -tp TENSOR_PARALLEL_SIZE`
**Description:**
Defines the number of tensor parallel replicas.

**Default:**
`1` (No tensor parallelism)

**Usage Context:**
Tensor parallelism splits individual layers of the model across multiple GPUs, enabling larger models to be trained or served by leveraging multiple devices simultaneously.

**How to Select:**
- **Single GPU Deployment:** Use the default value `1`.
- **Multi-GPU Deployment:** Set this based on the number of GPUs and the model's compatibility with tensor parallelism. For example, `2` for two replicas.

### `--distributed-executor-backend {ray,mp}`
**Description:**
Chooses the backend for distributed serving.

**Options:**
- **`ray`:** Utilizes Ray for distributed execution, which offers scalability and fault tolerance.
- **`mp`:** Uses Python's multiprocessing for simpler, possibly less scalable deployments.

**Usage Context:**
Select the backend based on your infrastructure needs and familiarity:
- **Ray:** Best for scalable, production-grade deployments requiring robust distributed execution.
- **Multiprocessing (`mp`):** Suitable for simpler setups or development environments.

### `--worker-use-ray`
**Description:**
Deprecated flag to use Ray for distributed execution.

**Usage Context:**
Previously used to enable Ray for distributed execution. Now deprecated in favor of `--distributed-executor-backend=ray`.

**How to Select:**
**Do Not Use:** Instead, use `--distributed-executor-backend=ray` to enable Ray.

---

## Performance Tuning

### `--max-num-batched-tokens MAX_NUM_BATCHED_TOKENS`
**Description:**
Sets the maximum number of batched tokens per iteration.

**Usage Context:**
Controlling the number of batched tokens can optimize throughput and latency based on the model and hardware capabilities.

**How to Select:**
Set based on your application's throughput requirements and memory constraints. Higher values can improve throughput but may increase latency.

### `--max-num-seqs MAX_NUM_SEQS`
**Description:**
Defines the maximum number of sequences per iteration.

**Default:**
`256`

**Usage Context:**
Limits the number of sequences processed in a single iteration, which helps manage memory usage and processing time.

**How to Select:**
Adjust based on the expected workload:
- **High Throughput Needs:** Increase the value to process more sequences simultaneously.
- **Memory-Constrained Environments:** Decrease the value to reduce memory usage.

### `--max-paddings MAX_PADDINGS`
**Description:**
Sets the maximum number of padding tokens in a batch.

**Usage Context:**
Managing padding helps optimize memory usage and computational efficiency, especially when dealing with variable-length sequences.

**How to Select:**
Choose a value that balances efficient batching with the variability of your input sequences. Lower values reduce memory overhead but may limit batch sizes.

### `--cpu-offload-gb CPU_OFFLOAD_GB`
**Description:**
Specifies the amount of CPU memory (in GiB) to offload data from the GPU per GPU.

**Default:**
`0`

**Usage Context:**
Offloading data to CPU memory can help manage GPU memory constraints, allowing larger models or batch sizes to be used at the cost of increased data transfer latency.

**How to Select:**
- **High GPU Memory Utilization:** Increase the offload size to utilize CPU memory for excess data.
- **Latency-Sensitive Applications:** Keep the offload size low to minimize data transfer delays.
- **Default Setting:** `0` is suitable when GPU memory is sufficient.

---

## LoRA and Prompt Tuning

### `--enable-lora`
**Description:**
Enables support for LoRA (Low-Rank Adaptation) adapters.

**Usage Context:**
LoRA allows fine-tuning models with fewer parameters by injecting low-rank matrices. This is useful for customizing models without extensive computational resources.

**How to Select:**
- **Enable:** Include this flag if you plan to use LoRA adapters for model fine-tuning.
- **Disable (Default):** Omit the flag if you do not require LoRA support.

### `--max-loras MAX_LORAS`
**Description:**
Sets the maximum number of LoRA adapters to support.

**Default:**
`1`

**Usage Context:**
Determines how many LoRA adapters can be loaded simultaneously, allowing multiple fine-tuned configurations or tasks to be handled.

**How to Select:**
- **Single Task:** Keep the default value `1`.
- **Multiple Tasks:** Increase the value based on the number of concurrent LoRA adapters you need, e.g., `3` for three adapters.

### `--enable-prompt-adapter`
**Description:**
Enables support for prompt tuning adapters.

**Usage Context:**
Prompt tuning allows fine-tuning the model's behavior by optimizing prompt embeddings without altering the model's weights. This is useful for customizing model responses based on specific prompts.

**How to Select:**
- **Enable:** Include this flag if you intend to use prompt adapters for customizing model outputs.
- **Disable (Default):** Omit the flag if prompt tuning is not required.

### `--max-prompt-adapters MAX_PROMPT_ADAPTERS`
**Description:**
Defines the maximum number of prompt adapters to support.

**Usage Context:**
Allows multiple prompt tuning configurations to be loaded, enabling diverse prompt-based customizations.

**How to Select:**
- **Single Configuration:** Keep the default value.
- **Multiple Configurations:** Increase the value based on how many distinct prompt adapters you need, e.g., `5` for five adapters.

---

## Speculative Decoding

### `--speculative-model SPECULATIVE_MODEL`
**Description:**
Specifies the name or path of the speculative model to use for speculative decoding.

**Usage Context:**
Speculative decoding can accelerate inference by generating multiple tokens ahead of time using a smaller model, which are then validated by the primary model.

**How to Select:**
Provide the name or path to a compatible smaller model designed for speculative decoding, e.g., `"gpt-2-small"`.

### `--num-speculative-tokens NUM_SPECULATIVE_TOKENS`
**Description:**
Sets the number of tokens to generate speculatively.

**Usage Context:**
Determines how many tokens the speculative model attempts to generate in advance, impacting both speed and accuracy.

**How to Select:**
- **Higher Values:** Increase throughput but may reduce accuracy if the speculative model makes errors.
- **Lower Values:** Improve accuracy but offer less speedup.
- **Balanced Approach:** Start with a moderate value like `5` and adjust based on performance and accuracy requirements.

---

## Miscellaneous

### `--seed SEED`
**Description:**
Sets the random seed for operations to ensure reproducibility.

**Default:**
`0`

**Usage Context:**
Use this argument to make experiments reproducible by controlling the randomness in model operations.

**How to Select:**
Provide an integer value, e.g., `42`. Use the same seed across runs to achieve consistent results.

### `--disable-log-stats`
**Description:**
Disables the logging of statistical data.

**Usage Context:**
Use this flag to reduce logging verbosity, which can be useful in production environments where logging overhead needs to be minimized.

**How to Select:**
- **Enable:** Include this flag to turn off statistical logging.
- **Disable (Default):** Omit the flag to keep statistics logging enabled.

### `--disable-log-requests`
**Description:**
Disables the logging of incoming requests.

**Usage Context:**
Useful for enhancing privacy or reducing I/O overhead in environments where request logs are unnecessary or sensitive.

**How to Select:**
- **Enable:** Include this flag to turn off request logging.
- **Disable (Default):** Omit the flag to keep request logging enabled.

### `--device {auto,cuda,neuron,cpu,openvino,tpu,xpu}`
**Description:**
Specifies the device type for vLLM execution.

**Default:**
`"auto"`

**Options:**
- **`auto`:** Automatically selects the best available device.
- **`cuda`:** NVIDIA GPUs using CUDA.
- **`neuron`:** AWS Neuron devices.
- **`cpu`:** Central Processing Unit.
- **`openvino`:** Intel OpenVINO toolkit for optimized inference.
- **`tpu`:** Tensor Processing Units.
- **`xpu`:** Other accelerators.

**Usage Context:**
Choose the device based on your hardware infrastructure and performance requirements. Selecting the optimal device can significantly impact inference speed and efficiency.

**How to Select:**
- **Best Performance:** Specify the most powerful available accelerator, e.g., `cuda` for NVIDIA GPUs.
- **Specific Hardware:** Choose based on the hardware you have, such as `tpu` for Google's TPUs.
- **Fallback:** Use `cpu` if no accelerators are available or for debugging purposes.
- **Automatic Selection:** Use `auto` to let vLLM choose the optimal device based on available resources.

---

For a complete list of CLI arguments and their detailed descriptions, please refer to the [vLLM Engine Arguments documentation](https://docs.vllm.ai/en/latest/models/engine_args.html).

## Creating a New Model Configuration File

To create a new model configuration file, follow these steps:

1. **Create a New YAML File:**
   - Navigate to the `configs` directory.
   - Create a new YAML file, e.g., `configs/my_model.yaml`.

2. **Use the Following Template:**

   ```yaml
   docker:
     port: 12345:8000
     options: --ipc=host
     image: vllm/vllm-openai:latest

   vllm:
     model: my-model-name-or-path
     tokenizer_mode: auto
     max_model_len: 8192
     quantization: None
     gpu_memory_utilization: 0.9
     max_num_batched_tokens: 8192
     max_num_seqs: 256
     block_size: 16
     tensor_parallel_size: 1
     dtype: auto
   ```

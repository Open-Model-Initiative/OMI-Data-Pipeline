#!/bin/bash

# Function to display usage information
usage() {
    echo "Usage: $0 [-e <env_file>]"
    echo "  -e <env_file>    Specify an environment file to load"
    exit 1
}

# Parse command line options
while getopts "e:" opt; do
    case ${opt} in
        e )
            ENV_FILE=$OPTARG
            ;;
        \? )
            usage
            ;;
    esac
done

# Load environment file if specified
if [ -n "$ENV_FILE" ]; then
    if [ -f "$ENV_FILE" ]; then
        source "$ENV_FILE"
        echo "Loaded environment from $ENV_FILE"
    else
        echo "Error: Environment file $ENV_FILE not found"
        exit 1
    fi
fi

# Check if HUGGING_FACE_HUB_TOKEN is set
if [ -z "$HUGGING_FACE_HUB_TOKEN" ]; then
    echo "Warning: HUGGING_FACE_HUB_TOKEN is not set. Some features may not work correctly."
    echo "You can set it in your environment or provide it in an env file using the -e option."
fi

# Prepare the Docker command
DOCKER_CMD="docker run --runtime nvidia --gpus all \
    -v ~/.cache/huggingface:/root/.cache/huggingface \
    -p 12434:8000 \
    --ipc=host \
    vllm/vllm-openai:latest \
    --tokenizer-mode mistral \
    --limit-mm-per-prompt 'image=4' \
    --max-model-len 16384 \
    --model \"mistralai/Pixtral-12B-2409\" \
    --env \"HUGGING_FACE_HUB_TOKEN=$HUGGING_FACE_HUB_TOKEN\""


# Execute the Docker command
eval $DOCKER_CMD

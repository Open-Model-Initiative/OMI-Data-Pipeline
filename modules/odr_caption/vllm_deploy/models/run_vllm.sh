#!/bin/bash

set -e

# Function to display usage information
usage() {
    echo "Usage: $0 -c <config_file> [-e <env_file>] [-r]"
    echo "  -c <config_file>  Specify the YAML configuration file"
    echo "  -e <env_file>     Specify an environment file to load (optional)"
    echo "  -r                Force rebuild of the Docker image (optional)"
    exit 1
}

# Parse command line options
REBUILD_FLAG=false
while getopts "c:e:r" opt; do
    case ${opt} in
    c)
        CONFIG_FILE=$OPTARG
        ;;
    e)
        ENV_FILE=$OPTARG
        ;;
    r)
        REBUILD_FLAG=true
        ;;
    \?)
        usage
        ;;
    esac
done

# Check if config file is provided
if [ -z "$CONFIG_FILE" ]; then
    echo "Error: Config file is required"
    usage
fi

# Get the absolute path of the config file directory
CONFIG_DIR=$(cd "$(dirname "$CONFIG_FILE")" && pwd)
CONFIG_FILE="$CONFIG_DIR/$(basename "$CONFIG_FILE")"

echo "Using config file: $CONFIG_FILE"

# Load environment file if specified
if [ -n "$ENV_FILE" ]; then
    ENV_FILE="$CONFIG_DIR/$ENV_FILE"
    if [ -f "$ENV_FILE" ]; then
        source "$ENV_FILE"
        echo "Loaded environment from $ENV_FILE"
    else
        echo "Error: Environment file $ENV_FILE not found"
        exit 1
    fi
fi

# Check if MODEL_DIR is set
if [ -z "$MODEL_DIR" ]; then
    echo "Warning: MODEL_DIR is not set. Using default path ~/.cache/huggingface"
    MODEL_DIR=~/.cache/huggingface
fi

# Function to read YAML file
parse_yaml() {
    local prefix=$2
    local s='[[:space:]]*' w='[a-zA-Z0-9_]*' fs=$(echo @ | tr @ '\034')
    sed -ne "s|^\($s\):|\1|" \
        -e "s|^\($s\)\($w\)$s:$s[\"']\(.*\)[\"']$s\$|\1$fs\2$fs\3|p" \
        -e "s|^\($s\)\($w\)$s:$s\(.*\)$s\$|\1$fs\2$fs\3|p" $1 |
        awk -F$fs '{
        indent = length($1)/2;
        vname[indent] = $2;
        for (i in vname) {if (i > indent) {delete vname[i]}}
        if (length($3) > 0) {
            vn=""; for (i=0; i<indent; i++) {vn=(vn)(vname[i])("_")}
            printf("%s%s%s=\"%s\"\n", "'$prefix'",vn, $2, $3);
        }
    }'
}

# Read YAML file
echo "Parsing YAML file..."
eval $(parse_yaml "$CONFIG_FILE")

echo "Parsed YAML contents:"
parse_yaml "$CONFIG_FILE"

# Function to build Docker image
build_docker_image() {
    local dockerfile="$1"
    local context="$2"
    local image_name="$3"

    echo "Building Docker image: $image_name"
    echo "Dockerfile: $dockerfile"
    echo "Context: $context"
    docker build -t "$image_name" -f "$dockerfile" "$context"
}

# Prepare the Docker command
DOCKER_CMD="docker run --runtime nvidia --gpus all"

# Add volume mount
echo "Adding volume mount..."
echo "  Adding volume: $MODEL_DIR:/root/.cache/huggingface"
DOCKER_CMD="$DOCKER_CMD -v $MODEL_DIR:/root/.cache/huggingface"

# Add port mappings
if [ -n "$docker_port" ]; then
    echo "Adding port mapping: $docker_port"
    DOCKER_CMD="$DOCKER_CMD -p $docker_port"
fi

# Add other Docker options
if [ -n "$docker_options" ]; then
    echo "Adding Docker options: $docker_options"
    DOCKER_CMD="$DOCKER_CMD $docker_options"
fi

# Always add HUGGING_FACE_HUB_TOKEN to Docker command
if [ -n "$HUGGING_FACE_HUB_TOKEN" ]; then
    echo "Adding HUGGING_FACE_HUB_TOKEN to environment"
    DOCKER_CMD="$DOCKER_CMD --env HUGGING_FACE_HUB_TOKEN=$HUGGING_FACE_HUB_TOKEN"
else
    echo "Warning: HUGGING_FACE_HUB_TOKEN is not set. Some features may not work correctly."
fi

# Check if we need to build the Docker image
if [ -n "$docker_build_dockerfile" ] && [ -n "$docker_build_context" ]; then
    # Convert relative paths to absolute paths
    dockerfile="$CONFIG_DIR/$docker_build_dockerfile"
    context="$CONFIG_DIR/$docker_build_context"

    # Check if the image already exists or if rebuild flag is set
    if ! docker image inspect "$docker_image" &>/dev/null || [ "$REBUILD_FLAG" = true ]; then
        if [ "$REBUILD_FLAG" = true ]; then
            echo "Rebuild flag set. Forcing rebuild of image $docker_image..."
        else
            echo "Image $docker_image not found. Building..."
        fi
        build_docker_image "$dockerfile" "$context" "$docker_image"
    else
        echo "Image $docker_image already exists. Skipping build."
    fi
else
    echo "No Dockerfile specified. Assuming image already exists."
fi

# Add image name
if [ -n "$docker_image" ]; then
    echo "Using image: $docker_image"
    DOCKER_CMD="$DOCKER_CMD $docker_image"
else
    echo "Error: Docker image is not specified in the config file"
    exit 1
fi

# Add CLI arguments
echo "Adding CLI arguments:"
for key in "${!vllm_@}"; do
    value="${!key}"
    arg_name="--${key#vllm_}"
    if [ "$value" = "true" ]; then
        echo "  Adding flag: $arg_name"
        DOCKER_CMD="$DOCKER_CMD $arg_name"
    elif [ "$value" != "false" ]; then
        echo "  Adding argument: $arg_name $value"
        DOCKER_CMD="$DOCKER_CMD $arg_name $value"
    fi
done

# Execute the Docker command
echo "Executing: $DOCKER_CMD"
eval $DOCKER_CMD

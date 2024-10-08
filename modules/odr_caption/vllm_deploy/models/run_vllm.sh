#!/bin/bash

set -e

# Function to display usage information
usage() {
    echo "Usage: $0 -c <config_file> [-e <env_file>]"
    echo "  -c <config_file>  Specify the YAML configuration file"
    echo "  -e <env_file>     Specify an environment file to load (optional)"
    exit 1
}

# Parse command line options
while getopts "c:e:" opt; do
    case ${opt} in
        c )
            CONFIG_FILE=$OPTARG
            ;;
        e )
            ENV_FILE=$OPTARG
            ;;
        \? )
            usage
            ;;
    esac
done

# Check if config file is provided
if [ -z "$CONFIG_FILE" ]; then
    echo "Error: Config file is required"
    usage
fi

echo "Using config file: $CONFIG_FILE"

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

# Check if MODEL_DIR is set
if [ -z "$MODEL_DIR" ]; then
    echo "Warning: MODEL_DIR is not set. Using default path ~/.cache/huggingface"
    MODEL_DIR=~/.cache/huggingface
fi

# Function to read YAML file
parse_yaml() {
    local prefix=$2
    local s='[[:space:]]*' w='[a-zA-Z0-9_]*' fs=$(echo @|tr @ '\034')
    sed -ne "s|^\($s\):|\1|" \
         -e "s|^\($s\)\($w\)$s:$s[\"']\(.*\)[\"']$s\$|\1$fs\2$fs\3|p" \
         -e "s|^\($s\)\($w\)$s:$s\(.*\)$s\$|\1$fs\2$fs\3|p"  $1 |
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

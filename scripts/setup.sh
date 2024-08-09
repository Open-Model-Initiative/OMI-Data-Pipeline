#!/bin/bash

# Check if .env file exists
if [ -f ".env" ]; then
    read -p "The .env file already exists. Do you want to replace it? (Y/N): " choice
    if [[ $choice == [Yy]* ]]; then
        rm .env
    else
        echo "Keeping existing .env file. Exiting."
        exit 0
    fi
fi

# Copy .env.template to .env
cp .env.template .env

# Ask user for root directory
read -p "Please enter the root directory path: " rootDir


# Ask user for model directory - default value is rootDir/models_cache
read -p "Please type the model directory path or press enter to use default value ($rootDir/models_cache): " modelDir
if [ -z "$modelDir" ]; then
    modelDir="$rootDir/models_cache"
fi


# Update .env file with root directory
sed -i "s|ROOT_DIR=.*|ROOT_DIR=$rootDir|" .env
sed -i "s|MODEL_CACHE_DIR=.*|MODEL_CACHE_DIR=$modelDir|" .env

echo ".env file has been created/updated with the provided root directory."

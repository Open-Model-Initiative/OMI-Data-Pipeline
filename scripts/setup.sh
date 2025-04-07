#!/bin/bash
# SPDX-License-Identifier: Apache-2.0

# Check if the main .env file exists
if [ -f ".env" ]; then
    read -p "The main .env file already exists. Do you want to replace it? (Y/N): " choice
    if [[ $choice == [Yy]* ]]; then
        rm .env
    else
        echo "Keeping existing .env file. Exiting."
        exit 0
    fi
fi

# Copy the main .env.template to .env
cp .env.template .env


# Check if the frontend .env file exists
if [ -f "./modules/odr_frontend/.env" ]; then
    read -p "The frontend .env file already exists. Do you want to replace it? (Y/N): " choice
    if [[ $choice == [Yy]* ]]; then
        rm ./modules/odr_frontend/.env
    else
        echo "Keeping existing .env file. Exiting."
        exit 0
    fi
fi

# Copy the frontend .env.template to .env
cp ./modules/odr_frontend/.env.template ./modules/odr_frontend/.env


# Ask user for root directory
read -p "Please enter the root directory path: " rootDir


# Ask user for model directory - default value is rootDir/models_cache
read -p "Please type the model directory path or press enter to use default value ($rootDir/models_cache): " modelDir
if [ -z "$modelDir" ]; then
    modelDir="$rootDir/models_cache"
fi


# Update the main .env file with the root directory
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    sed -i "" "s|ROOT_DIR=.*|ROOT_DIR=$rootDir|" .env
    sed -i "" "s|MODEL_CACHE_DIR=.*|MODEL_CACHE_DIR=$modelDir|" .env
else
    # Linux and other Unix-like systems
    sed -i "s|ROOT_DIR=.*|ROOT_DIR=$rootDir|" .env
    sed -i "s|MODEL_CACHE_DIR=.*|MODEL_CACHE_DIR=$modelDir|" .env
fi


echo ".env file has been created/updated with the provided root directory."

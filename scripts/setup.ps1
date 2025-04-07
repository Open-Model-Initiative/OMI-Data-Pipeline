# Check if the main .env file exists
if (Test-Path -Path ".env") {
    $choice = Read-Host "The main .env file already exists. Do you want to replace it? (Y/N)"
    if ($choice -eq "Y" -or $choice -eq "y") {
        Remove-Item -Path ".env"
    } else {
        Write-Host "Keeping existing .env file. Exiting."
        exit
    }
}

# Copy the main .env.template to .env
Copy-Item -Path ".env.template" -Destination ".env"

# Check if the frontend .env file exists
if (Test-Path -Path "./modules/frontend/.env") {
    $choice = Read-Host "The frontend .env file already exists. Do you want to replace it? (Y/N)"
    if ($choice -eq "Y" -or $choice -eq "y") {
        Remove-Item -Path "./modules/frontend/.env"
    } else {
        Write-Host "Keeping existing .env file. Exiting."
        exit
    }
}

# Copy the frontend .env.template to .env
Copy-Item -Path "./modules/frontend/.env.template" -Destination "./modules/frontend/.env"

# Ask user for root directory
$rootDir = Read-Host "Please enter the root directory path"

# Ask user for model directory
$modelDir = Read-Host "Please type the model directory path or press enter to use default value ($rootDir/models_cache)"
# if empty replace with default value
if ($modelDir -eq "") {
    $modelDir = "$rootDir/models_cache"
}

# Update the main .env file with root directory
$envContent = Get-Content -Path ".env"
$envContent = $envContent -replace "ROOT_DIR=.*", "ROOT_DIR=$rootDir"
$envContent = $envContent -replace "MODEL_CACHE_DIR=.*", "MODEL_CACHE_DIR=$modelDir"
Set-Content -Path ".env" -Value $envContent

Write-Host ".env file has been created/updated with the provided root directory."

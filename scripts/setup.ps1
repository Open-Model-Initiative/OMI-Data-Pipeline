# Check if .env file exists
if (Test-Path -Path ".env") {
    $choice = Read-Host "The .env file already exists. Do you want to replace it? (Y/N)"
    if ($choice -eq "Y" -or $choice -eq "y") {
        Remove-Item -Path ".env"
    } else {
        Write-Host "Keeping existing .env file. Exiting."
        exit
    }
}

# Copy .env.template to .env
Copy-Item -Path ".env.template" -Destination ".env"

# Ask user for root directory
$rootDir = Read-Host "Please enter the root directory path"

# Update .env file with root directory
$envContent = Get-Content -Path ".env"
$envContent = $envContent -replace "ROOT_DIR=.*", "ROOT_DIR=$rootDir"
Set-Content -Path ".env" -Value $envContent

Write-Host ".env file has been created/updated with the provided root directory."

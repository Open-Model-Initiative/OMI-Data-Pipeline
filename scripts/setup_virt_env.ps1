# Check if virtual environment exists
if (Test-Path -Path ".\venv") {
    $choice = Read-Host "Virtual environment already exists. Do you want to replace it (R) or update it (U)?"
    if ($choice -eq "R") {
        Remove-Item -Recurse -Force .\venv
        python -m venv venv
        Write-Host "Virtual environment replaced."
    } elseif ($choice -eq "U") {
        Write-Host "Updating existing virtual environment."
    } else {
        Write-Host "Invalid choice. Exiting."
        exit
    }
} else {
    python -m venv venv
    Write-Host "Virtual environment created."
}

# Activate virtual environment
. .\venv\Scripts\Activate.ps1

# Upgrade pip and install requirements
python -m pip install --upgrade pip
pip install -r ./requirements-dev.txt
pre-commit install

# Create virtual environment
python -m venv venv

# Activate virtual environment
. .\venv\Scripts\Activate.ps1

# Upgrade pip and install requirements
python -m pip install --upgrade pip 
pip install -e ./modules/odr_core
pip install -e ./modules/odr_api
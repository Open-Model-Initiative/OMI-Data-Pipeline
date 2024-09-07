# Run the FastAPI server with uvicorn

$env:PYTHONPATH = "."
./venv/Scripts/uvicorn.exe odr_api.app:app --host 0.0.0.0 --port 31100

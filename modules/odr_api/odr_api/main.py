import argparse
from loguru import logger

if __name__ == "__main__":
    import uvicorn

    parser = argparse.ArgumentParser(description="Open Data Repository API")
    parser.add_argument("--dev", action="store_true", help="Run in development mode with hot reloading")
    args = parser.parse_args()

    logger.info("Starting Open Data Repository API from main")

    if args.dev:
        logger.info("Running in development mode with hot reloading")
        uvicorn.run("odr_api.api.app:app", host="0.0.0.0", port=31100, reload=True)
    else:
        logger.info("Running in production mode with 4 workers")
        uvicorn.run("odr_api.api.app:app", host="0.0.0.0", port=31100, workers=8)

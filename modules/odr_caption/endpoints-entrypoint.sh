# SPDX-License-Identifier: Apache-2.0
#!/bin/bash

# Start the FastAPI server with uvicorn
uvicorn odr_caption.server.app:app \
    --host "0.0.0.0" \
    --port 32100 \
    --reload

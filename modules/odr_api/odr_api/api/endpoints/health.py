# SPDX-License-Identifier: Apache-2.0
from fastapi import APIRouter, status
from pydantic import BaseModel


router = APIRouter(tags=["health"])


class HealthCheck(BaseModel):
    status: str = "OK"


@router.get("/health", response_model=HealthCheck, status_code=status.HTTP_200_OK)
def get_health():
    """
    Perform a health check on the API.

    Returns:
        HealthCheck: A model containing the status of the API.
    """
    return HealthCheck(status="OK")

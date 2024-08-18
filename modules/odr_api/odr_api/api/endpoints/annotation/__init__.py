from odr_api.api.endpoints.annotation.annotation import router as annotation_router
from odr_api.api.endpoints.annotation.annotation_source import router as annotation_source_router
from odr_api.api.endpoints.annotation.annotation_rating import router as annotation_rating_router
from fastapi import APIRouter

router = APIRouter(tags=["annotation"])

router.include_router(annotation_router)
router.include_router(annotation_source_router)
router.include_router(annotation_rating_router)

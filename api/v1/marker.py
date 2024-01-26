from fastapi import APIRouter, Depends

from schemas.dnm import DnmGetRandomResponse
from schemas.marker import MarkerGetAllResponse
from service.impl.dnm_service import DnmService
from service.impl.marker_service import MarkerService

# Create router instance
router = APIRouter()


@router.get("/marker/", response_model=MarkerGetAllResponse)
async def get_all_markers(
        marker_service: MarkerService = Depends(MarkerService)
) -> MarkerGetAllResponse:
    return marker_service.get_all_markers()


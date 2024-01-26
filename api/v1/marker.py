from fastapi import APIRouter, Depends

from handlers.dnm import handle_get_random_dnm_exceptions
from schemas.dnm import DnmGetRandomResponse
from service.impl.dnm_service import DnmService

# Create router instance
router = APIRouter()


@router.get("/marker/", response_model=DnmGetRandomResponse)
def get_all_markers(
        public_id: str,
        marker_service: DnmService = Depends(DnmService)
) -> DnmGetRandomResponse:
    pass


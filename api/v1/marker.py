from typing import List

from fastapi import APIRouter, Depends, Form, File, UploadFile

from middleware.api_key import validate_api_key
from middleware.user import is_admin
from schemas.dnm import DnmGetRandomResponse
from schemas.marker import MarkerResponse, CreateMarkerRequest
from service.impl.dnm_service import DnmService
from service.impl.marker_service import MarkerService

# Create router instance
router = APIRouter()


@router.get("/marker/all", response_model=List[MarkerResponse])
async def get_all_markers(
        marker_service: MarkerService = Depends(MarkerService),
        _=Depends(validate_api_key),
) -> List[MarkerResponse]:

    return marker_service.get_all_markers()


@router.get("/marker/model/{model_public_id}", response_model=List[MarkerResponse])
async def get_markers_by_ai(
        model_public_id: str,
        marker_service: MarkerService = Depends(MarkerService),
        _=Depends(is_admin),
) -> List[MarkerResponse]:

    return marker_service.get_markers_by_ai_model(model_public_id)


@router.post("/marker/create")
async def create_marker(
        marker_service: MarkerService = Depends(MarkerService),
        name: str = Form(...),
        image: UploadFile = File(None),
        _=Depends(is_admin),
):

    return marker_service.create_marker(CreateMarkerRequest(
        name=name,
        image=image
    ))


@router.delete("/marker/{marker_id}")
async def delete_marker(
        marker_id: int,
        marker_service: MarkerService = Depends(MarkerService),
        _=Depends(is_admin),
):

    return marker_service.delete_marker(marker_id)


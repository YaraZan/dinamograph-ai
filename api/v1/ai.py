from typing import Annotated, Dict, Any, Optional, Union
from fastapi import APIRouter, Depends, Header, UploadFile, File, HTTPException, status, Form

from middleware.user import is_admin
from middleware.api_key import validate_api_key
from schemas.ai import AIModelCreateRequest, AIModelUpdateRequest, AIModelGetAllResponse, AIModelResponse
from schemas.dnm import DnmGetRandomResponse, DnmMarkRequest
from service.impl.ai_service import AIService
from service.impl.api_key_service import ApiKeyService
from service.impl.dnm_service import DnmService
from service.impl.token_service import TokenService

# Create router instance
router = APIRouter()


@router.get("/ai/all", response_model=AIModelGetAllResponse)
async def get_all_ai_models(
        ai_service: AIService = Depends(AIService),
        _=Depends(is_admin),
) -> AIModelGetAllResponse:

    return ai_service.get_all_models()


@router.get("/ai/{model_public_id}", response_model=AIModelResponse)
async def get_model_details(
        model_public_id: str,
        ai_service: AIService = Depends(AIService),
        _=Depends(is_admin),
) -> AIModelResponse:

    return ai_service.get_model_detail(model_public_id)


@router.post("/ai/create")
async def create_model(
        create_model_request: AIModelCreateRequest,
        ai_service: AIService = Depends(AIService),
        _=Depends(is_admin),
):

    return ai_service.create_model(create_model_request)


@router.put("/ai/update")
async def update_model(
        update_model_request: AIModelUpdateRequest,
        ai_service: AIService = Depends(AIService),
        _=Depends(is_admin),
):

    return ai_service.update_model(update_model_request)


@router.delete("/ai/delete")
async def delete_model(
        model_public_id: str,
        ai_service: AIService = Depends(AIService),
        _=Depends(is_admin),
):

    return ai_service.delete_model(model_public_id)


@router.post("/ai/predict")
async def predict_by_model(
        ai_service: AIService = Depends(AIService),
        _=Depends(validate_api_key),
        model_name: str = Form(...),
        image: Optional[UploadFile] = File(None),
        is_raw: bool = Form(False),
        raw: Optional[Dict[Any, Any]] = Form(None)
):

    return await ai_service.predict(
        model_name=model_name,
        image=image,
        is_raw=is_raw,
        raw=raw
    )

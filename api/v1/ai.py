from typing import Annotated, Dict, Any, Optional, Union, List
from fastapi import APIRouter, Depends, Header, UploadFile, File, HTTPException, status, Form
from pydantic import BaseModel

from middleware.user import is_admin, current_user
from middleware.api_key import validate_api_key
from schemas.ai import AIModelCreateRequest, AIModelUpdateRequest, AIModelGetAllResponse, AIModelResponse, \
    PredictByRawRequest
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
        _=Depends(current_user),
) -> AIModelGetAllResponse:

    return ai_service.get_all_models()


@router.get("/ai/{model_public_id}", response_model=AIModelResponse)
async def get_model_details(
        model_public_id: str,
        ai_service: AIService = Depends(AIService),
        _=Depends(current_user),
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


@router.post("/ai/predict/image")
async def predict_by_image(
        ai_service: AIService = Depends(AIService),
        _=Depends(validate_api_key),
        model_name: str = Form(...),
        image: UploadFile = File(...),
):

    return await ai_service.predict(
        model_name=model_name,
        image=image,
        is_raw=False,
        raw=None
    )


@router.post("/ai/predict/raw")
async def predict_by_raw_data(
        predict_by_raw_request: PredictByRawRequest,
        ai_service: AIService = Depends(AIService),
        _=Depends(validate_api_key),
):

    return await ai_service.predict(
        model_name=predict_by_raw_request.model_name,
        image=None,
        is_raw=True,
        raw=predict_by_raw_request.raw_data
    )

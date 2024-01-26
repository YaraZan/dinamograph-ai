from typing import Annotated, Dict, Any, Optional, Union
from fastapi import APIRouter, Depends, Header, UploadFile, File, HTTPException, status

from schemas.ai import AIModelRequest
from schemas.dnm import DnmGetRandomResponse, DnmMarkRequest
from service.impl.ai_service import AIService
from service.impl.api_key_service import ApiKeyService
from service.impl.dnm_service import DnmService

# Create router instance
router = APIRouter()


@router.post("/ai/create")
async def create_model(
        ai_model_request: AIModelRequest,
        ai_service: AIService = Depends(AIService),
        api_key_service: ApiKeyService = Depends(ApiKeyService),
        authorization: str = Header(...),
):
    scheme, token = authorization.split()

    if scheme.lower() != "basic":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Некорректный формат токена авторизации")

    api_key_service.validate_api_key(token)

    return ai_service.create_model(ai_model_request.model_name)


@router.post("/ai/train")
async def train_model(
        ai_model_request: AIModelRequest,
        ai_service: AIService = Depends(AIService),
        api_key_service: ApiKeyService = Depends(ApiKeyService),
        authorization: str = Header(...),
):
    scheme, token = authorization.split()

    if scheme.lower() != "basic":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Некорректный формат токена авторизации")

    api_key_service.validate_api_key(token)

    return ai_service.train(ai_model_request.model_name)


@router.post("/ai/predict")
async def predict_by_model(
        ai_model_request: AIModelRequest,
        ai_service: AIService = Depends(AIService),
        api_key_service: ApiKeyService = Depends(ApiKeyService),
        authorization: str = Header(...),
        image: Optional[UploadFile] = File(None),
        is_raw: bool = False,
        raw: Optional[Dict[Any, Any]] = None
):
    scheme, token = authorization.split()

    if scheme.lower() != "basic":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Некорректный формат токена авторизации")

    api_key_service.validate_api_key(token)

    return ai_service.predict(
        model_name=ai_model_request.model_name,
        image=image,
        is_raw=is_raw,
        raw=raw
    )

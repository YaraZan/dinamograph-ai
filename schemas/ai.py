from datetime import datetime
from typing import List, Optional, Dict, Any

from fastapi import UploadFile, File
from pydantic import BaseModel


class AIModelResponse(BaseModel):
    name: str
    public_id: str
    is_public: bool
    created_at: datetime
    categories_num: int
    train_amount: int


class AIModelGetAllResponse(BaseModel):
    models: List[AIModelResponse]


class AIModelUpdateRequest(BaseModel):
    model_public_id: str
    is_public: Optional[bool] = None
    new_name: Optional[str] = None


class AIModelCreateRequest(BaseModel):
    model_name: str
    epochs: Optional[int] = 35


class AIModelPredictRequest(BaseModel):
    model_public_id: str
    is_raw: bool = False
    image: Optional[UploadFile] = File(None)
    raw: Optional[Dict[Any, Any]] = None


class PredictByRawRequest(BaseModel):
    model_name: str
    raw_data: list

from datetime import datetime
from typing import List, Optional, Dict, Any

from fastapi import UploadFile, File
from pydantic import BaseModel


class AIModelResponse(BaseModel):
    name: str
    public_id: str
    created_at: datetime
    categories_num: int
    train_amount: int


class AIModelGetAllResponse(BaseModel):
    models: List[AIModelResponse]


class AIModelUpdateRequest(BaseModel):
    model_public_id: str
    new_name: str


class AIModelCreateRequest(BaseModel):
    model_name: str
    epochs: Optional[int] = 35


class AIModelPredictRequest(BaseModel):
    model_public_id: str
    is_raw: bool = False
    image: Optional[UploadFile] = File(None)
    raw: Optional[Dict[Any, Any]] = None

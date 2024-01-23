from pydantic import BaseModel


class AiTrain(BaseModel):
    model_id: int
    epochs: int


class AiPredict(BaseModel):
    model_id: int
    url: str


class AiCreate(BaseModel):
    model_name: str

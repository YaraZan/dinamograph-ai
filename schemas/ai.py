from pydantic import BaseModel


class AIModelRequest(BaseModel):
    model_name: str


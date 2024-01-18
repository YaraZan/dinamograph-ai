from pydantic import BaseModel

class DinamogrammGetRequest(BaseModel):
    public_id: str
    api_key: str

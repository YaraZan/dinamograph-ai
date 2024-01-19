from pydantic import BaseModel

class DnmGetRequest(BaseModel):
    public_id: str

class DnmMarkRequest(BaseModel):
    dnm_id: int
    marker_id: int


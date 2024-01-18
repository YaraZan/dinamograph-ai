from pydantic import BaseModel

class DinamogrammMarkRequest(BaseModel):
    id: int
    marker_id: int

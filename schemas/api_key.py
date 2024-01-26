from pydantic import BaseModel, UUID4


class ApiKeyResponse(BaseModel):
    public_id: UUID4
    key: str

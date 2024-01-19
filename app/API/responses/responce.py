from typing import List, Union, Any, Dict
from pydantic import BaseModel


class Response(BaseModel):
    message: str | None
    status: int | None
    data: Any | None